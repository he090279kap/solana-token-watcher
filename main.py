import requests
import schedule
import time
import logging
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Инициализация Telegram бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# API-адреса для мониторинга Solana, Ethereum, BSC
DEX_SCREENER_URLS = {
    "Solana": "https://api.dexscreener.com/latest/dex/tokens/solana",
    "Ethereum": "https://api.dexscreener.com/latest/dex/tokens/ethereum",
    "BSC": "https://api.dexscreener.com/latest/dex/tokens/bsc"
}

# Пороговые значения
MARKET_CAP_THRESHOLD = 10_000_000  # $10M
VOLUME_THRESHOLD = 50_000_000  # $50M

def get_tokens(network):
    """Получает список новых токенов для указанной сети."""
    url = DEX_SCREENER_URLS.get(network)
    if not url:
        logging.error(f"⚠ Сеть {network} не поддерживается.")
        return []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("pairs", [])
        else:
            logging.error(f"❌ Ошибка API ({network}): {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к API ({network}): {e}")
        return []

def check_tokens():
    """Проверяет новые токены во всех сетях и отправляет уведомления в Telegram."""
    for network in DEX_SCREENER_URLS.keys():
        logging.info(f"🔍 Проверяем токены в сети {network}...")
        tokens = get_tokens(network)

        for token in tokens:
            name = token.get("baseToken", {}).get("name", "Unknown")
            symbol = token.get("baseToken", {}).get("symbol", "???")
            market_cap = token.get("fdv", 0)  # Fully Diluted Valuation (аналог market_cap)
            volume_24h = token.get("volume", {}).get("h24", 0)
            token_address = token.get("pairAddress", "unknown")

            if market_cap >= MARKET_CAP_THRESHOLD and volume_24h >= VOLUME_THRESHOLD:
                message = (
                    f"🚀 Новый токен достиг лимитов ({network})!\n"
                    f"🔹 Название: {name} ({symbol})\n"
                    f"💰 Капитализация: ${market_cap:,.0f}\n"
                    f"📈 Объём торгов 24ч: ${volume_24h:,.0f}\n"
                    f"🔗 Подробнее: https://dexscreener.com/{network.lower()}/{token_address}"
                )
                send_telegram_alert(message)

def send_telegram_alert(message):
    """Отправляет уведомление в Telegram."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logging.info("📢 Уведомление отправлено!")
    except Exception as e:
        logging.error(f"❌ Ошибка отправки в Telegram: {e}")

# Запускаем проверку раз в 5 минут
schedule.every(5).minutes.do(check_tokens)

if __name__ == "__main__":
    logging.info("🎯 Запуск AI-Агента для мониторинга токенов Solana, Ethereum, BSC...")
    while True:
        schedule.run_pending()
        time.sleep(60)
