# NaverDataScraping
Simple module to scrape the page https://datalab.naver.com/keyword/trendResult.naver

## Getting Started
Need Python 3.8 or greater\
Need Chrome 114

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
https://www.youtube.com/watch?v=IwGVWJoBZWw

### Metadata
All input parameter will be included as metadata along with downloaded file metadata to be put on S3\
unfortunately current boto3 doesn't support unicode string as metadata so I can't upload the metadata of the file (which is in Korean), temporarily solution is to do some translate to ascii string\
metadata of S3 file can have very good use in the later process: **Last modified** can be used to track update of the file when we use stream uploading the file, check the time lag between the job's end_time and the arrival_time of data file on S3, **ETag** used for versioning, ...
