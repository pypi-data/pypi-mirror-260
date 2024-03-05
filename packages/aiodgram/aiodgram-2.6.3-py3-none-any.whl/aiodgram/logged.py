import logging
from datetime import datetime
from .exceptions import MyException

def print_message(type_message: str = None,
                  message: str = None):
    
    datetime_obj = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print(f'{datetime_obj} {type_message.upper()}: {message}')

class Logged:
    def __init__(self,
                 type_logging: str = 'info',
                 *,
                 filename: str = None) -> None:
        

        """
        Logging your project
        
        :param type_logging: str, the type of logging that you will do is minimal, default info
        :param filename: str, the name of the file that you want to use to output logs, default None
        """
        
        self.filename = filename

        match type_logging.upper():
            case 'ERROR':
                level = logging.ERROR
            case 'INFO':
                level = logging.INFO
            case 'WARNING':
                level = logging.WARNING
            case "CRITICAL":
                level = logging.CRITICAL
            case 'DEBUG':
                level = logging.DEBUG
            case _:
                MyException('Attribute Error', extra_info='Input a correct logging type!')
            

        logging.basicConfig(level=level, filename=self.filename, filemode='w', encoding='UTF-8',
                            format="%(asctime)s %(levelname)s: %(message)s",
                            datefmt='%d-%m-%Y %H:%M:%S')
    

    def critical(self,
                 message: str = 'CRITICAL ERROR'):
        
        """
        Show and write a critical error
        
        :param message: str, the message that you will output as a critical error, default 'CRITICAL ERROR'
        """
        
        logging.critical(message)

        match self.filename:
            case None:
                pass
            case _:
                print_message('critical', message)
    

    def info(self,
                 message: str = 'INFO'):
        
        """
        Show and write a info
        
        :param message: str, the message that you will output, default 'INFO'
        """
        
        logging.info(message)

        match self.filename:
            case None:
                pass
            case _:
                print_message('info', message)


    def error(self,
                 message: str = 'ERROR'):
        
        """
        Show and write a error
        
        :param message: str, the message that you will output as an error, default 'ERROR'
        """
        
        logging.error(message)

        match self.filename:
            case None:
                pass
            case _:
                print_message('error', message)


    def warning(self,
                 message: str = 'WARNING'):
        
        """
        Show and write a warning
        
        :param message: str, the message that you will output as a warning, default 'WARNING'
        """
        
        logging.warning(message)

        match self.filename:
            case None:
                pass
            case _:
                print_message('warning', message)
    

    def debug(self,
                 message: str = 'DEBUG'):
        
        """
        Show and write a debug
        
        :param message: str, the message that you will output as a debug, default 'DEBUG'
        """
        
        logging.debug(message)

        match self.filename:
            case None:
                pass
            case _:
                print_message('debug', message)


from .addition.beautiful import MyMessages
def log_errors(f):
    
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
    
        except Exception as e:
            MyMessages(text='Произошла ошибка!', color='red')
            Logged.error(e)
            raise e
        
    
    return inner


if __name__ == '__main__':
    print('testing\n')

    log = Logged()

    log.info('test')
    log.warning('test')
    log.error('test')
    log.critical('test')
    log.debug('test')