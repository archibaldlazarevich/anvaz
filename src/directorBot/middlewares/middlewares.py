import time

from aiogram import BaseMiddleware, Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update
from typing import Callable, Dict, Any, Awaitable


# class DirectorAccessMiddleware(BaseMiddleware):
#     def __init__(self, get_allowed_ids):
#         self.get_allowed_ids = get_allowed_ids
#
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any],
#     ) -> Any:
#         allowed_ids = await self.get_allowed_ids()
#         if event.from_user.id not in allowed_ids:
#             await event.answer("Доступ запрещён!!!")
#         else:
#             await handler(event, data)


class DirectorAccessMiddleware(BaseMiddleware):
    def __init__(self, get_allowed_ids: Callable[[], Awaitable[list[int]]]):
        self.get_allowed_ids = get_allowed_ids

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        allowed_ids = await self.get_allowed_ids()

        # Проверка доступа
        if event.from_user.id not in allowed_ids:
            await event.answer("Доступ запрещён!!!")
            return

        # Обработка команды /cancel
        state: FSMContext = data.get("state")
        state_data = await state.get_state()
        text = event.text or ""
        if text.startswith("/") and state_data is not None:
            await state.clear()
            dp: Dispatcher = data.get("dispatcher")
            bot: Bot = data.get("bot")
            update_id = data.get("update_id")
            if update_id is None:
                update_id = int(time.time() * 1000)

            update = Update(update_id=update_id, message=event)
            if dp:
                await dp.feed_update(bot=bot, update=update)
                return

        # Продолжаем обработку, если всё в порядке
        return await handler(event, data)
