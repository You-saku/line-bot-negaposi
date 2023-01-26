# 環境変数
import os
from dotenv import load_dotenv
load_dotenv(override=True)

AWS_DEFAULT_REGION=os.getenv('AWS_DEFAULT_REGION')
YOUR_CHANNEL_ACCESS_TOKEN=os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
YOUR_CHANNEL_SECRET=os.getenv('YOUR_CHANNEL_SECRET')
