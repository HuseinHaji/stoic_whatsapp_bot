# 🧘 Stoic WhatsApp Bot

This project automatically sends **Stoic philosophy quotes** to your **WhatsApp** twice a day using the **Twilio WhatsApp API** and **GitHub Actions**.  
It’s simple, serverless, and designed to inspire calm reflection every morning and evening.

---

## Features
- Sends Stoic quotes directly to your WhatsApp twice a day (08:30 & 20:30 Europe/Berlin).
- Built with **Python + Twilio API**.
- Runs automatically via **GitHub Actions** (no server required).
- **No repeats** until the entire quote list is cycled.
- Logs state in `state.json` and keeps it synced in the repo.

---

## Tech Stack
- **Python 3.11**
- **Twilio WhatsApp Sandbox / API**
- **GitHub Actions (scheduled cron jobs)**
- **JSON state management**

---

## Setup Guide

### Fork or clone the repo
```bash
git clone https://github.com/HuseinHaji/stoic_whatsapp_bot.git
cd stoic_whatsapp_bot
