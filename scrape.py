import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import constants
import courses


def start_session() -> webdriver:
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # keeps chrome open
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )
    driver.get(constants.SOC)
    return driver


def get_soup(driver: webdriver) -> BeautifulSoup:
    html_source = driver.page_source
    return BeautifulSoup(html_source, "html.parser")


def new_thing():
    driver = start_session()
    expand = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_element(By.ID, "subjectTitle2")
    )

    time.sleep(3)  # wait for page to fully load

    expand.click()

    soup = get_soup(driver)
    subjects = soup.find_all('div', class_='subject')

    # will even get prereqs even if the link is hidden
    prereqs = WebDriverWait(driver, timeout=10).until(
        lambda d: d.find_elements(By.CLASS_NAME, "prereq")
    )

    for i, subject in enumerate(subjects):
        # print title and course_id
        title = subject.find('span', class_="courseTitle").text
        print(title)
        course_id = subject.find('span', class_='courseId').text
        print(course_id)
        course_credits = subject.find('span', class_='courseCredits').text
        print(f"COURSE CREDITS: {course_credits}")

        course_notes = subject.find('div', 'courseNotesHeader')
        all_course_notes = course_notes.find_all('div', recursive=False)
        for course_note in all_course_notes:
            print(course_note.text.strip())

        # section listing for 1 subject
        section_listing = subject.find('div', class_='sectionListings')
        sections = section_listing.find_all('div', recursive=False)

        for section in sections:
            section_number = section.find('span', 'sectionDataNumber')

            # Comments, Notes, Sections open to
            section_header = section.find('div', 'sectionNotesHeader')
            all_notes = section_header.find_all('div', recursive=False)

            for notes in all_notes:
                print(notes.text)

            if section_number:
                print(f'SECTION: {section_number.text}')

            # instructors
            instructors = section.find('span', class_='instructors')
            if instructors and instructors.text:
                print(f"INSTRUCTORS: {instructors.text}")
            else:
                print("TBD")

            exam_code = section.find('span', class_='examCode')
            if exam_code:
                print(f"EXAM CODE: {exam_code.text}")

            # Meeting information for all sections
            meeting_times = section.find('div', "sectionMeetingTimesDiv")
            week_info = meeting_times.find_all('div', recursive=False)
            try:
                for day_info in week_info:
                    day = day_info.find('span', 'meetingTimeDay').text
                    hours = day_info.find('span', 'meetingTimeHours').text
                    campus = day_info.find('span', 'meetingTimeCampus').text
                    building = day_info.find('span', 'meetingTimeBuildingAndRoom')
                    building_link = building.find('a')['href']

                    print(f"{day}, {hours}, {campus}, {building.text}, {building_link}")
            except AttributeError:
                special_meets = meeting_times.div.find('span', recursive=False)
                for special_meet in special_meets:
                    print(special_meet.text)

        try:
            actions = ActionChains(driver)
            actions.move_to_element(prereqs[i]).perform()
            time.sleep(.5)
            peepeepoopoo = WebDriverWait(driver, timeout=1).until(
                lambda d: d.find_element(By.XPATH, "//*[@id='dijit__MasterTooltip_0']/div[2]/span")
            )
            print(peepeepoopoo.text)
        except TimeoutException:
            print("NO PREREQS")
        print()


def navigate_to_cs_courses_fall_2022(driver: webdriver):  # obsolete kinda
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


if __name__ == "__main__":
    new_thing()
