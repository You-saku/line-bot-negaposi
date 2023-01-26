import boto3
import config

AWS_DEFAULT_REGION = config.AWS_DEFAULT_REGION
LANGUAGE_CODE= "ja"

def detect_emotion(text):
    comprehend = boto3.client('comprehend', region_name=AWS_DEFAULT_REGION)
    response = comprehend.detect_sentiment(Text=text, LanguageCode=LANGUAGE_CODE)
    return response
