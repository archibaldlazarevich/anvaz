from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable


class AdminAccessMiddleware(BaseMiddleware):
    def __init__(self, get_allowed_ids):
        self.get_allowed_ids = get_allowed_ids

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        allowed_ids = await self.get_allowed_ids()
        print(allowed_ids)
        if event.from_user.id not in allowed_ids:
            await event.answer("Доступ запрещён!!!")
        else:
            await handler(event, data)
