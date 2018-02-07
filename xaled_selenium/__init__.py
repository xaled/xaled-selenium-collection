from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

logger = logging.getLogger(__name__)

def init_driver(headless=False, drivertype='firefox', driver_path=None, proxy=None):
    global browser

    # Display
    if headless:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1280, 1280))
        # logger.info("starting display..")
        display.start()
        logger.info("Headless display started.")




    drivertype = drivertype.lower()
    if drivertype == "firefox":
        if driver_path is None:
            driver = webdriver.Firefox()
        else:
            driver = webdriver.Firefox(executable_path=driver_path)
        logger.info("Firefox driver started.")
    elif drivertype == "chrome":
        if driver_path is None:
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Chrome(driver_path)
        logger.info("Chrome driver started.")
    elif drivertype == "phantomjs":
        driver = webdriver.PhantomJS()
        logger.info("PhantomJS driver started.")
    else:
        raise Exception("Invalid Driver Type:" + drivertype)

    # driver.set_window_size(1366, 680)
    return driver

def firefox_proxy(proxy="127.0.0.1:8080", executable_path='./geckodriver'):
    proxy_dict = {
        'proxyType': 'MANUAL',
        'httpProxy': proxy,
        'ftpProxy': proxy,
        'sslProxy': proxy,
        'noProxy': []
    }
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['acceptInsecureCerts'] = True
    caps['proxy'] = proxy_dict
    driver = webdriver.Firefox(executable_path=executable_path, capabilities=caps)
    return driver