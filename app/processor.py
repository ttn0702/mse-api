# from utils.utils import SentimentAnalysisModel
from utils.utils import SentimentAnalysisModel 


def analyze_content(content):
    model = SentimentAnalysisModel(
        model_path='data/bi_lstm_model.h5',
        tokenizer_path='data/tokenizer.pickle',
        stopwords_path='data/vietnamese-stopwords-dash.txt'
    )
    predicted_labels = model.bilstm_predictive_model(content)
    return predicted_labels