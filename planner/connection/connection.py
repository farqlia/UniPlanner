import json
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from planner.models.groups import Group, Course, Teacher
from planner.parsing.parse_elements import group_factory

ENROLLMENT_XPATH = "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[" \
                   "1]/td/table[2]/tbody/tr[15]/td/a"
FAILED_LOG_IN_XPATH = "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/b[" \
                      "2]/font"
PREFIX_COURSE = '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[' \
                '6]/tbody/tr['
PREFIX_GROUP = '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr['


class GroupsDownloader:
    def __init__(self):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)

    def open_website(self):
        url = "https://edukacja.pwr.wroc.pl/"
        self.driver.get(url)

    def log_user_in(self, login: str, password: str):
        username_input = self.driver.find_element(By.NAME, "login")
        username_input.send_keys(login)
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        login_button = self.driver.find_element(By.CSS_SELECTOR, ".BUTTON_ZALOGUJ")
        login_button.click()
        self.check_if_success()

    def check_if_success(self):
        try:
            _ = self.driver.find_element(By.XPATH, FAILED_LOG_IN_XPATH).text
            print("Login failed")
        except NoSuchElementException:
            print("Login succeeded")

    def open_enrollment_website(self):
        self.driver.find_element(By.XPATH, ENROLLMENT_XPATH).click()

    def go_to_current_enrollment(self):
        element = self.driver.find_element_by_xpath("//a[contains(text(), '2022/2023')]")
        element.click()
        element = self.driver.find_element_by_xpath("//a[contains(text(), 'W04N_Wydz_Zapisy_s_letni_2022/23_ST')]")
        element.click()
        button = self.driver.find_elements_by_css_selector('input[name="event_ZapisyPrzegladanieGrup"]')[1]
        button.click()
        criteria = Select(self.driver.find_element(By.NAME, "KryteriumFiltrowania"))
        criteria.select_by_visible_text("Z wektora zapisowego, do których słuchacz ma uprawnienia")

    def get_courses(self):
        courses_list, i, j = [], 2, 0
        pagination = self.driver.find_elements(By.CLASS_NAME, "paging-numeric-btn")
        while True:
            try:
                self.add_course(courses_list, i)
                i += 1
            except NoSuchElementException:
                if j < len(pagination):
                    pagination[j].click()
                    j += 1
                    i = 2
                else:
                    break
        return courses_list

    def get_groups(self, curr_course):
        curr_page = 0
        self.driver.get(curr_course.link)
        i = 4
        while True:
            try:
                if self.driver.find_element(By.XPATH, PREFIX_GROUP + str(i) + ']/td[1]').text == "":
                    i += 1
                self.add_groups(curr_course, i)
                i += 3
            except NoSuchElementException:
                pages = self.driver.find_elements(By.XPATH,
                                                  '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr['
                                                  '1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr['
                                                  '41]/td/table/tbody/tr/td/span/input[2]')
                if curr_page < len(pages):
                    i = 4
                    pages[curr_page].click()
                    curr_page += 1
                else:
                    break

    def add_course(self, courses, index):
        course_code = self.driver.find_element(By.XPATH, PREFIX_COURSE + str(index) + "]/td[1]/a").text
        course_name = self.driver.find_element(By.XPATH, PREFIX_COURSE + str(index) + "]/td[2]").text
        course_link = self.driver.find_element(By.XPATH, PREFIX_COURSE + str(index) + "]/td[1]/a").get_attribute("href")
        courses.append(Course(code=course_code, name=course_name, link=course_link, groups=[]))

    def add_groups(self, course, index):
        classes_code = self.driver.find_element(By.XPATH, PREFIX_GROUP + str(index) + ']/td[1]').text
        course_code = self.driver.find_element(By.XPATH, PREFIX_GROUP + str(index) + ']/td[2]').text
        lecturer = self.driver.find_element(By.XPATH, PREFIX_GROUP + str(index + 1) + ']/td[1]').text

        date_and_place = self.driver.find_element(By.XPATH, PREFIX_GROUP + str(index + 2) + ']/td/table'
                                                                                            '/tbody/tr['
                                                                                            '1]/td').text
        classes_type = self.driver.find_element(By.XPATH, PREFIX_GROUP + str(index + 1) + ']/td[2]').text
        course.groups.append(group_factory(code=classes_code, course=course_code, lecturer=lecturer,
                                           date_and_place=date_and_place, type=classes_type))

    def download_courses(self):
        courses = self.get_courses()
        for curr_course in courses:
            self.get_groups(curr_course)
        self.driver.quit()
        return courses

    def download_groups(self, login: str, password: str) -> List[Course]:
        try:
            self.open_website()
            self.log_user_in(login=login, password=password)
            self.open_enrollment_website()
            self.go_to_current_enrollment()
            return self.download_courses()
        except NoSuchElementException:
            return []


def obj_to_dict(obj):
    if isinstance(obj, list):
        return {
            "course": [obj_to_dict(c) for c in obj]
        }
    elif isinstance(obj, Teacher):
        return {
            "title": obj.title,
            "name": obj.name
        }
    elif isinstance(obj, Group):
        return {
            "code": obj.code,
            "course": obj.course,
            "lecturer": obj_to_dict(obj.lecturer),
            "day": str(obj.day),
            "week_type": str(obj.week_type),
            "start_time": str(obj.start_time),
            "end_time": str(obj.end_time),
            "building": obj.building,
            "hall": obj.hall,
            "type": str(obj.type)
        }
    elif isinstance(obj, Course):
        return {
            "name": obj.name,
            "code": obj.code,
            "groups": [obj_to_dict(c) for c in obj.groups]
        }


def dump_to_file(courses, file: str):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj_to_dict(courses), f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_name = 'pwr345992'
    user_password = 'me_gustas_tu'
    downloader = GroupsDownloader()
    subjects = downloader.download_groups(user_name, user_password)
    file_name = '../../data/new_.json'
    dump_to_file(subjects, file_name)

    """# Kliknięcie najnowszego zapisu driver.find_element(By.CSS_SELECTOR, "#GORAPORTALU > tbody > tr:nth-child(4) > 
    td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > table:nth-child(16) > tbody > 
    tr:nth-child(3) > td:nth-child(1) > a").click()

    trTable = driver.find_elements(By.XPATH,
                                   "//*[@id=\"GORAPORTALU\"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[8]/tbody/tr")

    # Wyszukiwanie zapisów jednostki
    for i in range(len(trTable)):
        tr = trTable[i]
        enrollmentType = tr.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        if "Wydział" in enrollmentType:
            tr.find_element(By.CSS_SELECTOR,
                            "td:last-child > table > tbody > tr > td:last-child > input:last-child").click()
            break"""
