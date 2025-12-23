import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from app.logging_config.logger_setup import get_logger

logger = get_logger("parser")

BASE_DIR = Path(__file__).resolve().parents[2]  
OUTPUT_CSV = BASE_DIR / "data" / "text_and_topic.csv"
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)  

RUBRICS = {
    "sport": "sport",
    "economics": "economics",
    "science": "science",
}

data = []

start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 3, 5)
current_date = start_date

while current_date <= end_date:
    for topic, rubric in RUBRICS.items():
        page = 1

        while True:
            url = current_date.strftime(
                f'https://lenta.ru/rubrics/{rubric}/%Y/%m/%d/page/{page}/'
            )
            logger.info(f'Запрос страницы: {url}')

            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 404:
                    logger.warning(f'Страница не найдена (404): {url}')
                    break

                response.raise_for_status()

            except requests.RequestException as e:
                logger.error(f'Ошибка запроса {url}: {e}')
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('h3', class_='card-full-news__title')

            if not titles:
                logger.warning(f'Страница существует, но новостей нет: {url}')
                break

            logger.info(
                f'Страница успешно спарсена: {url} | '
                f'Новостей: {len(titles)} | Тема: {topic}'
            )

            for el in titles:
                data.append({
                    "text": el.get_text(strip=True),
                    "topic": topic
                })

            page += 1

    current_date += timedelta(days=1)

# Сохраняем CSV
df = pd.DataFrame(data)
df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
logger.info(f'CSV сохранен по пути: {OUTPUT_CSV}')