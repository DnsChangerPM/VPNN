# استقرار روی VPS

۱. کاربر غیر-root بساز:

```bash
sudo useradd -m -s /bin/bash selfbot
sudo mkdir -p /opt/telethon-selfbot
sudo chown selfbot:selfbot /opt/telethon-selfbot
```

۲. پروژه را کپی کن و venv بساز:

```bash
sudo -u selfbot -H bash -lc '
cd /opt/telethon-selfbot
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
mkdir -p data logs
'
```

۳. `.env` را از `.env.example` بساز. فایل `*.session` را از ماشین لوکال (بعد از pairing) کپی کن.

۴. سرویس:

```bash
sudo cp deploy/selfbot.service /etc/systemd/system/telethon-selfbot.service
sudo systemctl daemon-reload
sudo systemctl enable --now telethon-selfbot
```

۵. لاگ:

```bash
journalctl -u telethon-selfbot -f
```

جایگزین: `docker compose up -d`
