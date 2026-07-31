import logging
import os
import traceback

class Logger():
    def __set_logger(self):
        log_directorio = "app/utils/logs"
        log_filename = "app.log"
        
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        log_path = os.path.join(log_directorio, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)
        
        if (logger.hasHandlers()):
            logger.handlers.clear()
            
        logger.addHandler(file_handler)
        
        return logger
    @classmethod
    def add_to_log(cls, level, message):
        try:
            logger = cls.__set_logger(cls)
            
            if (level == "critical"):  # Si el nivel es crítico
                logger.critical(message)  # Registra como crítico
            elif (level == "debug"):  # Si el nivel es debug
                logger.debug(message)  # Registra como debug
            elif (level == "error"):  # Si el nivel es error
                logger.error(message)  # Registra como error
            elif (level == "info"):  # Si el nivel es info
                logger.info(message)  # Registra como información
            elif (level == "warn"):  # Si el nivel es advertencia
                logger.warn(message)  # Registra como advertencia
        except Exception as ex:  # Si hay error al registrar
            print(traceback.format_exc())  
            print(ex)  
            
            
        