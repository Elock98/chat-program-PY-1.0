from asyncio.log import logger
import logging

class Logger:

    def __init__(self) -> None:
        LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"

        logging.basicConfig(filename = f".\log\chat_program.log", 
                            level=logging.DEBUG, # Change logging level
                            format=LOG_FORMAT,
                            filemode='a')

        self.__log = logging.getLogger()

    @property
    def log(self) -> logging.getLogger:
        """
            Access to logging object
        """
        return self.__log