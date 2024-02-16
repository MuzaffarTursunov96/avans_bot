import asyncio
from typing import Optional
import aiogram
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from keyboard import *
from string import ascii_letters
import aiohttp
import os 
import string
import random
import requests as rq


from aiohttp import web

API_TOKEN = ''

loop = asyncio.get_event_loop()

bot = Bot(token=API_TOKEN, loop=loop)





webhook_path = f'/{API_TOKEN}'

base_url ='https://oylikavans.uz'
local_url =''


websocket_connection = None
# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
app = web.Application()


STATES = {
    'START': 'start',
    'MENU': 'menu',
    'OY': 'oy',
    'COPY': 'copy',
    'AVANS': 'avans',
    'FINISH':'finish',
    'END':'end',
    'START_ADMIN':'start_admin',
    'ROYXAT':'royxat',
    'DELETE':'delete',

    ######################
    'USER_ID':'user_id',
    'USERNAME':'username',
    'USER_SAVE':'user_save',


    ###################
    'XABAR_START':'xabar_start',
    'YUBORISH':'yuborish'
}

user_states = {}
      



async def set_webhook():
    webhhok_uri =f'{base_url}{webhook_path}'
    await bot.set_webhook(
        webhhok_uri
    )
    

async def on_startup(_):
    await set_webhook()

admin_id =85697512
#85697512


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global admin_id
    if message.from_user.id == admin_id:
        user_states[message.chat.id] = STATES['START_ADMIN']
        return await bot.send_message(text='<em>Assalomu alaykum hushkelibsiz!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML')
    user_ids = await get_user_ids()
    if message.from_user.id in [int(user['user_id']) for user in user_ids]:
        user_states[message.chat.id] = STATES['MENU']
        return await bot.send_message(text='<em>Assalomu alaykum bizning <b>avans botga</b> xush kelibsiz.\n </em>',chat_id=message.chat.id,reply_markup=avans_markup,parse_mode='HTML')
    else:
        return await bot.send_message(text='<em>Iltimos royxatdan o\'tish uchun Adminga muroajat qiling!\ntel:+998 93 533 99 07</em>',chat_id=message.chat.id,parse_mode='HTML')
    
async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    if token == API_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)



def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # Includes uppercase letters, lowercase letters, and digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string
avans_list ={}

