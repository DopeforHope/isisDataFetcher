from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re

#IsisLink object
#attributes: link - url, type - later specified, right now only 'pdf'
class IsisLink():
    def __init__(self, link, type):
        self.link = link
        self.type = type #pdf,

    def __repr__(self):
        return "IsisLink{link: " + self.link + ", type: " + self.type + "}"

#IsisCourse object
#attributes: link - url, name - name of the course
class IsisCourse():
    def __init__(self, link, name):
        self.link = link
        self.name = name

    def __repr__(self):
        return "IsisCourse{link: " + self.link + ", name: " + self.name + "}"


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
        self.driver.find_element_by_id('username').send_keys(name)
        self.driver.find_element_by_id('password').send_keys(pw)
        self.driver.find_element_by_id('login-button').click()

        #TODO: implement check for right login

    def get_to_start_seite(self):
        return self.driver.get("https://isis.tu-berlin.de/my/index.php?mynumber=-2")

    def get_course_and_links(self):

        self.get_to_start_seite()

        course_container = self.driver.find_element_by_xpath("//*[contains(concat(' ', @class, ' '), 'course_list')]")

        course_list = course_container.find_elements_by_xpath(".//*[contains(@id,'course')]")
        course_array = np.asarray(course_list)

        result=[]
        for i in range(len(course_array)):
            title = course_array[i].find_element_by_tag_name("a").get_attribute("title")
            link = course_array[i].find_element_by_tag_name("a").get_attribute("href")
            result.append(IsisCourse(link, title))

        return result

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

    #returns IsisLink() for each link specified type from a course
    def get_all_links_from_course(self, url):

        #goto url
        self.driver.get(url)

        #extract all element with a href attribute
        linkElements = self.driver.find_elements_by_xpath("//*[@href]")

        result = []
        for linkElem in linkElements:
            link = linkElem.get_attribute('href')

            if(self.check_for_pdf_link(link)):
                isisObj = IsisLink(link, 'pdf')
                result.append(isisObj)
            elif(self.check_for_mod_link(link)):
                type = self.check_mod_link_for_type(linkElem)
                if(type != None):
                    isisObj = IsisLink(link, type)
                    result.append(isisObj)
        return result

    #checks link for pdf extension
    #input: link
    #output: boolean
    def check_for_pdf_link(self, link):
        if re.match('^.*\.(pdf)', link):
            return True
        else:
            return False

    #matches Link with regEx for known Isis/moodle links
    #input: link
    #output: boolean
    def check_for_mod_link(self, link):
        if re.match('(^https:\/\/isis\.tu-berlin\.de\/mod\/resource\/.*|^https:\/\/isis\.tu-berlin\.de\/mod\/url\/.*)', link):
            return True
        else:
            return False

    #gets the icon of a webelem and checks with known icon for type
    #input: WebElement - <a> tag with (^https:\/\/isis\.tu-berlin\.de\/mod\/resource\/.*|^https:\/\/isis\.tu-berlin\.de\/mod\/url\/.*) link
    #output: type - see IsisLink()
    # TODO: add more types
    def check_mod_link_for_type(self, wElem):
        img = wElem.find_element_by_tag_name('img')
        icon = img.get_attribute('src')
        print(icon)
        if(icon == "https://isis.tu-berlin.de/theme/image.php/isis_theme/core/1476377631/f/pdf-24"):
            return 'pdf'
        else:
            return None




df = IsisDataFetcher()
courseAndLinks = df.get_course_and_links()
print(courseAndLinks[0])
lFromCourse = df.get_all_links_from_course(courseAndLinks[0].link)
print(lFromCourse)