(() => {
    if (window.myPageObserver) {
        window.myPageObserver.disconnect();
        delete window.myPageObserver;
    }
})();