user_idd ={}
user_name ={}
admin_message =''
foydalanuvchi_idsi =''
@dp.message_handler()
async def user_start(message: types.Message):
    
    state = user_states.get(message.chat.id)

    global avans_list
    global user_idd
    global user_name
    global admin_message
    print(state)
    
    oylar =['Yanvar','Fevral','Mart','Aprel','May','Iyun','Iyul','Avgust','Sentyabr','Oktyabr','Noyabr','Dekabr']

    if state == None:
        await bot.send_message(text='<em>Iltimos start buyrug\'ini bosing</em>',chat_id=message.chat.id,reply_markup=start_markup,parse_mode='HTML')

    elif state == STATES['MENU']:
        if message.text =='💰 Avans miqdorini kiritish':
            user_states[message.chat.id] = STATES['OY']
            await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan oyni tanlang.</em>',chat_id=message.chat.id,reply_markup=oylar_markup,parse_mode='HTML')
        elif message.text =='🔄 Avans miqdorini o\'zgartirish':
            user_states[message.chat.id] = STATES['AVANS']
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos avans miqdorini kiriting\nMisol : 2550000</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Iltimos menudagi ro\'yxatdan buyruqni tanlang.</em>',chat_id=message.chat.id,reply_markup=avans_markup,parse_mode='HTML')

    elif state == STATES['OY']:
        if message.text in oylar:
            user_states[message.chat.id] = STATES['AVANS']
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos avans miqdorini kiriting\nMisol : 2500000</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Iltimos pastdagi ro\'yxatdan oyni tanlang.</em>',chat_id=message.chat.id,reply_markup=oylar_markup,parse_mode='HTML')

    elif state == STATES['AVANS']:
        try:
            avans = int(message.text)
            user_states[message.chat.id] = STATES['FINISH']
            
            avans_list[message.from_user.id] =avans
            await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=buyurtma_markup,parse_mode='HTML')
        except:
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos avans miqdorini tog\'ri formatda kiriting!\nMisol : 1500000 </em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
    elif state ==STATES['FINISH']:
        if message.text =='📠 Yuborish':
            user_states[message.chat.id] = STATES['MENU']
            if message.from_user.id in avans_list:
                data ={
                    'user_id':message.from_user.id,
                    'chat_id':message.chat.id,
                    'avans':avans_list[message.from_user.id],
                    'name':message.from_user.first_name
                }
                await user_avans_save(data)
                del avans_list[message.from_user.id]
                await bot.send_message(text='<em>Arizangiz qabul qilindi, yordam berganimizdan mamnunmiz.</em>',chat_id=message.chat.id,reply_markup=avans_markup,parse_mode='HTML')
            else:
                user_states[message.chat.id] = STATES['AVANS']
                remove_markup = ReplyKeyboardRemove()
                return await bot.send_message(text='<em>Iltimos avans miqdorini boshidan kiriting!</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
            
            
        elif message.text =='⬅️ Orqaga':
            user_states[message.chat.id] = STATES['AVANS']
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos avans miqdorini kiriting</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=buyurtma_markup,parse_mode='HTML')
            
    elif state == STATES['END']:
        user_states[message.chat.id] = STATES['MENU']
        await bot.send_message(text='<em>Arizangiz qabul qilindi, yordam berganimizdan mamnunmiz.</em>',chat_id=message.chat.id,reply_markup=avans_markup,parse_mode='HTML')
    
    ###########admin#############
    if  state == STATES['START_ADMIN'] and message.from_user.id == admin_id:
        if message.text =='🤵‍♂️ Foydalanuvchilar ro\'yxati':
            user_states[message.chat.id] = STATES['ROYXAT']
            users_list = await get_users()
            await bot.send_message(text='<em>Foydalanuvchini tanlang.</em>',chat_id=message.chat.id,reply_markup=get_users_markup(users=users_list),parse_mode='HTML')
        elif message.text =='💾 Excell fileni yuklash':
            excel_file_path = await get_excelfile_path()
            print(excel_file_path)
            if os.path.exists(excel_file_path):
                with open(excel_file_path, 'rb') as file:
                    await bot.send_document(message.chat.id, file)
            else:
                await message.reply("Excel file topilmadi")

        elif message.text =='➕ Yangi foydalanuvchi qo\'shish':
            user_states[message.chat.id] = STATES['USER_ID']
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>🆔 Foydalanuvchi idsini kiriting</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
        elif message.text =='✉️ Xabar yuborish':
            user_states[message.chat.id] = STATES['XABAR_START']
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos yubormoqchi bo\'lgan xabaringizni kiriting.</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML')
    elif state == STATES['ROYXAT']:
        global foydalanuvchi_idsi
        foydalanuvchi_idsi = message.text
        user_states[message.chat.id] = STATES['DELETE']
        users_list = await get_users()
        users_option =[option['name'] + '__' + str(option['user_id']) for option in users_list]
        if message.text in users_option:
            await bot.send_message(text='<em>Iltimos buyruqni tanlang.</em>',chat_id=message.chat.id,reply_markup=user_detail_mamrkup,parse_mode='HTML')
        elif message.text =="🏠 Uyga qaytish":
            user_states[message.chat.id] = STATES['START_ADMIN']
            await bot.send_message(text='<em>Iltimos menudagi buyruqlardan tanlang!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Foydalanuvchini tanlang.</em>',chat_id=message.chat.id,reply_markup=get_users_markup(users=users_list),parse_mode='HTML')
    
    elif state == STATES['DELETE']:
        
        if message.text =='🗑 Foydalanuvchini o\'chirish':
            data ={
                'user_id':foydalanuvchi_idsi.split('__')[1]
            }
            await delete_user(data=data)
            users_list = await get_users()
            await bot.send_message(text='<em>Foydalanuvchilar ro\'yxati.</em>',chat_id=message.chat.id,reply_markup=get_users_markup(users=users_list),parse_mode='HTML')
        elif message.text =="🏠 Uyga qaytish":
            user_states[message.chat.id] = STATES['START_ADMIN']
            await bot.send_message(text='<em>Iltimos menudagi buyruqlardan tanlang!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML')
        else:
            await bot.send_message(text='<em>Iltimos buyruqni tanlang.</em>',chat_id=message.chat.id,reply_markup=user_detail_mamrkup,parse_mode='HTML')
    ########user_save#####
    elif state == STATES['USER_ID']:
        try:
            user_id = int(message.text)
            user_states[message.chat.id] = STATES['USERNAME']
            user_idd[message.chat.id] = user_id
            await bot.send_message(text='<em>Iltimos foydalanuchi (F.I.O)sini kiriting</em>',chat_id=message.chat.id,parse_mode='HTML')
        except:
            remove_markup = ReplyKeyboardRemove()
            await bot.send_message(text='<em>Iltimos foydalanuvchi 🆔 sini tog\'ri formatda kiriting!</em>',chat_id=message.chat.id,reply_markup=remove_markup,parse_mode='HTML')
    elif state == STATES['USERNAME']:
        user_states[message.chat.id] = STATES['USER_SAVE']
        user_name[message.chat.id] = message.text
        await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=user_save_mamrkup,parse_mode='HTML')
    elif state == STATES['USER_SAVE']:
        user_states[message.chat.id] = STATES['ROYXAT']
        if message.text =='💿 Foydalanuvchini saqlash':
            data ={
                'user_id':user_idd[message.chat.id],
                'name':user_name[message.chat.id],
                'chat_id':message.chat.id
            }
            await create_user(data=data)
            del user_idd[message.chat.id]
            del user_name[message.chat.id]
            users_list = await get_users()
            print(users_list)
            await bot.send_message(text='<em>Foydalanuvchilar ro\'yxati.</em>',chat_id=message.chat.id,reply_markup=get_users_markup(users=users_list),parse_mode='HTML')
        elif message.text =="🏠 Uyga qaytish":
            user_states[message.chat.id] = STATES['START_ADMIN']
            await bot.send_message(text='<em>Iltimos menudagi buyruqlardan tanlang!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML') 
    
    elif state == STATES['XABAR_START']:
        admin_message = message.text
        user_states[message.chat.id] = STATES['YUBORISH']
        await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=xabar_mamrkup,parse_mode='HTML')
    
    elif state == STATES['YUBORISH']:
        if message.text =="📤 Yuborish":
            message_users = await get_users_for_message()
            print('users>>',message_users)
            for message_user in message_users:
                await bot.send_message(text=f'<em>{admin_message}</em>',chat_id=message_user['chat_id'],reply_markup=avans_markup,parse_mode='HTML') 
            user_states[message.chat.id] = STATES['START_ADMIN']
            await bot.send_message(text='<em>Xabar jonatildi!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML')
        elif message.text =='🏠 Uyga qaytish':
            user_states[message.chat.id] = STATES['START_ADMIN']
            await bot.send_message(text='<em>Iltimos menudagi buyruqlardan tanlang!</em>',chat_id=message.chat.id,reply_markup=admin_menu,parse_mode='HTML') 
        else:
            await bot.send_message(text='<em>Iltimos buyruqni tanlang</em>',chat_id=message.chat.id,reply_markup=xabar_mamrkup,parse_mode='HTML') 






