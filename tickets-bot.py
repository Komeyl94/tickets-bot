# charter-tickets.py
import asyncio
import aiohttp
import logging
import random
import jdatetime
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from aiogram import Bot
from aiogram.exceptions import BotBlocked

# Constants for Bot
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Placeholder
CHAT_ID = "YOUR_CHAT_ID_HERE"  # Placeholder
DEPARTURE_CITY = "Tehran"
DESTINATION_CITY = "Istanbul"

# Request headers
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Path for logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Print logs to console
    ]
)

# Helper functions
def get_jalali_dates():
    """Returns a list of Jalali dates for today and the next 2 days."""
    today = jdatetime.date.today()
    return [today.strftime('%Y-%m-%d'), 
            (today + jdatetime.timedelta(days=1)).strftime('%Y-%m-%d'), 
            (today + jdatetime.timedelta(days=2)).strftime('%Y-%m-%d')]

async def send_telegram_message(message):
    """Sends a message to a Telegram chat."""
    try:
        async with Bot(token=BOT_TOKEN) as bot:
            await bot.send_message(CHAT_ID, message)
    except BotBlocked:
        pass  # Handle BotBlocked exception if necessary
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")
        await send_telegram_message(f"Error sending Telegram message: {e}")

async def fetch_page(session, url):
    """Fetches the page content asynchronously."""
    try:
        ua = UserAgent()
        HEADERS['User-Agent'] = ua.random
        async with session.get(url, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching page: {e}")
        await send_telegram_message(f"Error accessing website: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await send_telegram_message(f"Unexpected error: {e}")

async def scrape_website(html):
    """Scrapes the website for specific data (prices)."""
    soup = BeautifulSoup(html, "html.parser")
    data = []
    try:
        results = soup.select(".resu")[:3]
        if not results:
            logging.warning("No results found")
            await send_telegram_message("No results found")
            return "No results found"
        
        for idx, resu in enumerate(results, 1):
            price = resu.select_one(".price span").text.strip() if resu.select_one(".price span") else "N/A"
            flight_time = resu.select_one(".date").text.strip() if resu.select_one(".date") else "N/A"
            seats_available = resu.select_one(".user").text.strip() if resu.select_one(".user") else "N/A"
            formatted_info = (f"✈️Flight {idx}:\n"
                              f"💲Price: {price}\n"
                              f"⌚Flight Time: {flight_time}\n"
                              f"#️⃣Seats Available: {seats_available}\n")
            data.append(formatted_info)
        
        result_message = "\n".join(data)
        logging.info(result_message)
        await send_telegram_message(result_message)
        return result_message
    except Exception as e:
        logging.error(f"Error scraping website: {e}")
        await send_telegram_message(f"Error scraping website: {e}")
        return None

def build_url(departure, destination, date):
    return f"https://melicharter.com/Ticket-{departure}-{destination}.html?t={date}"

async def monitor_website():
    """Monitors a website at a specified interval."""
    async with aiohttp.ClientSession() as session:
        while True:
            dates = get_jalali_dates()
            all_results = []
            
            for jalali_date in dates:
                url = build_url(DEPARTURE_CITY, DESTINATION_CITY, jalali_date)
                try:
                    logging.info(f"Fetching data for date: {jalali_date}")
                    await send_telegram_message(f"Fetching data for date: {jalali_date}")
                    html = await fetch_page(session, url)
                    if html:
                        result = await scrape_website(html)
                        if result:
                            all_results.append(f"🗓️Date: {jalali_date}\n{result}")

                    delay_between_dates = random.uniform(10, 20)
                    logging.info(f"Waiting for {delay_between_dates:.2f} seconds before fetching data for {jalali_date}")
                    await send_telegram_message(f"Waiting for {delay_between_dates:.2f} seconds before fetching data for {jalali_date}")
                    await asyncio.sleep(delay_between_dates)  # 1-minute delay between each date

                except Exception as e:
                    logging.error(f"Error in monitoring loop: {e}")
                    await send_telegram_message(f"Error in monitoring loop: {e}")
            delay_between_checks = random.uniform(900, 1200)
            logging.info(f"Waiting for {delay_between_checks / 60:.2f} minutes before next check")
            await send_telegram_message(f"Waiting for {delay_between_checks / 60:.2f} minutes before the next check...")
            await asyncio.sleep(delay_between_checks)  # Random sleep between 20 and 30 minutes

async def main():
    logging.info("Starting to monitor flights for today and the next 2 days")
    await send_telegram_message("Starting to monitor flights for today and the next 2 days")
    await monitor_website()

if __name__ == "__main__":
    asyncio.run(main())
