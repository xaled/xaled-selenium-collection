from selenium import webdriver
import logging

logger = logging.getLogger(__name__)

def init_driver(json_server=False, headless=False, drivertype='firefox', driver_path=None, proxy=None):
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

    if json_server:
        pass # TODO: json_server
        # server = JsonServerSocket(socket_path, callback=server_callback)
        # server.bind()
        # print("binded to %s" % socket_path)
        # try:
        #     while True:
        #         try:
        #             print("waiting for connection")
        #             connection, client_address = server.accept()
        #             print("got connection")
        #             while connection.receive_call():
        #                 pass
        #         except KeyboardInterrupt:
        #             print("shutting down...")
        #             break
        #         except Exception as e:
        #             logger.error("Error in selenium server: %s" % (str(e)), exc_info=True)
        #             server.reconnect()
        #         finally:
        #             pass
        # finally:
        #     server.close()

    # driver.set_window_size(1366, 680)
    return driver