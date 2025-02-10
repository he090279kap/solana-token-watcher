import requests
import schedule
import time
import logging
from telegram import Bot
from config import SOLANA_API_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_solana_tokens():
    """Получает список новых токенов Solana из API."""
    try:
        response = requests.get(SOLANA_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Ошибка API: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Ошибка подключения к API: {e}")
        return []

def check_tokens():
    """Проверяет новые токены на капитализацию и объём торгов."""
    tokens = get_solana_tokens()
    
    for token in tokens:
        name = token.get("name", "Unknown")
        symbol = token.get("symbol", "???")
        market_cap = token.get("market_cap", 0)
        volume_24h = token.get("volume_24h", 0)

        if market_cap >= 10_000_000 and volume_24h >= 50_000_000:
            message = (
                f"🚀 Новый токен достиг лимитов!\n"
                f"🔹 Название: {name} ({symbol})\n"
                f"💰 Капитализация: ${market_cap:,.0f}\n"
                f"📈 Объём торгов 24ч: ${volume_24h:,.0f}\n"
                f"🔗 Подробнее: https://solscan.io/token/{token.get('address')}"
            )
            send_telegram_alert(message)

def send_telegram_alert(message):
    """Отправляет уведомление в Telegram."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info("📢 Уведомление отправлено!")
    except Exception as e:
        logging.error(f"Ошибка отправки в Telegram: {e}")

# Запускаем проверку раз в 5 минут
schedule.every(5).minutes.do(check_tokens)

if __name__ == "__main__":
    logging.info("🎯 Запуск AI-Агента для мониторинга токенов Solana...")
    while True:
        schedule.run_pending()
        time.sleep(60)
