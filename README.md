# VPNN — Self-Bot تلگرام + هلپر بات

یوزربات Telethon با پنل دکمه‌ای روی یک هلپر بات جدا. دو کلاینت در یک پروسه.

## ریسک

یوزربات نقض شرایط استفادهٔ تلگرام است و ممکن است به محدودیت یا بن اکانت منجر شود.
با شمارهٔ دوم شروع کن و `DRY_RUN=1` را روشن بگذار تا ارسال واقعی انجام نشود.

توکن هلپر بات مثل رمز است. هرکس توکن را داشته باشد می‌تواند بات را کنترل کند؛
به همین دلیل binding به `OWNER_ID` اجباری است.

## معماری

```
                 ┌─────────────────────────────┐
  Telegram ────► │ bot_client  (هلپر بات / UI) │
  CallbackQuery  │  InlineKeyboard فقط اینجا   │
                 └────────────┬────────────────┘
                              │ asyncio.Queue + SQLite jobs
                 ┌────────────▼────────────────┐
                 │ user_client (اکانت / کار)    │
                 │ ارسال، فوروارد، بن، بکاپ    │
                 └─────────────────────────────┘
```

یوزر اکانت نمی‌تواند `buttons` بفرستد و `CallbackQuery` نمی‌گیرد.
اگر دکمه داخل چت واقعی لازم شد فقط از inline mode هلپر بات
(`send_with_inline_buttons`) استفاده کن؛ پیام «via @YourBot» دیده می‌شود
و هلپر بات باید به آن چت دسترسی داشته باشد.

## راه‌اندازی

1. API_ID / API_HASH از https://my.telegram.org → API development tools
2. بات جدید از ‎@BotFather‎ با `/newbot` → `BOT_TOKEN`
3. Inline Mode: در BotFather دستور `/setinline` روی هلپر بات
4. `.env` از روی `.env.example`
5. `DRY_RUN=1 python main.py` روی سیستم خودت → لاگین شماره/کد/2FA → pairing:
   `/start` روی هلپر بات → کد ۶ رقمی را در Saved Messages بفرست
6. بعد از ساخت `*.session` آن‌ها را به VPS ببر و سرویس را enable کن

جزئیات VPS: `deploy/README.deploy.md`

## دستورات متنی مجاز

`/start` `/menu` `/cancel` `/help`

بقیهٔ کارها دکمه است. کلیک، همان پیام پنل را edit می‌کند.
