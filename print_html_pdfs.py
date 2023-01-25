"""
prints html pages as pdf using chrome.
default input directory is html.
outputs to the pdfs folder.

usage: python3 print_html_pdfs.py <dir or [files]>

python3 print_html_pdfs.py
  * this prints as pdf all files with .html extension in html folder

python3 print_html_pdfs.py html/sample.html html/sample1.html
  * this prints as pdf the listed .html files only (regardless the folder)

python3 print_html_pdfs.py .
  * this prints as pdf the listed .html files in the specified folder
    (in this case the current directory, of which there are none)
"""

import sys
import os
from time import sleep
from os.path import exists
import json
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions

# paths
curr_dir = os.getcwd()
output_dir = "pdfs/"

print_settings = {
    "displayHeaderFooter": False,
    "printBackground": True
}


def main():
    pages = getPages()
    if len(pages) == 0:
        print("nothing to print, exiting")
        exit(0)

    driver = getDriver()

    for page in pages:
        file_segments = os.path.splitext(os.path.basename(page))
        prefix = file_segments[0]
        printPage(page, prefix, driver)

    driver.quit()


"""
get chrome web driver with print as pdf options.
"""
def getDriver():
    options = ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--kiosk-printing")
    options.add_argument('--headless')

    return webdriver.Chrome(options=options)


"""
get list of .html files to print.
"""
def getPages():
    input_dir = "html"
    if len(sys.argv) > 1:
        if not os.path.isdir(sys.argv[1]):
            return sys.argv[1:]
        else:
            input_dir = os.path.join(sys.argv[1])

    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    return [file for file in files if os.path.splitext(os.path.basename(file))[-1] == ".html"]


"""
get print .html file as pdf and save with prefix (filename without extension).
"""
def printPage(page, prefix, driver):
    url = "file://" + os.path.join(curr_dir, page)
    driver.get(url)

    # this is so jank but if page contains image, wait for 0.2 seconds before printing
    # (presence of image causes text to load slower)
    try:
        img = driver.find_element(By.TAG_NAME, 'img')
        sleep(0.2)
    except NoSuchElementException:
        pass

    # yeah so the following doesn't work bc the selenium expected conditions definition of visibility is:
    # "the element is not only displayed but also has a height and width that is greater than 0"
    # and when printing, the text could have height but not actually be loaded

    # try:
    #     _ = WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'body')))
    # except TimeoutException:
    #     print("warning: page timed out!")

    data = driver.execute_cdp_cmd("Page.printToPDF", print_settings)
    with open(output_dir + prefix + ".pdf", 'wb') as f:
        f.write(base64.b64decode(data['data']))

    if not exists(output_dir + prefix + ".pdf"):
        print("warning: " + page + " failed to print, skipping")


if __name__ == '__main__':
    main()