async def create_user(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/user-create',data=data) as response:
            data = await response.json()
    return data

async def delete_user(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/user-delete',data=data) as response:
            data = await response.json()
    return data


async def user_avans_save(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/user-avans-save',data=data) as response:
            data = await response.json()
    return data

async def user_avans_check(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(local_url+'/api/v1/user-avans-check',data=data) as response:
            data = await response.json()
    return data


async def get_users():
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/user-list') as response:
            data = await response.json()
    return data

async def get_excelfile_path():
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/get-path-excell') as response:
            data = await response.json()
    return data['path']

async def get_users_for_message():
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/get-users-for-message') as response:
            data = await response.json()
    return data

async def get_user_ids():
    async with aiohttp.ClientSession() as session:
        async with session.get(local_url+'/api/v1/get-user-ids') as response:
            data = await response.json()
    return data




def get_users_markup(users)->ReplyKeyboardMarkup:
    users_option =[str(option['name']) + '__' + str(option['user_id']) for option in users]
    buttons3 = [types.KeyboardButton(option) for option in users_option]
    users_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
        types.KeyboardButton('🏠 Uyga qaytish')
    ).add(
    *buttons3 
    )
    return users_markup




app.router.add_post(f'/{API_TOKEN}',handle_webhook)


if __name__ == '__main__':
    # app.on_startup.append(on_startup)

    # web.run_app(
    #     app,
    #     host='0.0.0.0',
    #     port=8080
    # )

    executor.start_polling(dp, loop=loop, skip_updates=True)
