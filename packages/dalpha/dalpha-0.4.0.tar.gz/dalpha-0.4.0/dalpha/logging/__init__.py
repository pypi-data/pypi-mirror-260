import logging
import logging.config

from dalpha.logging.log_formatter import DalphaJsonFormatter

class DalphaLogger:
    def __init__(self, level=logging.INFO):
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(level)

        # Create formatter
        formatter = DalphaJsonFormatter(json_ensure_ascii=False)

        # Add formatter to handler
        consoleHandler.setFormatter(formatter)

        # Get the root logger
        self.logger = logging.getLogger('Dalpha')
        self.logger.setLevel(level)
        self.logger.addHandler(consoleHandler)

    def __make_extra(self, event, properties, data):
        return {
            "event": event,
            "properties": properties,
            "data": data
        }
    
    def info(self, message, event=None, properties={}, data={}):
        self.logger.info(
            message,
            extra = self.__make_extra(event, properties, data)
        )
    
    def error(self, message, event=None, properties={}, data={}):
        self.logger.error(
            message,
            extra = self.__make_extra(event, properties, data)
        )

    def warning(self, message, event=None, properties={}, data={}):
        self.logger.warning(
            message,
            extra = self.__make_extra(event, properties, data)
        )
    
    def debug(self, message, event=None, properties={}, data={}):
        self.logger.debug(
            message,
            extra = self.__make_extra(event, properties, data)
        )

logger = DalphaLogger()

