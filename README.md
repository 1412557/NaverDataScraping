# NaverDataScraping
Simple module to scrape the page https://datalab.naver.com/keyword/trendResult.naver

## Getting Started
Need Python 3.8 or greater

### Install required packages
``` pip install -r requirements.txt ```

### Provide the necessary parameters
Only keyword is needed, the others are all optional\
keywords: keys and sub-keys \
period: Period (1 month, 3 months, 1 year, entire) frequency: (month, year, day), date_range (start_date, end_date)\
device: (pc, mobile, entire)\
gender: (male, female, entire)\
age: entire or any of ('-12', '13-18', '19-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-')

### Run the main script
``` python main.py ```

### Check the downloaded data
folder files used as staging\
folder process will store the loaded and transformed data

### DEMO VIDEO
https://www.youtube.com/watch?v=HXMRO6JBMXI
