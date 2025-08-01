# 🎥 YouTube Downloader Bot

Telegram бот для скачивания видео и аудио с YouTube в различных форматах. Бот поддерживает загрузку с отображением прогресса и автоматической конвертацией в выбранный формат.

## ✨ Возможности

- 🎥 Загрузка видео в форматах:
  - MP4
  - AVI
  - MOV

- 🎵 Загрузка аудио в форматах:
  - MP3
  - WAV
  - AIFF
  - OGG

- 📊 Дополнительные функции:
  - Отображение прогресса загрузки
  - Интуитивный интерфейс с инлайн-кнопками
  - Автоматическое удаление файлов после отправки

## 🚀 Установка

### Предварительные требования

- Python 3.7 или выше
- FFmpeg
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))

### Установка FFmpeg

#### Windows
1. Скачайте FFmpeg с [официального GitHub репозитория](https://github.com/BtbN/FFmpeg-Builds/releases)
2. Распакуйте архив
3. Скопируйте содержимое папки `bin` в `C:\ffmpeg`
4. Добавьте `C:\ffmpeg` в переменную среды PATH

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Установка бота

1. Клонируйте репозиторий:
```bash
git clone https://github.com/iamgrim-iq/YT-DownloadBOT
cd yt-downloadbot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## 🚀 Запуск

```bash
python bot.py
```

## 📝 Использование

1. Запустите бота в Telegram командой `/start`
2. Выберите тип файла (видео/аудио)
3. Выберите формат файла
4. Отправьте ссылку на YouTube видео
5. Дождитесь загрузки и получите файл

## 📁 Структура проекта

```
youtube-downloader-bot/
│
├── bot.py           # Основной файл бота
├── config.py        # Конфигурация (токен и пути)
├── requirements.txt # Зависимости проекта
└── downloads/       # Папка для временных файлов
```

## 📚 Зависимости

- pyTelegramBotAPI==4.14.0
- yt-dlp==2023.12.30
- ffmpeg-python==0.2.0

## ⚠️ Важные замечания

- Убедитесь, что у бота есть права на отправку файлов в чат
- Проверьте наличие свободного места на диске
- Для больших файлов может потребоваться больше времени на обработку

## 📝 Лицензия

Этот проект распространяется под лицензией GNU GPL 3.0. Подробности в файле [LICENSE](LICENSE).

## 👥 Вклад в проект

Если вы хотите внести свой вклад в проект:

1. Сделайте форк репозитория
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## Автор
Бота написал firecoding
Tik-Tok: @firecoding
TG Channel: @codeapostol
