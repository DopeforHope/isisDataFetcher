from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


class IsisDataFetcher():

    def __init__(self):
        name = ""
        pw = ""
        while((name == "") | (pw == "")):
            name = input("Loginname: ")
            print("Login :", name)
            pw = input("Password: ")  # TODO: nicer password taking
            print("PW :", pw)

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")

        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])

        # goto ISIS page because direct access is not permitted
        self.driver.get("https://isis.tu-berlin.de/")

        # wait until page is up
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.content")))

        # click shibbolethbutton to go to login page
        self.driver.find_element_by_id('shibbolethbutton').click()

        # Fill the login form and submit it
        self.driver.find_element_by_name('j_username').send_keys(name)
        self.driver.find_element_by_id('password').send_keys(pw)
        self.driver.find_element_by_name('Submit').submit()

    def get_to_start_seite(self):
        return self.driver.get("https://isis.tu-berlin.de/my/index.php?mynumber=-2")

    def get_course_and_links(self):

        self.get_to_start_seite()

        course_container = self.driver.find_element_by_xpath("//*[contains(concat(' ', @class, ' '), 'course_list')]")

        course_list = course_container.find_elements_by_xpath(".//*[contains(@id,'course')]")
        course_array = np.asarray(course_list)
        title = []
        links = []

        for i in range(len(course_array)):
            title.append(course_array[i].find_element_by_tag_name("a").get_attribute("title"))
            links.append(course_array[i].find_element_by_tag_name("a").get_attribute("href"))

        title_arr = np.asarray(title)
        link_arr = np.asarray(links)

        return np.vstack((title_arr, link_arr)).T

        # tAndLArray[0] is your first course with link
        # - Example:
        # ['Programmierpraktikum Cyber-Physical Systems SS16', 'https://isis.tu-berlin.de/course/view.php?id=6852']

    def get_weeks_and_pdfs(self, url):

        # goto course page
        self.driver.get(url)

        week_container = self.driver.find_element_by_xpath('//*[@id="main"]/div/div/ul')

        # weeks = week_container.find_elements_by_xpath(".//*[contains(@id,'section')]")
        weeks = week_container.find_elements_by_xpath("//li")

        weeks = np.asarray(weeks)

        week_titles = []
        week_pdfs = []

        for i in range(len(weeks)):
            w_title = weeks[i].get_attribute("aria-label")
            if(w_title is not None):
                pdf_links = []

                week_titles.append(w_title)
                week_content = weeks[i].find_element_by_class_name("content").find_element_by_tag_name("ul")
                week_content = np.asarray(week_content.find_elements_by_xpath(".//*[contains(@id,'module')]"))
                for wE in week_content:
                    # print(wE.get_attribute("class"))
                    if("resource" in wE.get_attribute("class")):
                        pdf_links.append(wE.find_element_by_tag_name("a").get_attribute("href"))
                week_pdfs.append(pdf_links)

        week_titles = np.asarray(week_titles)
        week_pdfs = np.asarray(week_pdfs)

        return (np.vstack((week_titles, week_pdfs)).T)

    def make_folder_title(self, titles):
        results = []
        for i in range(len(titles)):
            results.append(''.join([c for c in titles[i] if not(c.islower() | c.isspace())]))
        return np.asarray(results)

