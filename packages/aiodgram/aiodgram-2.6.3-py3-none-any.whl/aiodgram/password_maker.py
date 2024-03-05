from random import randint, sample, choice
from .library import TgBot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

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
            pwd = ''
            difficulty = str(message.text())
            password_len = await state.get_data('password_len')

            match difficulty.lower():
                
                case 'easy':
                    for i in range(password_len):
                        if i % 2 == 0:
                            pwd += choice(letter_lower)
                        
                        if i % 3 == 0:
                            pwd += choice(letter_upper)
                        
                        if i % 5 == 0:
                            pwd += choice(special_chars)

                        if i % 7 == 0:
                            pwd += choice(numbers)

                case 'medium':
                    for i in range(password_len):
                        if i % 2 == 0:
                            pwd += choice(letter_lower)
                        
                        if i % 3 == 0:
                            pwd += choice(letter_upper)
                        
                        if i % 5 == 0:
                            pwd += choice(special_chars)

                        if i % 7 == 0:
                            pwd += choice(numbers)
                        
                        if i % 11 == 0 or i % 13 == 0:
                            pwd += choice(letter_lower) + choice(letter_upper) + choice(special_chars)
                    
                case 'hard':
                    for i in range(password_len):
                        if i % randint(2,4) == 0:

                            pwd += choice(letter_lower)
                        
                        if i % randint(3,5) == 0:

                            pwd += choice(letter_upper)
                        
                        if i % randint(4, 6) == 0:

                            pwd += choice(numbers)

                        if i % randint(5, 7) == 0:
                            pwd += choice(special_chars)
                        
                        if i % randint(11, 15) == 0:
                            pwd += choice(special_chars) + choice(letter_lower) + choice(letter_upper) + choice(numbers)


                case _:
                    await message.answer('You should only write: easy / medium / hard')
                

            if len(pwd) != 0:
                pwd  = sample(pwd, len(pwd))
                await message.answer(f"Your password: {pwd}")
            
            else:
                await message.answer("ERROR")