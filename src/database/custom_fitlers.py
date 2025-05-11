from aiogram.filters import Filter
from aiogram.types import Message

from src.database.data_func import get_all_dir_id


class IsDirector(Filter):
    async def __call__(self, message: Message) -> bool:
        allowed_ids = await get_all_dir_id()
        return message.from_user.id in allowed_ids
