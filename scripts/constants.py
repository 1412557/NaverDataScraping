import os
DRIVER_PATH = '../utils/chromedriver.exe'
BASEURL = 'https://datalab.naver.com'
URL = 'https://datalab.naver.com/keyword/trendSearch.naver'
PERIOD_LIST = ['entire', '1 month', '3 months', '1 year']
AGE_LIST = ['-12', '13-18', '19-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-']
CURRENT_PATH = os.getcwd()
DOWNLOAD_FOLDER = CURRENT_PATH + '\\files'
PROCESS_FOLDER = CURRENT_PATH + '\\process'

S3_BUCKET_NAME = "my-naver-data-bucket"
REGION_NAME = ""
ACCESS_ID = "AKIA2QOQWV6UN3TODBPI"
ACCESS_KEY= "poSLBfDJj4IAEWNn/lgFCL+3F92yRUvf0t1dROzi"
