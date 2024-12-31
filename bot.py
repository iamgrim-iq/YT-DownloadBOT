import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import time
from config import TOKEN, DOWNLOAD_PATH

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Создание папки для загрузок, если её нет
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

# Словарь для хранения выбранного формата для каждого пользователя
user_states = {}

def create_main_keyboard():
    """Создание основной инлайн клавиатуры"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🎥 Видео", callback_data="video"),
        InlineKeyboardButton("🎵 Аудио", callback_data="audio")
    )
    return keyboard

def create_video_formats_keyboard():
    """Создание клавиатуры форматов видео"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("MP4", callback_data="format_mp4"),
        InlineKeyboardButton("AVI", callback_data="format_avi"),
        InlineKeyboardButton("MOV", callback_data="format_mov")
    )
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
    return keyboard

def create_audio_formats_keyboard():
    """Создание клавиатуры форматов аудио"""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("MP3", callback_data="format_mp3"),
        InlineKeyboardButton("WAV", callback_data="format_wav")
    )
    keyboard.row(
        InlineKeyboardButton("AIFF", callback_data="format_aiff"),
        InlineKeyboardButton("OGG", callback_data="format_ogg")
    )
    keyboard.row(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
    return keyboard

def progress_bar(current, total):
    """Создание прогресс-бара"""
    progress = int(current * 10 / total)
    return "🟩" * progress + "⬜" * (10 - progress)

def progress_hook(d, message):
    """Хук для отслеживания прогресса загрузки"""
    if d['status'] == 'downloading':
        try:
            total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percentage = (downloaded / total) * 100
                progress = progress_bar(downloaded, total)
                bot.edit_message_text(
                    f"⏳ Загрузка...\n{progress} {percentage:.1f}%",
                    message.chat.id,
                    message.message_id
                )
        except Exception as e:
            print(f"Error in progress hook: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    welcome_text = ("👋 Привет! Я бот для скачивания видео с YouTube!\n\n"
                   "🎥 Я могу скачивать видео в разных форматах:\n"
                   "• MP4, AVI, MOV для видео\n"
                   "• MP3, WAV, AIFF, OGG для аудио\n\n"
                   "🎯 Выберите формат загрузки:")
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик callback-запросов"""
    if call.data == "video":
        bot.edit_message_text(
            "🎥 Выберите формат видео:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_video_formats_keyboard()
        )
    
    elif call.data == "audio":
        bot.edit_message_text(
            "🎵 Выберите формат аудио:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_audio_formats_keyboard()
        )
    
    elif call.data == "back_to_main":
        bot.edit_message_text(
            "🎯 Выберите формат загрузки:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=create_main_keyboard()
        )
    
    elif call.data.startswith("format_"):
        format_type = call.data.split("_")[1]
        user_states[call.message.chat.id] = format_type
        bot.edit_message_text(
            "🔗 Пожалуйста, отправьте ссылку на YouTube видео:",
            call.message.chat.id,
            call.message.message_id
        )

@bot.message_handler(func=lambda message: True)
def handle_url(message):
    """Обработчик URL"""
    if message.text.startswith(('https://youtube.com', 'https://www.youtube.com', 'https://youtu.be')):
        chat_id = message.chat.id
        if chat_id not in user_states:
            bot.reply_to(message, "❌ Пожалуйста, сначала выберите формат. Используйте /start")
            return

        format_type = user_states[chat_id]
        progress_message = bot.reply_to(message, "⏳ Начинаем загрузку...")

        try:
            output_template = os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s')
            
            # Настройка yt-dlp
            if format_type in ['mp4', 'avi', 'mov']:
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'progress_hooks': [lambda d: progress_hook(d, progress_message)],
                    'outtmpl': output_template,
                    'merge_output_format': format_type,
                }
            else:  # аудио форматы
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'progress_hooks': [lambda d: progress_hook(d, progress_message)],
                    'outtmpl': output_template,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format_type,
                        'preferredquality': '192',
                    }],
                }

            # Загрузка
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)
                
                # Получаем правильное имя файла
                if format_type in ['mp4', 'avi', 'mov']:
                    new_filename = os.path.splitext(filename)[0] + '.' + format_type
                else:
                    new_filename = os.path.splitext(filename)[0] + '.' + format_type
                
                # Проверяем существование файла
                if not os.path.exists(new_filename):
                    raise Exception(f"Файл {new_filename} не был создан")
                
                # Отправка файла
                with open(new_filename, 'rb') as file:
                    if format_type in ['mp4', 'avi', 'mov']:
                        bot.send_video(chat_id, file, caption="✅ Ваше видео готово!")
                    else:
                        bot.send_audio(chat_id, file, caption="✅ Ваше аудио готово!")
                
                # Удаление файла
                os.remove(new_filename)
                
                bot.edit_message_text(
                    "✅ Загрузка завершена!",
                    progress_message.chat.id,
                    progress_message.message_id
                )

        except Exception as e:
            bot.edit_message_text(
                f"❌ Произошла ошибка при загрузке: {str(e)}",
                progress_message.chat.id,
                progress_message.message_id
            )
            print(f"Error details: {e}")
            
    else:
        bot.reply_to(message, "❌ Пожалуйста, отправьте корректную ссылку на YouTube видео")

if __name__ == '__main__':
    bot.infinity_polling()