from bot_config import dp, bot
from aiogram import types
import random

player_status = True
total_candys = 150
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name} '
                                                      f'Привет, для того чтобы играть вводи количество конфет от 1 до 28, чтобы перезапустить игру введи /restart' )
@dp.message_handler(commands=['restart'])
async def restart(message: types.Message):
    global total_candys
    total_candys = 150
    await bot.send_message(message.from_user.id, text=f'Игра перезапущена {total_candys} конфет осталось')

async def check_win(message: types.Message):
    global total_candys
    global player_status
    if total_candys == 0:
        if player_status:
            await bot.send_message(message.from_user.id, text='Игрок проиграл')
        else:
            await bot.send_message(message.from_user.id, text='Игрок выйграл')


async def bot_turn(message: types.Message):
    global player_status
    global total_candys
    if total_candys > 28:
        take = random.randint(1,29)
    else:
        take = total_candys
    total_candys-=take
    await bot.send_message(message.from_user.id, text=f'Бот взял {take}'
                                                f' осталось {total_candys}')
    player_status = True
    if total_candys == 0: 
        await check_win(message)

async def player_to_turn(message: types.Message):
    global total_candys
    if total_candys > 0:
        await bot.send_message(message.from_user.id, text='Ход игрока')

@dp.message_handler()
async def player_turn(message: types.Message):
    global player_status
    global total_candys
    if message.text.isdigit():
        if 0<int(message.text)<29:
            if total_candys >= int(message.text):
                    total_candys-=int(message.text)
                    await bot.send_message(message.from_user.id, text=f'{message.from_user.first_name} взял {message.text}'
                                                            f' осталось {total_candys}')
                    player_status = False
                    if total_candys > 0: 
                        await bot_turn(message)
                        await player_to_turn(message)
                    else:
                        await check_win(message)
            else:
                await bot.send_message(message.from_user.id, text=f'Число больше остатка конфет')
        else:
            await bot.send_message(message.from_user.id, text=f'Введите корректное число')
    else:
        await bot.send_message(message.from_user.id, text=f'Введите число')
