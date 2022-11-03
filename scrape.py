from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import constants
import courses


def start_session() -> webdriver:
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True) #keeps chrome open
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get(constants.SOC)
    return driver


def navigate_to_cs_courses_fall_2022(driver: webdriver):
    try:
        fall_spring = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(
            By.ID, "FALL_SPRING_1_INPUT"))
        fall_spring.click()
        campus = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "campus_NB")
        )
        campus.click()
        grade = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID, "level_U"))
        grade.click()
        con_button = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "continueButton")
        )
        con_button.click()

        sub_search = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "subject_search_id")
        )
        assert sub_search.get_attribute('class') == 'selected'

        course_select = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "dijit_form_FilteringSelect_0")
        )
        course_select.send_keys("Computer Science (198)")
        course_select.send_keys(Keys.RETURN)

        bs = WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.ID, "01:198:107.1.courseExpandIcon")
        )
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


def get_soup(driver: webdriver) -> BeautifulSoup:
    html_source = driver.page_source
    return BeautifulSoup(html_source, "html.parser")


def main():
    driver = start_session()
    navigate_to_cs_courses_fall_2022(driver)
    soup = get_soup(driver)
    subjects = soup.find_all('div', class_='subject')

    objs = []
    for subject in subjects:
        title = subject.find('span', class_="courseTitle").text
        course_id = subject.find('span', class_='courseId').span.span.text
        try:
            open_sections = subject.find('span', class_='courseOpenSectionsNumerator').text
        except AttributeError:
            try:
                open_sections = subject.find('span', class_='courseOpenSectionsNumeratorZero').text
            except AttributeError:
                print("welp")
                exit(1)
        all_sections = subject.find('span', class_='courseOpenSectionsDenominator').text
        # print(f"{course_id}--> {title}")
        # print(f"Sections: {open_sections}{all_sections}")
        objs.append(courses.Course(title, course_id, open_sections + all_sections))

    print(objs[6].course_title)
    print(objs[6].sections)

    # instructors = soup.find_all('span', class_="instructors")
    # for i in instructors:
    #     print(i.text)


if __name__ == "__main__":
    main()
