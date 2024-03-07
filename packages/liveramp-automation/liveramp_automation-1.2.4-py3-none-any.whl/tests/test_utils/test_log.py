from liveramp_automation.utils.log import Logger


def test_log_info():
    Logger.info("info")


def test_log_critical():
    Logger.critical("critical")


def test_log_error():
    Logger.error("Error")


def test_log_debug():
    Logger.debug("Debug")


def test_log_warning():
    Logger.warning("warning")
