import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from logging_config.logger_setup import print_log
import pandas as pd

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
            print_log('info', f'Запрос страницы: {url}')

            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 404:
                    print_log('warning', f'Страница не найдена (404): {url}')
                    break

                response.raise_for_status()

            except requests.RequestException as e:
                print_log('error', f'Ошибка запроса {url}: {e}')
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all('h3', class_='card-full-news__title')

            if not titles:
                print_log('warning', f'Страница существует, но новостей нет: {url}')
                break

            print_log(
                'info',
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

df = pd.DataFrame(data)
df.to_csv(r'C:\class_news\data\text_and_topic.csv', index=False, encoding='utf-8-sig')