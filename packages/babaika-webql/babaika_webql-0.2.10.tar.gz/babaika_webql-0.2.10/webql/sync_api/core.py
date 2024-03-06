"""
This module is an entrypoint to WebQL service
"""

import logging
from typing import Any

from webql.sync_api.web import InteractiveItemTypeT, PageTypeT, PlaywrightWebDriver, WebDriver

from .session import Session

log = logging.getLogger(__name__)


def start_session(
    url: str,
    *,
    web_driver: WebDriver[InteractiveItemTypeT, PageTypeT] = PlaywrightWebDriver(),
    user_auth_session: Any = None,
) -> Session[InteractiveItemTypeT, PageTypeT]:
    """Start a new synchronous WebQL session.

    Parameters:

    url (str): The URL to start the session with.
    web_driver (optional): The web driver to use. Defaults to Playwright web driver.
    user_auth_session (optional): The user authentication session.

    Returns:

    Session: The new session.
    """
    log.debug(f"Starting session with {url}")

    web_driver.start_browser(user_auth_session=user_auth_session)
    web_driver.open_url(url)
    session = Session[InteractiveItemTypeT, PageTypeT](web_driver)
    return session
