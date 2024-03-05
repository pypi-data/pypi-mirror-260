from ..main.library import TgBot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import secrets

class Context(StatesGroup):
    len_password = State()
    difficulty = State()

letter_lower = 'abcdefghijklmnopqrstuvwxyz'
letter_upper = letter_lower.upper()
numbers = '0123456789'
special_chars = "/,.'$#@!?()*&:;-_=+[]{}|<>"


class PasswordMaker:
    def __init__(self, 
                 bot: TgBot = None) -> None:
        
        self.bot = bot
        self.dispatcher = bot.dispatcher

    async def make(self,
                       user_id: int = None,
                       message: str = None):
        
        await self.bot.send_message(user_id=user_id, message=message)
        await Context.len_password.set()

        def _create_pwd(len, chars):
            return ''.join(secrets.choice(chars) for _ in range(len))

    
        @self.dispatcher.message_handler(state=Context.len_password)
        async def password(self, message: types.Message, state: FSMContext):
            try:
                password_len = int(message.text())
            
            except:
                await message.answer('INPUT A CORRECT NUMBER')
                state.finish()
            
            if password_len < 0:
                await message.answer("The password must be greater than 0")
            
            await state.update_data(password_len=password_len)
            
            await message.answer("Password difficulty")
            await Context.next()

        
        @self.dispatcher.message_handler(state=Context.difficulty)
        async def message_step2(self, message: types.Message, state: FSMContext):
            difficulty = str(message.text())
            password_len = await state.get_data('password_len')

            match difficulty.lower():
                
                case 'easy':
                    chars = ''.join(ascii_lowercase).join(ascii_uppercase)
                    pwd = _create_pwd(password_len, chars)

                case 'medium':
                    chars = ''.join(ascii_lowercase).join(ascii_uppercase).join(digits)
                    pwd = _create_pwd(password_len, chars)
                    
                case 'hard':
                    chars = ''.join(ascii_lowercase).join(ascii_uppercase).join(digits).join(punctuation)
                    pwd = _create_pwd(password_len, chars)


                case _:
                    await message.answer('You should only write: easy / medium / hard')
                

            if len(pwd) != 0:
                await message.answer(f"Your password: {pwd}")
            
            else:
                await message.answer("ERROR")