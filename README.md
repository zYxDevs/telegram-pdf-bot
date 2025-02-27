# Telegram PDF Bot

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/pdfbot)
[![MIT License](https://img.shields.io/github/license/zeshuaro/telegram-pdf-bot.svg)](https://github.com/zeshuaro/telegram-pdf-bot/blob/master/LICENSE)
[![GitHub Actions](https://github.com/zeshuaro/telegram-pdf-bot/actions/workflows/github-actions.yml/badge.svg)](https://github.com/zeshuaro/telegram-pdf-bot/actions/workflows/github-actions.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=telegram-pdf-bot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=telegram-pdf-bot)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=telegram-pdf-bot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=telegram-pdf-bot)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Crowdin](https://badges.crowdin.net/telegram-pdf-bot/localized.svg)](https://crowdin.com/project/telegram-pdf-bot)
[![Telegram Channel](https://img.shields.io/badge/Telegram-Channel-blue.svg)](https://t.me/pdf2botdev)
[![Mentioned in Awesome Telegram](https://awesome.re/mentioned-badge.svg)](https://github.com/ebertti/awesome-telegram)

[![Github-sponsors](https://img.shields.io/badge/sponsor-30363D?style=for-the-badge&logo=GitHub-Sponsors&logoColor=#EA4AAA)](https://github.com/sponsors/zeshuaro)
[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/zeshuaro)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/zeshuaro)
[![LiberaPay](https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black)](https://liberapay.com/zeshuaro/)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://patreon.com/zeshuaro)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/JoshuaTang)

A Telegram bot that can:

- Compress, crop, decrypt, encrypt, merge, preview, rename, rotate, scale and split PDF files
- Compare text differences between two PDF files
- Create PDF files from text messages
- Add watermark to PDF files
- Add text layers to PDF files to make them searchable with text
- Extract images and text from PDF files
- Convert PDF files into images
- Beautify handwritten notes images into PDF files
- Convert webpages and images into PDF files

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=4991e58bfd21&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Setup Database

The bot uses [Datastore](https://cloud.google.com/datastore) on Google Cloud Platform (GCP). Create a new project on GCP and enabble Datastore in the project. Install the [gcloud CLI](https://cloud.google.com/sdk/) and run `gcloud init` to initialise it with your project.

### OS Requirements

Ubuntu

```sh
apt-get install poppler-utils libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

macOS

```sh
brew install libxml2 libxslt poppler cairo pango gdk-pixbuf libffi
```

### Install dependencies

This project uses [Poetry](https://python-poetry.org/) as the dependency manager, run the following command to install the dependencies:

```sh
poetry install --no-root
```

### Compile the translation files

Run the following command to compile all the translation files:

```sh
pybabel compile -D pdf_bot -d locale/
```

### Setup Your Environment Variables

Copy the `.env` example file and edit the variables within the file:

```sh
cp .env.example .env
```

### Running The Bot

You can then start the bot with the following command:

```bash
python -m pdf_bot
```
