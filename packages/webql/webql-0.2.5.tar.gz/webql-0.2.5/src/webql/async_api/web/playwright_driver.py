import asyncio
import json
import time
from typing import Union

from playwright.async_api import Error, Frame, Locator, Page, StorageState, async_playwright
from playwright_stealth import StealthConfig, stealth_async

from webql.async_api.web.network_monitor import PageActivityMonitor
from webql.async_api.web.web_driver import WebDriver
from webql.common.driver_constants import RENDERER, USER_AGENT, VENDOR
from webql.common.driver_settings import ProxySettings, ScrollDirection, StealthModeConfig
from webql.common.errors import (
    AccessibilityTreeError,
    ElementNotFoundError,
    NoOpenBrowserError,
    NoOpenPageError,
    OpenUrlError,
)
from webql.common.js_snippets.snippet_loader import load_js
from webql.common.utils import ensure_url_scheme

from .web_driver import WebDriver


class PlaywrightWebDriver(WebDriver[Locator, Page]):
    def __init__(self, headless=True, proxy: ProxySettings = None) -> None:
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._current_page = None
        """The current page that is being interacted with."""

        self._original_html = None
        """The page's original HTML content, prior to any WebQL modifications"""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

        self._proxy = proxy

        self._page_monitor = None

        self._current_tf_id = None

        self._stealth_mode_config = None

    def locate_interactive_element(self, response_data: dict) -> Locator:
        """
        Locates an interactive element in the web page.

        Parameters:

        response_data (dict): The data of the interactive element from the WebQL response.

        Returns:

        Locator: The interactive element.
        """
        tf623_id = response_data.get("tf623_id")
        if not tf623_id:
            raise ElementNotFoundError("tf623_id")
        iframe_path = response_data.get("attributes", {}).get("iframe_path")
        return self.find_element_by_id(tf623_id, iframe_path)

    async def get_text_content(self, web_element: Locator) -> str:
        """
        Gets the text content of the web element.

        Parameters:

        web_element (Locator): The web element.

        Returns:

        str: The text content of the web element.
        """
        return await web_element.text_content()

    async def start_browser(self, user_session_extras: dict = None):
        """
        Starts a new browser session and set user session state (if there is any).
        """
        await self._start_browser(
            headless=self._headless, user_session_extras=user_session_extras, proxy=self._proxy
        )

    @property
    def is_headless(self) -> bool:
        """Returns whether the browser is running in headless mode or not."""
        return self._headless

    async def stop_browser(self):
        """Closes the current browser session."""
        if self._context:
            await self._context.close()
            self._context = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    async def enable_stealth_mode(
        self,
        webgl_vendor: str = VENDOR,
        webgl_renderer: str = RENDERER,
        nav_user_agent: str = USER_AGENT,
    ):
        """Enable the stealth mode and set the stealth mode configuration.

        Parameters:
        webgl_vendor (str): The WebGL vendor to use.
        webgl_renderer (str): The WebGL renderer to use.
        nav_user_agent (str): The navigator user agent to use.
        """
        self._stealth_mode_config = StealthModeConfig(
            vendor=webgl_vendor, renderer=webgl_renderer, nav_user_agent=nav_user_agent
        )

    async def open_url(self, url: str):
        """
        Opens a new page and navigates to the given URL.
        """
        if not self._browser:
            raise NoOpenBrowserError()
        await self._open_url(url)

    async def get_current_url(self) -> str:
        """Get the URL of the active page."""
        if not self._current_page:
            raise NoOpenPageError()
        return self._current_page.url

    async def get_html(self) -> dict:
        """Returns the original HTML (i.e. without any WebQL modifications) fetched from the most recently loaded page".

        Returns:

        string: The HTML content of the web page.
        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')
        return self._original_html

    async def get_current_page(self) -> Page:
        """Returns the current page.

        Returns:

        Page: The current page.
        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')
        return self._current_page

    async def open_html(self, html: str):
        """
        Opens a new page and loads the given HTML content.
        """
        if not self._browser:
            raise NoOpenBrowserError()
        self._current_page = await self._context.new_page()
        self._current_tf_id = 0
        await self._current_page.set_content(html)

    async def prepare_accessiblity_tree(self, lazy_load_pages_count: int = 3) -> dict:
        """Prepare the AT by modifing the dom. It will return the accessibility tree after waiting for page to load and dom modification.

        Parameters:
        lazy_load_pages_count: The number of times to scroll down and up the page.

        Returns:
        dict: AT of the page
        """
        if not self._current_page:
            raise NoOpenPageError()

        self._original_html = await self._current_page.content()
        await self._preprocess_dom(lazy_load_pages_count=lazy_load_pages_count)

        accessibility_tree = None
        try:
            accessibility_tree = await self._get_page_accessibility_tree(self._current_page)
            await self._process_iframes(accessibility_tree)

        except Exception as e:
            raise AccessibilityTreeError() from e

        return accessibility_tree

    async def get_accessibility_tree(self) -> dict:
        """Returns the up-to-date accessibility tree of the page.

        Returns:
        dict: The accessibility tree of the page.
        """
        try:
            accessibility_tree = await self._get_page_accessibility_tree(self._current_page)
            await self._process_iframes(accessibility_tree, modify_dom=False)
        except Exception as e:
            raise AccessibilityTreeError() from e

        return accessibility_tree

    async def wait_for_page_ready_state(self):
        """Wait for the page to reach the "Page Ready" or stable state."""
        if not self._page_monitor:
            self._page_monitor = PageActivityMonitor()
        else:
            # Reset the network monitor to clear the logs
            self._page_monitor.reset()

        # Add event listeners to track DOM changes and network activities
        await self._add_page_event_listeners()

        # Wait for the page to reach the "Page Ready" state
        await self._determine_load_state(self._page_monitor)

        # Remove the event listeners to prevent overwhelming the async event loop
        await self._remove_page_event_listeners()

    async def scroll_page(self, scroll_direction: ScrollDirection, pixels: int = 720):
        """Scrolls the page up or down.

        Parameters:
        scroll_direction (ScrollDirection): The direction to scroll the page.
        pixels (int): The number of pixels to scroll.
        """
        if not self._current_page:
            raise NoOpenPageError()

        delta_y = pixels if scroll_direction == ScrollDirection.DOWN else -pixels
        await self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)

    async def scroll_to_bottom(self):
        """Scrolls the page to the bottom."""
        if not self._current_page:
            raise NoOpenPageError()

        await self._current_page.evaluate(load_js("scroll_to_bottom"))

    async def scroll_to_top(self):
        """Scrolls the page to the top."""
        if not self._current_page:
            raise NoOpenPageError()

        await self._current_page.evaluate(load_js("scroll_to_top"))

    async def get_user_session_state(self) -> StorageState:
        """Returns the user session / storage state of the page."""
        if not self._browser:
            raise NoOpenBrowserError()
        return await self._context.storage_state()

    async def _process_iframes(
        self,
        page_accessibility_tree: dict = None,
        *,
        iframe_path: str = "",
        frame: Frame = None,
        modify_dom: bool = True,
    ):
        """
        Recursively retrieves the accessibility trees for all iframes in a page or frame.

        Parameters:
            iframe_path (str): The path of the iframe in the frame hierarchy.
            frame (Frame): The frame object representing the current frame.
            page_accessibility_tree (dict): The accessibility tree of the page.

        Returns:
            None
        """
        if frame is None:
            iframes = await self._current_page.query_selector_all("iframe")
        else:
            content_frame = await frame.content_frame()
            iframes = await content_frame.query_selector_all("iframe")

        for iframe in iframes:
            iframe_id = await iframe.get_attribute("tf623_id")
            iframe_path_to_send = ""
            if iframe_path:
                iframe_path_to_send = f"{iframe_path}."
            iframe_path_to_send = f"{iframe_path_to_send}{iframe_id}"
            iframe_accessibility_tree = await self._get_frame_accessibility_tree(
                iframe, iframe_path_to_send, modify_dom=modify_dom
            )

            self._merge_iframe_tree_into_page(
                iframe_id, page_accessibility_tree, iframe_accessibility_tree
            )

            await self._process_iframes(
                iframe_path=iframe_path_to_send,
                frame=iframe,
                page_accessibility_tree=page_accessibility_tree,
                modify_dom=modify_dom,
            )

    async def _get_page_accessibility_tree(self, page: Page) -> dict:
        """
        Retrieves the accessibility tree for the given page.

        Returns:
            dict: The accessibility tree for the page.
        """
        return await page.accessibility.snapshot(interesting_only=False)

    async def _get_frame_accessibility_tree(
        self, frame: Frame, iframe_path, modify_dom: bool = True
    ) -> dict:
        """
        Retrieves the accessibility tree for a given frame.

        Parameters:
            frame (Frame): The frame for which to retrieve the accessibility tree.
            iframe_path: The path of the iframe within the frame.

        Returns:
            dict: The accessibility tree for the frame.
        """
        frame_context = await frame.content_frame()

        # Prevent modify dom multiple times when getting the most up-to-date accessibility tree
        if modify_dom:
            await self._modify_dom(context=frame_context, iframe_path=iframe_path)

        content_frame_document_serialized = await frame_context.evaluate(load_js("serialize_dom"))
        temp_browser = await self._playwright.chromium.launch()
        temp_page = await temp_browser.new_page()
        # temp_page.route("**/*", lambda route: route.abort())
        await temp_page.set_content(content_frame_document_serialized)
        await temp_page.wait_for_load_state("load")
        accessibility_tree = await self._get_page_accessibility_tree(temp_page)
        await temp_browser.close()

        return accessibility_tree

    def _merge_iframe_tree_into_page(
        self, iframe_id, accessibility_tree: dict, iframe_accessibility_tree: dict
    ):
        """
        Stitches the iframe accessibility tree with the page accessibility tree.

        Parameters:
            iframe_id (str): The ID of the iframe.
            accessibility_tree (dict): The accessibility tree of the page.
            iframe_accessibility_tree (dict): The accessibility tree of the iframe.

        Returns:
            None
        """
        for child in accessibility_tree.get("children", []):
            keyshortcuts_str = child.get("keyshortcuts", "{}")
            keyshortcuts_dict = json.loads(keyshortcuts_str)
            if "children" not in child:
                child["children"] = []
            if "tf623_id" in keyshortcuts_dict and keyshortcuts_dict["tf623_id"] == iframe_id:
                child["children"].append(iframe_accessibility_tree)
                break
            self._merge_iframe_tree_into_page(iframe_id, child, iframe_accessibility_tree)

    async def _preprocess_dom(self, lazy_load_pages_count=3):
        """Scroll the page and Modifies the dom by assigning a unique ID to every node in the document.

        Parameters:
        lazy_load_pages_count (int): The number of pages to scroll down and up to load lazy loaded content.
        """
        if not self._current_page:
            raise NoOpenPageError()

        await self._page_scroll(pages=lazy_load_pages_count)
        await self._modify_dom(context=self._current_page)

    async def _apply_stealth_mode_to_page(self, page: Page):
        """Applies stealth mode to the given page.

        Parameters:
        page (Page): The page to which stealth mode will be applied.
        """
        # Only mask User Agent in headless mode to avoid detection for headless browsers
        mask_user_agent = self._headless

        await stealth_async(
            page,
            config=StealthConfig(
                vendor=self._stealth_mode_config["vendor"],
                renderer=self._stealth_mode_config["renderer"],
                # nav_user_agent will only take effect when navigator_user_agent parameter is True
                nav_user_agent=self._stealth_mode_config["nav_user_agent"],
                navigator_user_agent=mask_user_agent,
            ),
        )

    async def _open_url(self, url: str):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided.

        Parameters:

        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.

        """

        self._current_page = None
        url = ensure_url_scheme(url)

        try:
            page = await self._context.new_page()
            if self._stealth_mode_config is not None:
                await self._apply_stealth_mode_to_page(page)
            self._current_tf_id = 0
            await page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            raise OpenUrlError() from e

        self._current_page = page

    async def _modify_dom(self, context: Union[Page, Frame], iframe_path=None):
        """
        Modifies the DOM and updates the current_tf_id.

        Parameters:
            context (Page | Frame): The context in which the DOM will be modified.
            iframe_path (str, optional): The path to the iframe. Defaults to None.
        """
        self._current_tf_id = await context.evaluate(
            load_js("modify_dom"),
            {"iframe_path": iframe_path, "current_tf_id": self._current_tf_id},
        )

    async def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up to load all contents on the page.

        Parameters:

        pages (int): The number of pages to scroll down.
        """
        if pages < 1:
            return

        if self._stealth_mode_config is None:
            delta_y = 10000
            for _ in range(pages):
                await self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                await asyncio.sleep(0.1)

            delta_y = -10000
            await asyncio.sleep(1)
            for _ in range(pages):
                await self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                await asyncio.sleep(0.1)
        else:
            for _ in range(pages):
                await self.scroll_to_bottom()
                await asyncio.sleep(0.1)

            await asyncio.sleep(1)

            for _ in range(pages):
                await self.scroll_to_top()
                await asyncio.sleep(0.1)

    async def _start_browser(
        self,
        user_session_extras: dict = None,
        headless=True,
        proxy: ProxySettings = None,
    ):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        ignored_args = [
            "--enable-automation",
            "--disable-extensions",
        ]
        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
        ]
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=headless, proxy=proxy, args=args, ignore_default_args=ignored_args
        )
        self._current_tf_id = 0
        self._context = await self._browser.new_context(
            user_agent=USER_AGENT, storage_state=user_session_extras
        )

    def _get_frame_context(self, iframe_path: str = None) -> Union[Frame, Page]:
        """
        Returns the frame context for the given iframe path.

        Parameters:
            iframe_path (str): The path of the iframe within the frame.

        Returns:
            Frame | Page: The frame context for the given iframe path.
        """
        if not iframe_path:
            return self._current_page
        iframe_path_list = iframe_path.split(".")
        frame_context = self._current_page
        for iframe_id in iframe_path_list:
            frame_context = frame_context.frame_locator(f"[tf623_id='{iframe_id}']")
        return frame_context

    def find_element_by_id(self, tf623_id: str, iframe_path: str = None) -> Locator:
        """
        Finds an element by its TF ID within a specified iframe.

        Args:
            tf623_id (str): The generated tf id of the element to find.
            iframe_path (str): The path to the iframe containing the element.

        Returns:
            Locator: The located element.

        Raises:
            ElementNotFoundError: If the element with the specified TF ID is not found.
        """
        try:
            element_frame_context = self._get_frame_context(iframe_path)
            return element_frame_context.locator(f"[tf623_id='{tf623_id}']")
        except Exception as e:
            raise ElementNotFoundError(tf623_id) from e

    async def _determine_load_state(self, monitor: PageActivityMonitor, timeout_seconds=14):
        start_time = time.time()

        while True:
            try:
                last_updated_timestamp = await self._current_page.evaluate(
                    load_js("get_last_dom_change")
                )
            # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
            except Error:
                while True:
                    if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                        break
                    await asyncio.sleep(0.2)

            if monitor.check_conditions(last_active_dom_time=last_updated_timestamp):
                break
            if time.time() - start_time > timeout_seconds:
                break
            await asyncio.sleep(0.3)

    async def _add_page_event_listeners(self):
        self._current_page.on("request", self._page_monitor.track_network_request)
        self._current_page.on("requestfinished", self._page_monitor.track_network_response)
        self._current_page.on("requestfailed", self._page_monitor.track_network_response)
        self._current_page.on("load", self._page_monitor.track_load)

        try:
            await self._current_page.evaluate(load_js("add_dom_change_listener"))
        # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
        except Error:
            start_time = time.time()
            while True:
                if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                    break
                await asyncio.sleep(0.2)

    async def _remove_page_event_listeners(self):
        self._current_page.remove_listener("request", self._page_monitor.track_network_request)
        self._current_page.remove_listener(
            "requestfinished", self._page_monitor.track_network_response
        )
        self._current_page.remove_listener(
            "requestfailed", self._page_monitor.track_network_response
        )
        self._current_page.remove_listener("load", self._page_monitor.track_load)
        await self._current_page.evaluate(load_js("remove_dom_change_listener"))
