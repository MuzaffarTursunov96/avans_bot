from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from main_bot import dp,bot
from aiogram import types
from datetime import datetime






button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')

markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

markup4 = ReplyKeyboardMarkup().row(
    button1, button2, button3
)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)


lang_markup =ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(
    KeyboardButton('🇺🇿 Uz'),
    KeyboardButton('🇷🇺 Ru'),
    # KeyboardButton('Eng')  
)
start_markup =ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(
    KeyboardButton('/start'), 
)

avans_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('💰 Avans miqdorini kiritish'),KeyboardButton('🔄 Avans miqdorini o\'zgartirish')
)
menu_markup2 = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('🔄 Tilni o\'zgartirish'),
)
options =['🏛 Uyga qaytish','AAAAA','BBBBBB','CCCCCCCC','DDDDDDD']

buttons = [types.KeyboardButton(option) for option in options]

dorilar_markup = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
  *buttons 
)



buyurtma_markup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    KeyboardButton('📠 Yuborish'),
    KeyboardButton('⬅️ Orqaga'),
)
month = datetime.now().month

oylar =['Yanvar','Fevral','Mart','Aprel','May','Iyun','Iyul','Avgust','Sentyabr','Oktyabr','Noyabr','Dekabr']


oylar_buttons = [types.KeyboardButton(option) for option in oylar[month-1:]]
    


oylar_markup =ReplyKeyboardMarkup(row_width=1,resize_keyboard=True).add(
  *oylar_buttons 
)


admin_menu = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    types.KeyboardButton('🤵‍♂️ Foydalanuvchilar ro\'yxati'),types.KeyboardButton('➕ Yangi foydalanuvchi qo\'shish')
).add(
    types.KeyboardButton('💾 Excell fileni yuklash'),types.KeyboardButton('✉️ Xabar yuborish')
)

user_detail_mamrkup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    types.KeyboardButton('🗑 Foydalanuvchini o\'chirish'),types.KeyboardButton('🏠 Uyga qaytish')
)
user_save_mamrkup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    types.KeyboardButton('💿 Foydalanuvchini saqlash'),types.KeyboardButton('🏠 Uyga qaytish')
)

xabar_mamrkup = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(
    types.KeyboardButton('📤 Yuborish'),types.KeyboardButton('🏠 Uyga qaytish')
)










