from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import abc
import os
import logging.config
from typing import Dict

from scripts.constants import DRIVER_PATH, URL, PERIOD_LIST, DOWNLOAD_FOLDER, AGE_LIST
from helpers.helper import try_parsing_date

logging.config.fileConfig(fname='utils/logging_to_file.conf')
logger = logging.getLogger(__name__)
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": DOWNLOAD_FOLDER}
options.add_experimental_option("prefs", prefs);


class AbstractNaverScraping(abc.ABC):

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)

    @abc.abstractmethod
    def start_scraping(self):
        raise NotImplementedError()


class NaverScraping(AbstractNaverScraping):

    def __init__(self, keyword: Dict, period=None, date_range='default', device='default', gender=None,
                 age='default'):
        super().__init__()
        self._keyword = keyword
        self.period = period
        self.date_range = date_range
        self.device = device
        self.gender = gender
        self.age = age

    def get_metadata(self):
        metadata = {
            'keyword': self._keyword,
            'period': self.period,
            'date_range': self.date_range[:2],
            'device': self.device,
            'gender': self.gender,
            'age': self.age
        }
        return metadata

    def start_scraping(self) -> list[str]:
        logging.info("Start scraping data from " + URL)
        self.driver.get(URL)

        logging.info("Successfully start up webdriver")
        # Input Keywords
        try:
            logging.info("Start setting keywords parameter")
            keyword_elements = self.driver.find_elements(By.XPATH,
                                                         "//fieldset//div[contains(@class,'form_row keyword')]")
            no_of_keyword = len(self._keyword.keys())
            for i, item in enumerate(keyword_elements[:no_of_keyword]):
                key = list(self._keyword.keys())[i]
                keyword_box = item.find_element(By.XPATH, r".//input[contains(@id,'item_keyword')]")
                keyword_box.click()
                keyword_box.send_keys(key)
                sub_keyword_box = item.find_element(By.XPATH, r".//input[contains(@id,'item_sub_keyword')]")
                sub_keyword_box.click()
                sub_keyword_box.send_keys(self._keyword[key])
        except NoSuchElementException as exp:
            logging.error("Log error Xpath for keyword not found. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done setting up keyword parameters")

        # Input period
        try:
            logging.info("Start setting up periods parameter")
            if self.period != 'default':
                period_element = self.driver.find_element(By.XPATH, "//*[@class='set_period']")
                if self.period['period'] in PERIOD_LIST:
                    option_index = PERIOD_LIST.index(self.period['period']) + 1
                    period_option = period_element.find_element(By.XPATH,
                                                                f".//*[contains(@for,'period{option_index}')]")
                    period_option.click()
                else:
                    try:
                        period_option = period_element.find_element(By.XPATH, f".//*[contains(@for,'period5')]")
                        period_option.click()
                        start_date = try_parsing_date(self.period["date_range"][0])
                        end_date = try_parsing_date(self.period["date_range"][1])
                        if end_date < start_date or start_date.year < 2016:
                            raise ValueError
                        period_target_element = self.driver.find_element(By.XPATH, ".//*[@class='set_period_target']")
                        start_year_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'startYear')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(start_date.year)}')",
                                                   start_year_ele)
                        start_month_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'startMonth')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(start_date.month).zfill(2)}')", start_month_ele)
                        end_year_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'endYear')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(end_date.year)}')", end_year_ele)
                        end_month_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'endMonth')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(end_date.month).zfill(2)}')", end_month_ele)
                        end_day_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'endDay')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(start_date.day).zfill(2)}')", end_day_ele)
                        start_day_ele = period_target_element.find_element(By.XPATH, ".//input[contains(@id, 'startDay')]")
                        self.driver.execute_script(f"arguments[0].setAttribute('value', '{str(end_date.day).zfill(2)}')", start_day_ele)
                    except ValueError:
                        print("Date format not valid")

                # Input frequency
                if self.period['frequency'] in ['date', 'month', 'year']:
                    frequency_element = self.driver.find_element(By.XPATH, "//a[contains(@id,'time')]")
                    self.driver.execute_script(f"arguments[0].setAttribute('value', '{self.period['frequency']}')",
                                               frequency_element)

        except NoSuchElementException as exp:
            logging.error("Error Xpath for period not found. Stack trace " + str(exp), exc_info=True)
        except (KeyError, ValueError) as exp:
            logging.error(
                "Error detect input for period not valid, set default for invalid parameters. Stack trace " + str(exp),
                exc_info=True)
        except IndexError as exp:
            logging.error("Error No manual date input found for period. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done setting up parameters for period")

        # Input device
        try:
            logging.info("Start setting up parameters for device")
            if self.device == 'mobile':
                device_xpath = "//input[contains(@id,'item_device') and @value='mo']"
            elif self.device == 'pc':
                device_xpath = "//input[contains(@id,'item_device') and @value='pc']"
            else:
                device_xpath = "//input[contains(@id,'item_device') and contains(@class,'check_all')]"
            tick_box_device = self.driver.find_element(By.XPATH, device_xpath)
            tick_box_device.click()
        except NoSuchElementException as exp:
            logging.error("Log error Xpath for device not found. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done setting up parameters for device")

        # Input gender
        try:
            logging.info("Start setting up parameters for gender")
            if self.gender == 'female':
                device_xpath = "//input[contains(@id,'item_gender') and @value='f']"
            elif self.gender == 'male':
                device_xpath = "//input[contains(@id,'item_gender') and @value='m']"
            else:
                device_xpath = "//input[contains(@id,'item_gender') and contains(@class,'check_all')]"
            tick_box_device = self.driver.find_element(By.XPATH, device_xpath)
            tick_box_device.click()
        except NoSuchElementException as exp:
            logging.error("Log error Xpath for gender not found. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done setting up parameters for gender")

        # Input age
        try:
            logging.info("Start setting up parameters for age")
            if 'entire' in self.age:
                age_xpath = "//input[contains(@id,'item_age') and contains(@class,'check_all')]"
                tick_box_age = self.driver.find_element(By.XPATH, age_xpath)
                tick_box_age.click()
            else:
                for item in self.age:
                    index = AGE_LIST.index(item) + 1
                    age_xpath = f"//input[contains(@id,'item_age') and @value='{index}']"
                    tick_box_age = self.driver.find_element(By.XPATH, age_xpath)
                    tick_box_age.click()

        except NoSuchElementException as exp:
            logging.error("Log error Xpath for age not found. Stack trace " + str(exp), exc_info=True)
        except (IndexError, ValueError) as exp:
            logging.error("Invalid input for age. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done setting up parameters for age")

        # hit data search button
        try:
            logging.info("Requesting data files base on parameter")
            submit_button = self.driver.find_element(By.XPATH, "//*[contains(@class,'trend_search_detail_query')]/*")
            submit_button.click()
        except NoSuchElementException as exp:
            logging.error("Log error Xpath for submit button not found. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Requesting data files base on parameter successfully")

        # wait for page to load
        try:
            wait = WebDriverWait(self.driver, 10)
            # download excel file
            wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@href,'qcExcel')]"))).click()
            logging.info(f"Start download file")
            import time
            time.sleep(5)
            logging.info(f"Download successfully")

            return [f for f in os.listdir(DOWNLOAD_FOLDER)]
        finally:
            self.driver.quit()
