from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .beautiful import ColorStart
from .loading import Loading
from .exceptions import MyException



class TgBot:

    """
    Your Telegram Bot for sent messages, photo and video
    """

    def __init__(self,
                token: str = '', *,
                admin_username: str = '',
                parse_mode: bool = False,
                parse_mode_type: str = 'html',
                memory_storage: bool = False):
        """
        For settings, your Telegram Bot.
        
        :param token: str, token your TG Bot, from BotFather, default None.
        :param admin_username: str, username admin this bot, default None
        :param parse_mode: bool, enable or disable parse_mode, default True
        :param parse_mode_type: str, HTML or MARKDOWN, default HTML
        :param memory_storage: bool, enable or disable memoryStorage, default False
        """
        
        self.token = token
        self.executor = executor
        self.admin_username = admin_username

        match parse_mode:
            case True:

                match parse_mode_type.upper():
                    case 'HTML':
                        self.bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
                    case 'MARKDOWN':
                        self.bot = Bot(token=token, parse_mode=types.ParseMode.MARKDOWN)
                    case _:
                        MyException('AttributeError', extra_info="You must input 'html' or 'markdown' !")



            case _:
                self.bot = Bot(token=token)


        match memory_storage:
            case True:
                self.dispatcher = Dispatcher(self.bot, storage=MemoryStorage())

            case _:
                self.dispatcher = Dispatcher(self.bot)
        
        
    async def send_message(self,
                       chat_id: int,
                       message: str,
                       reply_markup = None
                       ) -> None:
        """
        For sent message from your bot.

        :param chat_id: chat ID user who used bot
        :param message: your message
        :param reply_markup: your markup for message, default None

        :return None
        """

        await self.bot.send_message(chat_id=chat_id,
                                    text=message,
                                    reply_markup=reply_markup)



    async def send_photo(self,
                         chat_id: int,
                         photo: str,
                         caption: str = None,
                         reply_markup = None) -> None:
        """
        For sent photo from your bot.

        :param chat_id: chat id user who used bot
        :param photo: your photoed
        :param caption: text under photo in this message, default None
        :param reply_markup: your markup for message, default None

        :return None
        """

        await self.bot.send_photo(chat_id=chat_id,
                                  photo=photo,
                                  caption=caption,
                                  reply_markup=reply_markup)



    async def send_video(self,
                        chat_id: int,
                        video: str, *,
                        caption: str = None,
                        reply_markup = None) -> None:

        """
        For send video.
        
        :param chat_id: int, chat ID user who used bot
        :param video: str, link for video
        :param caption: str, text under video in this message, default None
        :param reply_markup: your markup for message, default None

        :return None
        """
        
        await self.bot.send_video(chat_id=chat_id,
                                    video=open(f'{video}.mp4', 'rb'),
                                    caption=caption,
                                    reply_markup=reply_markup)
    


    async def loading(self,
                      chat_id: int,
                      percentages: int = 100):
        
        """
        Animate loading for your Telegram Bot

        :param chat_id: int, Chat ID of the person to whom the message is being sent, default None
        :param percentages: int, count percentages, default 100

        :return loading animate
        """

        load = Loading(self.bot)
        await load.animation_loading(user_id=chat_id, percentages=percentages)




#----------------------------------------------------------------------------------

    async def on_startup(self, dp: Dispatcher):

        await ColorStart(self.dispatcher, self.admin_username).on_startup()


    async def on_shutdown(self, dp: Dispatcher):

        await ColorStart().on_shutdown()



    def start_polling(self, *,
                      dispatcher = None,
                      skip_updates = True,
                      on_startup = None,
                      on_shutdown = None) -> None:

        """
        For start your Telegram Bot.
        
        :param dispatcher: Dispatcher, default None
        :param skip_updates: False or True, default True
        :param on_startup: your define for startup, use your define, default None
        :param on_shutdown: your define for shutdown, use your define, default None

        :return None
        """

        if on_startup == None:
            on_startup = self.on_startup

        if on_shutdown == None:
            on_shutdown = self.on_shutdown
        
        if dispatcher == None:
            dispatcher = self.dispatcher

        self.executor.start_polling(dispatcher=dispatcher,
                                    skip_updates=skip_updates,
                                    on_startup=on_startup,
                                    on_shutdown=on_shutdown)

#----------------------------------------------------------------------------------