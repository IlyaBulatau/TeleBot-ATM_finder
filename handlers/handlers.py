from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command

from keyboards.keyboards import create_choice_bank_kb, create_get_location_user
from services.services import get_info_banks_for_city, is_valid_city
from database.database import users_db, in_user_db, save_coordinate_user

router = Router()

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    if not in_user_db(str(message.from_user.id)):
        users_db({message.from_user.id: {}})
    await message.answer(text=f'Привет, {message.from_user.first_name}\nдля дальнейшего взаимодействия со мной используй меню',
                          reply_markup=create_choice_bank_kb())
        

# @router.message(lambda msg: msg.location)
# async def get_location_user(message: Message):
#     lat = message.location.latitude
#     lon = message.location.longitude
#     save_coordinate_user(user_id=str(message.from_user.id), lat=lat, lon=lon)
#     await message.delete()
#     await message.answer(text='Выберите банк', reply_markup=create_choice_bank_kb())
    
@router.callback_query(Text(text='BelBank'))
async def get_info_belarus_bank(callback: CallbackQuery):
    answers = get_info_banks_for_city('Мачулищи')
    for answer in answers:
        await callback.message.answer(text=answer)