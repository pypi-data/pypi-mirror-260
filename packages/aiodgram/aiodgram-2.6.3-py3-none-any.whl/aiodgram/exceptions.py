from .addition.beautiful import MyMessages

class MyException:
    def __init__(self,
                 message: str = None,
                 *,
                 extra_info: any = None) -> None:
        
        """
        Create a your exception
        
        :param message: str, the message that you will output as an error, default None
        :param extra_info: str, additional information about the error that occurred, default None
        """
        
        self.message = message
        self.extra_info = extra_info

        MyMessages(clear=False, text='Произошла ошибка!', color='red')

        if self.extra_info != None:
            print(f'Additional information: {self.extra_info}')
        
        exit()


if __name__ == '__main__':
    print('test exceptions\n')
    MyException('test', extra_info='only test')
