# 📥 Insta & Shorts Bot

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot%20API-0088cc?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)

</div>

---

## 🇷🇺 Описание

**Telegram-бот**, который скачивает видео с **Instagram Reels** и **YouTube Shorts** по ссылке и отправляет их прямо в чат.

Просто отправь ссылку — бот возьмёт всё на себя.

### ✨ Возможности

- 📱 Скачивание **Instagram Reels** и **Instagram Posts** с видео
- 🎬 Скачивание **YouTube Shorts**
- ⚡ Асинхронная обработка — бот не зависает во время загрузки
- 🔄 Автоматическое обновление зависимостей каждые 12 часов
- 🐳 Полностью упакованы в **Docker** — одной командой запуска
- 💾 Временные файлы хранятся в RAM (`tmpfs`) — диск не засоряется

---

## 🇬🇧 Description

A **Telegram bot** that downloads videos from **Instagram Reels** and **YouTube Shorts** by link and sends them directly into the chat.

Just send a link — the bot handles the rest.

### ✨ Features

- 📱 Download **Instagram Reels** and video **Posts**
- 🎬 Download **YouTube Shorts**
- ⚡ Asynchronous processing — the bot stays responsive during downloads
- 🔄 Auto-upgrades key dependencies every 12 hours
- 🐳 Fully containerised with **Docker** — single-command deploy
- 💾 Temp files live in RAM (`tmpfs`) — no disk clutter

---

## 📁 Структура проекта / Project Structure

```
.
├── bot.py              # 🤖 Основной код бота / Main bot logic
├── Dockerfile          # 🐳 Образ контейнера / Container image
├── docker-compose.yml  # 📦 Оркестрация контейнеров / Container orchestration
├── entrypoint.sh       # 🚀 Точка входа контейнера / Container entry point
├── .env                # 🔐 Переменные окружения / Environment variables
└── .dockerignore       # 🚫 Исключения Docker-контекста / Docker build exclusions
```

---

## 🚀 Запуск / Getting Started

### 1. Предварительные требования / Prerequisites

| Инструмент | Версия |
|:----------:|:------:|
| Docker | latest |
| Docker Compose | v2+ |

### 2. Получить токен бота / Get a bot token

1. Открой Telegram и напиши [@BotFather](https://t.me/BotFather)
2. Создай бота командой `/newbot`
3. Скопи полученный **токен**

### 3. Настройка окружения / Configure environment

Создай файл `.env` (или редактируй существующий):

```env
TOKEN=your_telegram_bot_token_here
```

### 4. Старт / Launch

```bash
docker compose up -d --build
```

Бот запущен и готов к работе. Для просмотра логов:

```bash
docker compose logs -f
```

### 5. Остановка / Stop

```bash
docker compose down
```

---

## ⚙️ Как это работает / How It Works



1. Пользователь отправляет ссылку на Reels или Shorts
2. Бот определяет платформу и запускает загрузку в фоне
3. Видео скачивается и отправляется пользователю как файл
4. Временные данные автоматически очищаются

---

## 🛠️ Стек технологий / Tech Stack

| Технология | Назначение / Purpose |
|:----------:|:--------------------:|
| ![Python](https://img.shields.io/badge/-Python%203.12-3572A5?style=flat-square&logo=python&logoColor=white) | Основной язык |
| ![python-telegram-bot](https://img.shields.io/badge/-python--telegram--bot-0088cc?style=flat-square&logo=telegram&logoColor=white) | Telegram Bot API |
| ![yt-dlp](https://img.shields.io/badge/-yt--dlp-red?style=flat-square) | YouTube Shorts download |
| ![instaloader](https://img.shields.io/badge/-instaloader-E1306C?style=flat-square&logo=instagram&logoColor=white) | Instagram Reels download |
| ![FFmpeg](https://img.shields.io/badge/-FFmpeg-007db5?style=flat-square) | Video stream merging |
| ![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Контейнеризация |

---

## ⚠️ Примечания / Notes

- Загрузка контента зависит от внешних библиотек (`instaloader`, `yt-dlp`). Изменения API со стороны Instagram или YouTube могут временно нарушить работу.
- Downloading content depends on third-party libraries (`instaloader`, `yt-dlp`). Instagram or YouTube API changes may temporarily affect functionality.
- Токен бота — секретная информация. Не коммитьте `.env` в публичные репозитории.
- The bot token is sensitive. Never commit `.env` to public repositories.
