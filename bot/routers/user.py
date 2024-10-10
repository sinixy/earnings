from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import db


router = Router(name=__name__)

@router.message(CommandStart())
async def start(message: Message):
    db.create_user(user_id=message.from_user.id)
    await message.answer(f'Darova')