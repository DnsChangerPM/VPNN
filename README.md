# NEON VOID // Hunters of the Rift

یک بازی سه‌بعدی browser-based با Babylon.js: با سفینه‌ی نئونی در میدان سیارکی پرواز کن، پهپادهای خلأ را نابود کن، کریستال‌ها را جمع کن و کمبو بساز.

## اجرا

```bash
npm install
npm run dev
```

برای نمایش خودکار دمو بدون ورودی دستی، آدرس را با `?demo` باز کن. کنترل‌ها: **WASD / Arrow Keys** برای حرکت، **Space یا کلیک** برای شلیک. روی موبایل دکمه‌های لمسی ظاهر می‌شوند.

## بررسی و build

```bash
npm run check
npm run build
npm run preview
```

## انتشار

Workflow موجود در `.github/workflows/deploy.yml` با هر push روی `main`، پروژه را build و به GitHub Pages منتشر می‌کند. در تنظیمات repository نیز باید در **Settings → Pages → Source** گزینه‌ی **GitHub Actions** فعال باشد.

## معماری

بازی کاملاً static است و به backend نیاز ندارد. `src/main.ts` پوسته‌ی DOM و HUD را مدیریت می‌کند و `src/game/scene.ts` منطق مستقل Babylon را نگه می‌دارد. برای جزئیات و تصمیم‌های هنری، `PLAN.md`، `STRUCTURE.md`، `ASSETS.md` و `MEMORY.md` را ببین.
