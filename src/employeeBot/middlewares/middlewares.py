from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable


# class EmployeeAccessMiddleware(BaseMiddleware):
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

class EmployeeAccessMiddleware(BaseMiddleware):
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
            return  # Прекращаем дальнейшую обработку

        # Обработка команды /cancel
        state: FSMContext = data.get("state")
        text = event.text or ""
        if text.startswith("/") and state is not None:
            await state.clear()  # Сброс состояния
            await event.answer("Действие отменено.")
            return  # Прекращаем дальнейшую обработку

        # Продолжаем обработку, если всё в порядке
        return await handler(event, data)
