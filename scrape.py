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
#chrome_options.add_experimental_option("detach", True) #keeps chrome open
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) #shuts it the fuck up
chrome_options.add_argument('headless')
def start_session():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    WebDriverWait(driver, timeout=10)
    driver.get(constants.SOC)
    return driver
    
driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),options=chrome_options)

# try:
#     WebDriverWait(driver, timeout=10).until(driver.find_element(By.ID, "FALL_SPRING_1_TEXT"))
# except NoSuchElementException:
#     print("Didn't find it")
# finally:
#     print("works?")
driver.get(constants.SOC)

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
    # print(course_expand.text)
except NoSuchElementException:
    print("Didn't find it")
except TimeoutException:
    print("Time Out")
except AssertionError:
    print("for some reason youre not in the subject box")
# finally:
#     driver.quit()

# for ele in driver.find_elements(By.CLASS_NAME, "highlighttext"):
#     ele.click()

course_expand = WebDriverWait(driver,timeout=10).until(lambda d: d.find_element(By.XPATH, "/html/body/main/div[2]/table/tbody/tr/td[2]/div[5]/div[1]/h4/span"))
course_expand.click()
html_source = driver.page_source



soup = BeautifulSoup(html_source, "html.parser")
# for all_subj_info in soup.find_all('div', class_='subject'):
#     course_name_spans = soup.find_all('span', class_='highlighttext')
    
#     course_names = [print(course_name) for course_name in course_name_spans]
#     print(len(course_name_spans)/2)
#     break


# all_subj_info = soup.find_all('div', class_='subject')

course_name_spans = soup.find_all('span', class_='courseTitle') #*the right one
# for c in course_name_spans:
#     print(c.text)
    
instructors = soup.find_all('span', class_="instructors")
for i in instructors:
    print(i.text)

# print(soup.find('span', class_='courseTitle'))

    
    
        

#element = WebDriverWait(driver, timeout=10).until(driver.find_element(By.ID, "FALL_SPRING_1_TEXT"))


