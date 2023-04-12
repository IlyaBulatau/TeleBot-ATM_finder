from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Text, Command, StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import create_choice_bank_kb
from services.services import get_info_banks_for_city, is_valid_city, create_task, delete_image_file
from database.database import users_db, in_user_db

router = Router()

class FSMCitySelection(StatesGroup):
    city = State()

@router.message(Command(commands='start'), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    if not in_user_db(str(message.from_user.id)):
        users_db({message.from_user.id: {}})
    await message.answer(text=f'Привет, {message.from_user.first_name}\nдля дальнейшего взаимодействия со мной используй меню\nдля выбора населенного пункта отправь команду /place',
                          )
    
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Вы отменили действие, что бы сново начать поиск нажмите команду /place')
    await state.clear()

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_default_state(message: Message):
    await message.answer(text='Отменять нечего, для поиска выберите /place')
    
@router.message(Command(commands='place'), StateFilter(default_state))
async def procces_place_command(message: Message, state: FSMContext):
    await message.answer(text='Укажите населенный пункт')
    await state.set_state(FSMCitySelection.city)

@router.message(StateFilter(FSMCitySelection.city), lambda msg: is_valid_city(msg.text))
async def process_city_send(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer(text='Хорошо, теперь выберите Банк', reply_markup=create_choice_bank_kb())

@router.message(StateFilter(FSMCitySelection.city))
async def process_not_city(message: Message):
    await message.answer(text='Похоже такого города не существует\nлибо вы ввели населенный пункт не верно\n\nПожалуйста, попробуйте еще раз\n\nДля того что бы отменить поиск выберите команту /cancel')

    
@router.callback_query(Text(text='BelBank'))
async def get_info_belarus_bank(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    answers = get_info_banks_for_city(data['city'])
    
    for answer in answers:
        file = answer.split("\n\n")[1].replace(" ", "_").replace("/", "_")[8:]
        while True:
            try:
                photo=FSInputFile(f'{file}.jpg')
                await callback.message.answer_photo(photo=photo, caption=answer)
                delete_image_file(file=f'{file}.jpg')
                break
            except:
                continue
    state.clear()

@router.callback_query(Text(text='AlfaBank'))
async def process_get_info_alfa_bank(callback: CallbackQuery):
    await callback.answer(text='Ксожалению этот банк еще не поддерживается')

