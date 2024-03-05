import asyncio

class Loading:

    def __init__(self,
                 bot) -> None:
        
        self.bot = bot

    async def animation_loading(self,
                                user_id: int = None,
                                percentages: int = 100) -> None:
        
        """
        Animate loading for your Telegram Bot

        :param user_id: int, User ID of the person to whom the message is being sent, default None
        :param percentages: int, count percentages, default 100
        """

        upload_message = await self.bot.send_message(chat_id=user_id, text="Начинаем загрузку...")
        await asyncio.sleep(1)
        download_str = '='
        for i in range(percentages+1):
            if i%11==0:
                download_str = download_str + '='
            await upload_message.edit_text(text=f"{download_str} {i}%")
            await asyncio.sleep(0.1)
        await upload_message.delete()