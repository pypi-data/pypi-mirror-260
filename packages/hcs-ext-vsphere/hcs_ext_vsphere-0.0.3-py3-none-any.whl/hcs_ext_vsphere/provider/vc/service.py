import logging
from . import govc

log = logging.getLogger(__name__)

_initialized = False


def init(config: dict, test_health: bool = True):
    global _initialized
    if _initialized:
        return

    govc.init(config)
    if test_health:
        govc.run("about", raise_on_failure=True)
    _initialized = True
