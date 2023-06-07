from scripts.naverscraping import NaverScraping
from scripts import constants
from scripts.transforming import ETLProcess
from helpers.helper import clean_up_repo
import sys


def main():
    try:
        logging.info("Main() started")
        # Setting up arguments
        keyword = { # Must have keyword
            "Computer": "Apple, Microsoft",
            "Cosmetic": "YSL",
            "Football": "Liverpool",
            "War": "Russia"
        }
        period = { # valid option include [1 month, 3 months, 1 year, entire]
            'period': '1 year',
            'frequency': 'month',
            'date_range': ['2019/04/19', '2021/12/23']
        }
        device = 'pc'
        gender = 'female'
        age = ['-12', '60-'] # age can be entire to select all, check option in AGE_LIST

        # Clean up folders everytime we start scraping,
        clean_up_repo(constants.DOWNLOAD_FOLDER)
        clean_up_repo(constants.PROCESS_FOLDER)

        # Start scraping
        crawler = NaverScraping(keyword, period=period, device=device, gender=gender, age=age)
        meta_data = crawler.get_metadata() # auto gen meta_data
        files = crawler.start_scraping()

        # Start ETL
        if not files:
            raise Exception("Crawling job failed unexpectedly, no downloaded file found")
        for file in files:
            file_path = constants.DOWNLOAD_FOLDER + f"\\{file}"
            meta_data["file_name"] = file
            pipeline = ETLProcess(file_path, meta_data) # along with metadata in the file, we can upload it to s3
            pipeline.process()
    except Exception as exp:
        logging.error("Error in main() method. Stack Trace " + str(exp), exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    # Load Logging Configuration File
    import logging.config
    logging.config.fileConfig(fname='utils/logging_to_file.conf')
    main()
