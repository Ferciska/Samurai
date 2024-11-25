import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random

# Логирование
logging.basicConfig(level=logging.INFO)

# Укажите токен вашего бота
API_TOKEN = "7952594519:AAGt2FyMf2oHACUNFbLkH-dgeXd1JF3UOFU"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Шутки для бота
jokes = [
    "Самурай заходит в бар... и бар превращается в додзё 🥋",
    "Почему самурай никогда не опаздывает? Потому что он режет время катаной! ⏳",
    "Самурай – это не профессия, это состояние души 🧘‍♂️",
    "- Над самураями, играющими в компьютерные игры, висит смертельная опасность.- Неужели? С чего вы это взяли, сэр?- Ну как же. По самурайским правилам, если самурай терпит поражение, он обязан сделать себе харакири.",
    "Месть - это блюдо, которое нужно подавать в тапки.(Из кодекса котов-самураев)",
    "Пиво " + 'Самурай' + "! Три бутылки вечером и на утро вас не отличишь от японца!",
    "Если опозорится японский самурай - он убьет себя.Если опозорится русский самурай - он убьет того, кто будет над ним смеяться.",
    "Самурай не носит зонт – дождь уважает его честь и обходит стороной.",
    "Даже чай в руках самурая заваривается быстрее – из страха перед катаной.",
    "Самурай никогда не забывает – у него память наточена!",
    "В интернет-спорах самурай режет аргументы пополам.",
    "Самурайский GPS всегда прокладывает путь через додзё.",
    "Самурай не проигрывает в шахматы – он рубит доску.",
    "У самурая нет будильника – он просыпается, как только солнце боится опоздать.",
    "Самурай не отпускает бороду – у катаны должна быть чистая работа.",
    "Если самурай садится за руль, то правила движения сами кланяются ему.",
    "Самурай не говорит дважды – его слово режет тишину напополам.",
]

# Подозрительные слова для модерации
ban_keywords = ["шлюха", "спам", "реклама", "порно", "бот"]

# --- Функционал ---

# Стартовая команда
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую, воин! 🥷\n"
        "Я самурайский бот и готов поддерживать порядок в чате.\n"
        "Введи /help, чтобы узнать, что я умею."
    )

# Список команд
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Вот что я могу:\n"
        "/start - Начать общение\n"
        "/joke - Рассказать самурайскую шутку\n"
        "/clean - Удалить спам\n"
        "/menu - Открыть меню действий"
    )

# Шутка
@dp.message(Command("joke"))
async def cmd_joke(message: Message):
    await message.answer(random.choice(jokes))

# Модерация сообщений
@dp.message(F.text)
async def filter_spam(message: Message):
    if any(word in message.text.lower() for word in ban_keywords):
        await message.delete()
        await message.answer(
            f"Сообщение от @{message.from_user.username} было удалено. 🛡️\n"
            "В чате запрещены подозрительные слова!"
        )

# Меню действий
@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Шутка", callback_data="joke")
    keyboard.button(text="Чистка", callback_data="clean")
    keyboard.adjust(2)
    await message.answer("Выбери действие:", reply_markup=keyboard.as_markup())

# Обработка нажатий на кнопки
@dp.callback_query(F.data == "joke")
async def callback_joke(callback: CallbackQuery):
    await callback.message.answer(random.choice(jokes))
    await callback.answer()

@dp.callback_query(F.data == "clean")
async def callback_clean(callback: CallbackQuery):
    await callback.message.answer("Чистота в чате обеспечена! 🧹")
    await callback.answer()

# --- Запуск ---

if __name__ == "__main__":
    dp.run_polling(bot)
