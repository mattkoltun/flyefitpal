from time import sleep
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By

LOGIN_URL = "https://myflye.flyefit.ie/login"
BOOKING_URL = "https://myflye.flyefit.ie/myflye/book-workout"
SITE_IDS = {
    "Baggot Street": 2,
    "Blanchardstown": 16,
    "CHQ": 10,
    "Cork City": 15,
    "Drumcondra": 9,
    "Dundrum": 7,
    "Georges Street": 5,
    "Jervis Street": 17,
    "Liffey Valley": 14,
    "Macken Steet": 3,
    "Portobello": 8,
    "Ranelagh": 1,
    "Sallynoggin": 13,
    "Stillorgan": 11,
    "Swords": 4,
    "Tallaght": 12
    }

ACTION_WAIT=10
DEFAULT_CHROME_OPTIONS = [
    #"--headless", 
    #"--single-process", 
    #"--disable-gpu", 
    #"--no-sandbox"
    ]


class FullyBookedException(Exception):
    pass

class AlreadyBookedException(Exception):
    pass

class NotYetAvailableException(Exception):
    pass

class GymSiteNotFound(Exception):
    pass

class WrongTimeSlotException(Exception):
    pass

class DailyLimitReachedException(Exception):
    pass

class WorkoutSession(object): 
    def __init__(self, site_name, time, date):
        try:
            self.time = time
            self.date = date
            self.site_name = site_name
            self.site_id = SITE_IDS[site_name]
        except KeyError:
            raise GymSiteNotFound("Gym Site not found.")


class FlyefitPal(object):
    def __init__(self, email, password, wait=ACTION_WAIT, chrome_options=[]):
        self.__email = email
        self.__password = password
        chrome_options = self.__construct_options(chrome_options)
        self.__driver = webdriver.Chrome(options=chrome_options)
        self.__driver.implicitly_wait(wait) 

    def __construct_options(self, options):
        options.extend(DEFAULT_CHROME_OPTIONS)
        chrome_options = webdriver.ChromeOptions()
        for opt in options:
            chrome_options.add_argument(opt)
        return chrome_options

    def __login(self):
        self.__driver.get(LOGIN_URL)
        self.__driver.find_element(By.NAME, "email_address").send_keys(self.__email)
        self.__driver.find_element(By.NAME, "password").send_keys(self.__password)
        self.__driver.find_element(By.NAME, "log_in").click()

    def __go_to_bookout_page(self, workout):
        self.__driver.get(BOOKING_URL)
        
        # find 3 drop down selectors TYPE, SITE, DATE
        site_selector = self.__driver.find_elements(By.CLASS_NAME, "selectric-wrapper")[1]
        site_selector.click() # click on SITE to show drop down

        # find site options and select appropriate one
        site_choices = site_selector.find_elements(By.TAG_NAME, "li")
        for choice in site_choices:
            if choice.text == workout.site_name:
                choice.click()
                break

    def __construct_booking_url(self, workout):
        splitted = self.__driver.current_url.split("/")
        splitted[-1] = workout.date
        splitted[-2] = str(workout.site_id)
        return "/".join(splitted)

    def __find_book_button(self, time_slot):
        # find all buttons for all time slots 
        buttons = self.__driver.find_elements(By.CLASS_NAME, "btn-primary")
        for btn in buttons:
            if btn.get_attribute("data-course-time") == time_slot:
                return btn
        return None

    def __book_session(self, workout):
        self.__driver.get(self.__construct_booking_url(workout))

        button = self.__find_book_button(workout.time)
        if not button:
            raise WrongTimeSlotException("Time slot not found for this gym location.")
        elif button.text == "Booked":
            raise AlreadyBookedException("Time slot is already booked.")
        elif button.text == "Fully Booked":
            raise FullyBookedException("Time slot is fully booked out.")
        elif button.text == "Not Yet Open":
            raise NotYetAvailableException("Time slot not open yet.")

        # click the Book button
        button.click() 
        # Confirm booking button
        confirm_button = self.__driver.find_element(By.ID, "book_class")
        sleep(1) # required as sometimes the button doesn't load on time
        if not confirm_button.text:
            raise DailyLimitReachedException("You've already booked once for that day.")
        confirm_button.click()

    def book_workout(self,workout_session):
        self.__login()
        self.__go_to_bookout_page(workout_session)
        self.__book_session(workout_session)
        self.__driver.quit()
