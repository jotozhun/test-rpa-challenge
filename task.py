import time
import requests
import pandas
import os

from models.NYNEWS_OBJ import NYNEWS_OBJ
from utils.utils import map_categories_to_index, normalize_months_to_watch, find_dollar_ocurrence
from utils.nytimes_vars import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from SeleniumLibrary.errors import ElementNotFound
from RPA.Robocorp.WorkItems import WorkItems


def main(word: str, categories: list[str], number_of_months: int):
    # Lists of lists with the information of earch row
    df_rows_list = []

    nynews_obj = NYNEWS_OBJ(url=NYTIMES_URL)
    today_date = datetime.now()
    # destination_folder = f"logs/{today_date.strftime(EXECUTION_NAME_FORMAT)}"
    destination_folder = "output"
    categories_indexes = map_categories_to_index(categories, CATEGORIES_MAP_INDEX)

    try:
        # Search a word
        nynews_obj.click_on_btn()
        nynews_obj.search_for(word=word)
        nynews_obj.click_on_element(SORT_FILTER_BTN)
        nynews_obj.browser_lib.press_keys(SORT_FILTER_BTN, DOWN_ARROW)

        # Filter for most recent news
        nynews_obj.click_on_btn(SECTION_FILTER_BTN)
        nynews_obj.wait_for_element_to_be_present(SECTION_FILTER_DROPDOWN)

        # Select the categories for the filter
        category_elements = nynews_obj.browser_lib.find_elements(SECTION_CHECKBOX)
        for category_index in categories_indexes:
            category_elements[category_index].click()
        nynews_obj.click_on_btn(HIDE_SECTION_FILTER_BTN)

        # Filter for date ranges
        nynews_obj.click_on_btn(DATE_FILTER_BTN)
        nynews_obj.wait_for_element_to_be_present(DATE_FILTER_DROPDOWN)

        # Select option to specify date ranges
        date_options = nynews_obj.browser_lib.find_elements(DATE_FILTER_OPTION)
        date_options[-1].click()

        specific_date_inputs = nynews_obj.browser_lib.find_elements(DATE_INPUT_RANGE)
        start_date = today_date.replace(day=1) - relativedelta(months=normalize_months_to_watch(number_of_months))

        specific_date_inputs[0].send_keys(start_date.strftime(STANDARD_DATE_FORMAT))
        specific_date_inputs[1].send_keys(today_date.strftime(STANDARD_DATE_FORMAT))

        nynews_obj.click_on_btn(HIDE_DATE_FILTER_BTN)

        print("Waiting for 10 seconds")
        time.sleep(10)
        is_show_more_btn = nynews_obj.browser_lib.is_element_visible(SHOW_MORE_BTN)
        print("Element show more button: ")
        print(is_show_more_btn)

        nynews_obj.browser_lib.capture_element_screenshot(SHOW_MORE_BTN, filename="./output/screenshot_btn.png")
        nynews_obj.browser_lib.capture_element_screenshot(COOKIES_POPUP, filename="./output/screenshot_btn2.png")
        if nynews_obj.browser_lib.is_element_visible(COOKIES_POPUP):
            nynews_obj.browser_lib.press_keys(COOKIES_POPUP, ALT_KEY, ALT_KEY, ALT_KEY, ENTER_KEY)
        nynews_obj.browser_lib.capture_element_screenshot(SHOW_MORE_BTN, filename="./output/screenshot_btn3.png")

        # while nynews_obj.browser_lib.is_element_enabled("css:div.css-f63blv.e2qmvq0"):
        #     print("Button Load More")
        #     nynews_obj.click_on_element("css:div.css-f63blv.e2qmvq0")

        # Create a directory of the execution results with the today's datetime as name

        # try:
        #     while True:
        #         time.sleep(5)
        #         show_more_btn = nynews_obj.browser_lib.find_element(SHOW_MORE_BTN)
        #         show_more_btn.click()
        #         # nynews_obj.click_on_btn(SHOW_MORE_BTN)
        #         # TODO
        #         # This delay is neccesary when button appears more than 1 time
        #         # But soon the page will be so large that will last more to load this button
        #         time.sleep(3)
        # except e:
        #     print("No Load More buttons found")
        print("Create images folder")
        news_elements = nynews_obj.browser_lib.find_elements(NEWS_ELEMENT)
        for news_element in news_elements:
            print("Starting store")
            # Stores the news data in this list in order: title, date, description, filename
            tmp_new_obj = []
            title_element = nynews_obj.browser_lib.find_element(TITLE_NEWS_ELEMENT,
                                                                news_element).text
            date_element = nynews_obj.browser_lib.find_element(DATE_NEWS_ELEMENT,
                                                               news_element).text
            description_element = nynews_obj.browser_lib.find_element(DESCRIPTION_NEWS_ELEMENT,
                                                                      news_element).text
            tmp_new_obj.append(title_element)
            tmp_new_obj.append(date_element)
            tmp_new_obj.append(description_element)

            # Check if title or description contains any amount of money
            if find_dollar_ocurrence(title_element) or find_dollar_ocurrence(description_element):
                tmp_new_obj.append("True")
            else:
                tmp_new_obj.append("False")
            try:
                # In case the image of the new doesn't exists
                image = nynews_obj.browser_lib.find_element(IMAGE_NEWS_ELEMENT,
                                                            news_element)
                image_url = image.get_attribute("src")

                # Filtering url and query params to get the filename
                image_filename = image_url.split("/")[-1].split("?")[0]
                with open(f"{destination_folder}/{image_filename}", "wb") as file:
                    image_response = requests.get(image_url, stream=True)

                    # Since images are large size, we download them by chunks
                    for image_batch in image_response.iter_content(1 * KILOBYTE):
                        if not image_batch:
                            break
                        file.write(image_batch)
                tmp_new_obj.append(image_filename)
            except ElementNotFound as e:
                tmp_new_obj.append(NOT_FOUND_ELEMENT)
            finally:
                # In case of failures on getting information, the news information will be kept
                df_rows_list.append(tmp_new_obj)

    finally:
        # In case the webpage fails at the middle of the script, it will save the data obtained
        nynews_obj.quit_browsers()

        df_data = pandas.DataFrame(df_rows_list)
        df_data.to_excel(f"{destination_folder}/data.xlsx", header=OUTPUT_HEADERS, index=False)

if __name__ == "__main__":
    word = "murder"
    categories = ["Arts", "U.S.", "World"]
    number_of_months = 0
    # library = WorkItems()
    # library.get_input_work_item()
    # word = library.get_work_item_variable("word")
    # categories = library.get_work_item_variable("categories")
    # number_of_months = library.get_work_item_variable("number_of_months")
    main(word, categories, number_of_months)
