from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import constants

chrome_options = Options()
chrome_options.add_experimental_option("detach", True) #keeps chrome open
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #stops continuous prints from Selenium
# chrome_options.add_argument('headless')
def start_session()->webdriver:
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    driver.get(constants.SOC)
    return driver
    
# driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=chrome_options)

# driver.get(constants.SOC)
def navigate_to_cs_courses_fall_2022(driver:webdriver):
    try:
        fall_spring = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID,"FALL_SPRING_1_INPUT"))
        fall_spring.click()
        campus = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID,"campus_NB"))
        campus.click()
        grade = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID,"level_U"))
        grade.click()
        con_button = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID,"continueButton"))
        con_button.click()
        
        sub_search = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID,"subject_search_id"))
        assert sub_search.get_attribute('class') == 'selected'
        
        course_select = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID, "dijit_form_FilteringSelect_0"))
        course_select.send_keys("Computer Science (198)")
        course_select.send_keys(Keys.RETURN)
        
        bs = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.ID, "01:198:107.0.courseExpandIcon"))
        bs.click()
    except NoSuchElementException:
        print("Didn't find it")
        exit(1)
    except TimeoutException:
        print("Time Out")
        exit(1)
    except AssertionError:
        print("for some reason youre not in the subject box")
        exit(1)

# finally:
#     driver.quit()

def get_soup(driver:webdriver)->BeautifulSoup:
    html_source = driver.page_source
    return BeautifulSoup(html_source, "html.parser")
    
def main():
    driver = start_session()
    navigate_to_cs_courses_fall_2022(driver)
    soup = get_soup(driver)
    course_name_spans = soup.find_all('span', class_='courseTitle') #*the right one
    instructors = soup.find_all('span', class_="instructors")
    for i in instructors:
        print(i.text)

if __name__ == "__main__":
    main()
# for c in course_name_spans:
#     print(c.text)
    

# print(soup.find('span', class_='courseTitle'))
 


