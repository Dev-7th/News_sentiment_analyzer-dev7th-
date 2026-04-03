from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class NewsAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def sentiment_Func(self, all_news_data):
        for items in all_news_data:
            description = items['description'] if items['description'] != "No description provided." else ""
            full_text = f"{items['headline']}. {description}"
            sentiment_dict = self.vader.polarity_scores(full_text)

            if sentiment_dict['compound'] >= 0.05:
                overall_sentiment = "Postive"
            elif sentiment_dict['compound'] <= -0.05:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"

            items["sentiment"] = overall_sentiment

        return all_news_data
