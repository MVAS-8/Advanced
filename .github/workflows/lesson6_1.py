import aiohttp
import asyncio
import sqlite3
import logging
from datetime import datetime

# Налаштування логування
logging.basicConfig(filename='aiohttp_scraping.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Підключення до бази даних
def create_db_connection():
    conn = sqlite3.connect('aiohttp_scraping.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraping_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            start_time DATETIME,
            end_time DATETIME,
            status_code INTEGER,
            duration REAL
        )
    ''')
    return conn, cursor

# Функція для логування в базу даних
def log_scraping_result(cursor, conn, url, start_time, end_time, status_code, duration):
    cursor.execute('''
        INSERT INTO scraping_logs 
        (url, start_time, end_time, status_code, duration) 
        VALUES (?, ?, ?, ?, ?)
    ''', (url, start_time, end_time, status_code, duration))
    conn.commit()

async def scrape_url(session, url, cursor, conn):
    try:
        start_time = datetime.now()
        logging.info(f"Початок запиту до {url}")
        
        # Логування початку запиту в базу даних
        cursor.execute('''
            INSERT INTO scraping_logs (url, start_time) 
            VALUES (?, ?)
        ''', (url, start_time))
        conn.commit()
        
        async with session.get(url) as response:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if response.status == 200:
                logging.info(f"Успішно отримано відповідь від {url}")
                
                # Оновлення запису в базі даних
                log_scraping_result(cursor, conn, url, start_time, end_time, 
                                    response.status, duration)
            else:
                logging.warning(f"Отримано статус {response.status} для {url}")
    
    except Exception as e:
        logging.error(f"Помилка при запиті до {url}: {e}")

async def scrape_urls(urls):
    conn, cursor = create_db_connection()
    
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_url(session, url, cursor, conn) for url in urls]
        await asyncio.gather(*tasks)
    
    conn.close()

# Тестові URLs
test_urls = [
    'https://www.python.org',
    'https://www.github.com',
    'https://www.stackoverflow.com'
]

# Запуск асинхронного скрапінгу
asyncio.run(scrape_urls(test_urls))