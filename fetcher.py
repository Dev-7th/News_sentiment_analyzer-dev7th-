import requests
from bs4 import BeautifulSoup
import analyzer
import pandas as pd  # importing pandas as pd
from datetime import date


class fetcher:
    def run(self):
        url = "https://www.bbc.com/"
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }

        response = requests.get(url, headers=header)
        status = response.status_code
        if (response.status_code == 200):
            print("successfully connect to the website!")
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            golden_container = soup.find_all(
                'div', attrs={'data-testid': 'anchor-inner-wrapper'})

            all_news_data = []
            for box in golden_container:

                headline_tag = box.find(
                    'h2', attrs={'data-testid': 'card-headline'})
                description_tag = box.find(
                    'p', attrs={'data-testid': 'card-description'})

                if headline_tag:
                    title = headline_tag.text.strip()

                    if description_tag:
                        desc = description_tag.text.strip()
                    else:
                        desc = "No description provided."

                    story = {
                        'headline': title,
                        'description': desc
                    }
                    all_news_data.append(story)

            brain = analyzer.NewsAnalyzer()
            all_news_data_sentiment = brain.sentiment_Func(all_news_data)

            df = pd.DataFrame(all_news_data_sentiment)
            df.to_csv(f'news_sentiment({date.today()}).csv', index=False)
        else:
            print(f"Failed. Status code: {response.status_code}")


if __name__ == "__main__":
    script = fetcher()
    script.run()
