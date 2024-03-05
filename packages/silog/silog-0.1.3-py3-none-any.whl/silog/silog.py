import logging
import os
from datetime import datetime

class Silog:
    _instance = None

    def __new__(cls, logPath="logs", level=logging.INFO, format="[%(asctime)s][%(levelname)s]%(message)s"):
        if cls._instance is None:
            cls._instance = super(Silog, cls).__new__(cls)
            cls._instance.__initLogger(logPath, level, format)
        return cls._instance

    def __initLogger(self, logPath, level, format):
        self.__logPath = logPath
        self.__level = level
        self.__format = format
        self.__logger = logging.getLogger('Silog')
        self.__updateLogFile()

    def __updateLogFile(self):
        currentDate = datetime.now().strftime('%Y-%m-%d')
        logFile = os.path.join(self.__logPath, f"{currentDate}.log")
        
        os.makedirs(os.path.dirname(logFile), exist_ok=True)

        handler = logging.FileHandler(logFile)
        formatter = logging.Formatter(self.__format)
        handler.setFormatter(formatter)

        if self.__logger.hasHandlers():
            self.__logger.handlers.clear()

        self.__logger.setLevel(self.__level)
        self.__logger.addHandler(handler)

    def __checkRefresh(self):
        currentLogFile = self.__logger.handlers[0].baseFilename
        currentDateInFile = os.path.basename(currentLogFile).split('.')[0]
        currentDate = datetime.now().strftime('%Y-%m-%d')
        
        if currentDateInFile != currentDate:
            self.__updateLogFile()

    def debug(self, message):
        self.__checkRefresh()
        self.__logger.debug(message)

    def info(self, message):
        self.__checkRefresh()
        self.__logger.info(message)

    def warning(self, message):
        self.__checkRefresh()
        self.__logger.warning(message)

    def error(self, message):
        self.__checkRefresh()
        self.__logger.error(message)

    def critical(self, message):
        self.__checkRefresh()
        self.__logger.critical(message)