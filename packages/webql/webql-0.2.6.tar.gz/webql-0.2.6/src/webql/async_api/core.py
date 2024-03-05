"""
This module is an entrypoint to WebQL service
"""

import logging

from webql.async_api.web import InteractiveItemTypeT, PageTypeT, PlaywrightWebDriver, WebDriver
from webql.common.storage_state import StorageState

from .session import Session

log = logging.getLogger(__name__)


async def start_async_session(
    url: str,
    *,
    web_driver: WebDriver[InteractiveItemTypeT, PageTypeT] = PlaywrightWebDriver(),
    user_session: StorageState = None,
) -> Session[InteractiveItemTypeT, PageTypeT]:
    """Start a new asynchronous WebQL session.

    Parameters:

    url (str): The URL to start the session with.
    web_driver (optional): The web driver to use. Defaults to Playwright web driver.

    Returns:

    Session: The new session.
    """
    log.debug(f"Starting asynchronous session with {url}")

    await web_driver.start_browser(user_session_extras=user_session)
    await web_driver.open_url(url)
    session = Session[InteractiveItemTypeT, PageTypeT](web_driver)
    return session
