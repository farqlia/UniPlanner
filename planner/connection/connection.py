import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from typing import Tuple
from datetime import datetime
import re
from planner.models.classes import Class, Course, DayOfWeek, WeekType

# Sorry ze tutaj ale to na szybko zebys zobaczyl
# Do testow odsylam jak to wyglada
# Mysle ze mozemy miec te pola w klasie Class zamiast wlasnie tego stringa

PLACE_AND_DATE_REGEX = re.compile("(?P<day_of_week>\w{2})(?P<type_of_week>[TPN+12/]*) "
                                "(?P<hour_start>\d{2}:\d{2})-(?P<hour_end>\d{2}:\d{2}), bud. (?P<building>[-\w]+), sala (?P<hall>\w+)")

POLISH_ABBR_DAY_OF_WEEK = {'pn': DayOfWeek.Monday, 'wt':
    DayOfWeek.Tuesday, 'śr': DayOfWeek.Wednesday, 'cz': DayOfWeek.Thursday,
                           'pt': DayOfWeek.Friday}


def as_hour(hour: str) -> datetime:
    return datetime.strptime(hour, "%H:%M")


def parse_date_and_place(date_and_place: str) -> Tuple[DayOfWeek, WeekType, datetime, datetime, str, str]:
    match = PLACE_AND_DATE_REGEX.match(date_and_place)
    day_of_week = POLISH_ABBR_DAY_OF_WEEK[match.group("day_of_week")]
    type_of_week = WeekType.EVERY_WEEK if len(match.group("type_of_week")) == 0 \
        else WeekType.EVEN_WEEK if match.group("type_of_week").startswith("/TP") else WeekType.ODD_WEEK
    start_time = as_hour(match.group("hour_start"))
    end_time = as_hour(match.group("hour_end"))
    return day_of_week, type_of_week, start_time, end_time, match.group("building"), match.group("hall")


def do_fetch_subjects(login, password): # TA FUNKCJA JEST STRASZNA JUTRO TO NAPRAWIĘ  # Jest super!!!
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    url = 'https://edukacja.pwr.wroc.pl/EdukacjaWeb/studia.do'
    driver.get("https://edukacja.pwr.wroc.pl/")
    # Wprowadzenie nazwy użytkownika
    username_input = driver.find_element(By.NAME, "login")
    username_input.send_keys(login)

    # Wprowadzenie hasła
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)

    # Kliknięcie przycisku "ZALOGUJ"
    login_button = driver.find_element(By.CSS_SELECTOR, ".BUTTON_ZALOGUJ")
    login_button.click()

    # Sprawdzenie czy wystąpił błąd logowania
    """try:
        potentialLoginError = driver.find_element(By.XPATH,
                                                  "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/b[2]/font").text
        raise LoginException()
    except NoSuchElementException:
        pass"""




    # Kliknięcie przycisku "ZAPISY"
    driver.find_element(By.XPATH,
                        "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/table[2]/tbody/tr[15]/td/a").click()

    prawoDoZapisow = driver.find_element(By.XPATH,
                                         "//*[@id=\"GORAPORTALU\"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[5]/tbody/tr[4]/td").text
    if "Brak prawa" in prawoDoZapisow:
        print("blad prawa do zapisow")

    element = driver.find_element_by_xpath("//a[contains(text(), '2022/2023')]")

    # Kliknięcie znalezionego elementu
    element.click()

    element = driver.find_element_by_xpath("//a[contains(text(), 'W04N_Wydz_Zapisy_s_letni_2022/23_ST')]")
    element.click()

    button = driver.find_elements_by_css_selector('input[name="event_ZapisyPrzegladanieGrup"]')[1]
    button.click()

    """ # Kliknięcie najnowszego zapisu
    driver.find_element(By.CSS_SELECTOR,
                        "#GORAPORTALU > tbody > tr:nth-child(4) > td > table > tbody > tr:nth-child(1) > td.PRAWA_KOMORKA > table > tbody > tr > td > table:nth-child(16) > tbody > tr:nth-child(3) > td:nth-child(1) > a").click()

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

    filter = Select(driver.find_element(By.NAME, "KryteriumFiltrowania"))
    filter.select_by_visible_text("Z wektora zapisowego, do których słuchacz ma uprawnienia")

    courses = []
    pagination = driver.find_elements(By.CLASS_NAME, "paging-numeric-btn")

    i = 2
    j = 0

    while True:
        try:
            course_code = driver.find_element(By.XPATH,
                                            "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[6]/tbody/tr[" + str(
                                                i) + "]/td[1]/a").text
            course_name = driver.find_element(By.XPATH,
                                              "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[6]/tbody/tr[" + str(
                                                  i) + "]/td[2]").text
            course_link = driver.find_element(By.XPATH,
                                                    "/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[6]/tbody/tr[" + str(
                                                        i) + "]/td[1]/a").get_attribute("href")
            courses.append(Course(code=course_code, name=course_name, link=course_link))
            i += 1
        except NoSuchElementException:
            if j < len(pagination):
                pagination[j].click()
                j += 1
                i = 2
            else:
                break
    for curr_course in courses:
        pageNum = 0
        driver.get(curr_course.link)
        it = 4
        while True:
            try:

                if driver.find_element(By.XPATH,
                                       '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                               it) + ']/td[1]').text == "":
                    it += 1

                classes_code = driver.find_element(By.XPATH,
                                                  '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                                      it) + ']/td[1]').text
                course_code = driver.find_element(By.XPATH,
                                                       '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                                           it) + ']/td[2]').text
                lecturer = driver.find_element(By.XPATH,
                                                     '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                                         it + 1) + ']/td[1]').text

                date_and_place = driver.find_element(By.XPATH,
                                                  '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                                      it + 2) + ']/td/table/tbody/tr[1]/td').text
                classes_type = driver.find_element(By.XPATH,
                                                  '//*[@id="GORAPORTALU"]/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[' + str(
                                                      it + 1) + ']/td[2]').text
                curr_course.classes.append(Class(code=classes_code, course=course_code, lecturer=lecturer,
                      date_and_place=date_and_place, type=classes_type))
                it += 3

            except NoSuchElementException:
                list = driver.find_elements(By.XPATH,
                                            '/html/body/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td/table[7]/tbody/tr[41]/td/table/tbody/tr/td/span/input[2]')
                if pageNum < len(list):
                    it = 4
                    list[pageNum].click()
                    pageNum += 1
                else:
                    break

    driver.quit()
    return courses


def obj_to_dict(obj):
    if isinstance(obj, list):
        return{
            "course": [obj_to_dict(c) for c in obj]
        }
    elif isinstance(obj, Class):
        return {
            "code": obj.code,
            "course": obj.course,
            "lecturer": obj.lecturer,
            "date_and_place": obj.date_and_place,
            "type": obj.type
        }
    elif isinstance(obj, Course):
        return {
            "name": obj.name,
            "code": obj.code,
            "classes": [obj_to_dict(c) for c in obj.classes]
        }


if __name__ == '__main__':
    login = 'pwr384918'
    password = 'puszek112'
    subjects = do_fetch_subjects(login, password)
    with open('../../data/courses.json', 'w', encoding='utf-8') as f:
        json.dump(obj_to_dict(subjects), f, indent=4, ensure_ascii=False)
