# 🚀 AI Solana Token Watcher  

Этот AI-Агент **отслеживает новые токены на блокчейне Solana** и отправляет уведомления в Telegram, когда:  
✅ Капитализация **> $10M**  
✅ Объём торгов 24ч **> $50M**  

## **📌 Как установить и запустить?**  
### **1️⃣ Склонируйте репозиторий:**  
```bash
git clone https://github.com/ВАШ_АККАУНТ/solana-token-watcher.git
cd solana-token-watcher
2. Установите зависимости:pip install -r requirements.txt
3. Добавьте API-ключи в config.py:
SOLANA_API_URL = "https://api.dexscreener.com/latest/dex/tokens/solana"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
4. Запустите AI-Агента:python main.py

Если проект полезен, поставь ⭐