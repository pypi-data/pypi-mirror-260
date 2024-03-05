from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


class Button:
    def __init__(self) -> None:
        pass

    
    def add_button(self, button_text: str = None, **kwargs) -> KeyboardButton:

        """
        Create your button

        :param button_text: str, text on your button
        """
        return KeyboardButton(text=button_text, **kwargs)


    def add_markup(self,
                   keyboard: list = [], *,
                   resize_keyboard: bool = True,
                   one_time_keyboard: bool = False,
                   row_width: int = 3,
                   **kwargs) -> ReplyKeyboardMarkup:


        """
        Create keyboard for your message(s)

        :param keyboard: list, your keyboard, example: [[add_button('test'), add_button('test2')], [add_button('test3')]], default None
        :param resize_keyboard: bool, resize your keyboard, all window or beutiful, default True
        :param one_time_keyboard: bool, show keyboard ones or always, default False
        :param row_width: int, count buttons on row, default 3
        """

        return ReplyKeyboardMarkup(keyboard=keyboard,
                                   resize_keyboard=resize_keyboard,
                                   one_time_keyboard=one_time_keyboard,
                                   row_width=row_width, **kwargs)




    def add_inline_button(self,
                          button_text: str = 'test',
                          callback_data: str = 'test', *,
                          url: str = None,
                          **kwargs) -> InlineKeyboardButton:

        """
        Create your inline button

        :param button_text: str, text on your button, default 'test'
        :param url: str, url in your button, default None
        :param callback_data: str, callback for your button, default 'test'
        """
        return InlineKeyboardButton(text=button_text,
                                    url=url,
                                    callback_data=callback_data, **kwargs)


    def add_inline_markup(self,
                   keyboard: list = [],
                   row_width: int = 3,
                   **kwargs) -> InlineKeyboardMarkup:


        """
        Create keyboard for your message(s)

        :param keyboard: list, your keyboard, example: [[add_inline_button('test', callback_data='test'), add_inline_button('test2', callback_data='test2')], [add_inline_button('test3', callback_data='test3')]], default None
        :param row_width: int, count buttons on row, default 3
        """

        return InlineKeyboardMarkup(row_width=row_width,
                                    inline_keyboard=keyboard, **kwargs)