from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database import *
from bot.filters.filters import RegisteredFilter
from bot.keyboards import get_keyboard

router = Router()

STUDENT_KB = get_keyboard(
    'Посмотреть свои результаты',
    'Добавить результат',
    placeholder='Выберите действие',
    sizes=(2, ),
)


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привет, я помогу тебе записать результаты твоих экзаменов',
        reply_markup=get_keyboard(
            'Зарегистрироваться',
            'Войти',
            'Выйти',
            placeholder='Выберите действие',
            sizes=(2, 2)
        ),
    )


@router.message(RegisteredFilter(), or_f(Command('login'), F.text.casefold() == 'войти'))
async def login_handler(message: types.Message, session: AsyncSession):
    student_id = message.from_user.id
    try:
        await message.answer('Вы авторизовались', reply_markup=STUDENT_KB)
        await login_query(session, student_id)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@router.message(RegisteredFilter(), F.text.casefold() == 'выйти')
async  def logout_handler(message: types.Message, session: AsyncSession):
    student_id = message.from_user.id
    try:
        await message.answer('Вы вышли')
        await logout_query(session, student_id)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@router.message(RegisteredFilter(), or_f(Command('view_scores'), F.text.casefold() == 'посмотреть свои результаты'))
async def view_scores_handler(message: types.Message, session: AsyncSession):
    student_id = message.from_user.id
    try:
        if RegisteredFilter():
            for result in await view_student_score_query(session, student_id):
                await message.answer(f"{result.title}: {result.score}")
        else:
            await message.answer('Вы не зарегистрированы')
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")



'''FSM для регистрации'''

class Registration(StatesGroup):
    name = State()
    surname = State()


@router.message(StateFilter(None),or_f(Command('register'), F.text.casefold() == 'зарегистрироваться'))
async def register_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите имя", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Registration.name)



@router.message(Registration.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    if len(message.text) >= 100:
        await message.answer(
            'Имя не должно превышать 100 символов. \n Введите заново'
        )
        return
    await state.update_data(id=message.from_user.id)
    await state.update_data(name=message.text)
    await message.answer('Введите фамилию')
    await state.set_state(Registration.surname)


@router.message(Registration.name)
async def add_name(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, внесите коректные данные")


@router.message(Registration.surname, F.text)
async def add_surname(message: types.Message, state: FSMContext, session: AsyncSession):
    if len(message.text) >= 100:
        await message.answer(
            'Фамилия не должна превышать 100 символов. \n Введите заново'
        )
        return
    await state.update_data(surname=message.text)
    data = await state.get_data()
    try:
        await register_query(session, data)
        await message.answer('Вы зарегистрированы!', reply_markup=STUDENT_KB)
        await state.clear()

    except Exception as e:
        await message.answer(str(e))
        await state.clear()


@router.message(Registration.surname)
async def add_surname(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, внесите коректные данные")


'''FSM для добавления результата'''

class AddScores(StatesGroup):
    title = State()
    score = State()


@router.message(RegisteredFilter(), StateFilter(None),or_f(Command('enter_scores'), F.text.casefold() == 'Добавить результат'))
async def add_score_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название предмета", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddScores.title)


@router.message(AddScores.title, F.text)
async def add_title(message: types.Message, state: FSMContext):
    if len(message.text) >= 100:
        await message.answer(
            'Название предмета не должно превышать 100 символов. \n Введите заново'
        )
        return
    await state.update_data(title=message.text)
    await message.answer('Введите результат')
    await state.set_state(AddScores.score)

@router.message(AddScores.title)
async def add_name(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, внесите коректные данные")


@router.message(AddScores.score, F.text)
async def add_score(message: types.Message, state: FSMContext, session: AsyncSession):
    student_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer('Результат должен быть числом')
        return
    await state.update_data(score=int(message.text))
    await state.update_data(student_id=student_id)
    data = await state.get_data()
    try:
        await add_score_query(session, data)
        await message.answer('Результат добавлен!')
        await state.clear()

    except Exception as e:
        await message.answer(str(e))
        await state.clear()

@router.message(AddScores.score)
async def add_score(message: types.Message):
    await message.answer("Вы ввели недопустимые данные, внесите коректные данные")