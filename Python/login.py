from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


class isisDataFetcher():

    def __init__(self):
        name = ""
        pw = ""
        while((name == "") | (pw == "")):
            name = input("Loginname: ")
            print("Login :", name)
            pw = input("Password: ")#TODO: nicer password taking
            print("PW :", pw)

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")

        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])

        #goto isis page because direct access is not permitted
        self.driver.get("https://isis.tu-berlin.de/")

        #wait until page is up
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.content")))

        #click shibbolethbutton to go to login page
        self.driver.find_element_by_id('shibbolethbutton').click()


        # Fill the login form and submit it
        self.driver.find_element_by_name('j_username').send_keys(name)
        self.driver.find_element_by_id('password').send_keys(pw)
        self.driver.find_element_by_name('Submit').submit()

    def getToStartSeite(self):
        return self.driver.get("https://isis.tu-berlin.de/my/index.php?mynumber=-2")

    def getCourseAndLinks(self):

        self.getToStartSeite()

        courseContainer = self.driver.find_element_by_class_name("course_list")

        courseList = courseContainer.find_elements_by_xpath(".//*[contains(@id,'course')]")
        courseArray = np.asarray(courseList)
        title = []
        links = []

        for i in range(len(courseArray)):
            title.append(courseArray[i].find_element_by_tag_name("a").get_attribute("title"))
            links.append(courseArray[i].find_element_by_tag_name("a").get_attribute("href"))

        titleArr = np.asarray(title)
        linkArr = np.asarray(links)

        return np.vstack((titleArr,linkArr)).T

        #tAndLArray[0] is your first course with link
        # - Example:['Programmierpraktikum Cyber-Physical Systems SS16', 'https://isis.tu-berlin.de/course/view.php?id=6852']

    def getWeeksAndPDFs(self, url):

        #goto course page
        self.driver.get(url)

        weekContainer = self.driver.find_element_by_class_name("weeks")

        weeks = weekContainer.find_elements_by_xpath(".//*[contains(@id,'section')]")

        weeks = np.asarray(weeks)

        weekTitles = []

        weekPdfs = []


        for i in range(len(weeks)):
            wTitle = weeks[i].get_attribute("aria-label")
            if(wTitle != None):
                pdfLinks = []

                weekTitles.append(wTitle)
                weekContent = weeks[i].find_element_by_class_name("content").find_element_by_tag_name("ul")
                weekContent = np.asarray(weekContent.find_elements_by_xpath(".//*[contains(@id,'module')]"))
                for wE in weekContent:
                    #print(wE.get_attribute("class"))
                    if("resource" in wE.get_attribute("class")):
                        pdfLinks.append(wE.find_element_by_tag_name("a").get_attribute("href"))
                weekPdfs.append(pdfLinks)

        weekTitles = np.asarray(weekTitles)
        weekPdfs = np.asarray(weekPdfs)

        return(np.vstack((weekTitles,weekPdfs)).T)

    def makeFolderTitle(self, titles):
        results = []
        for i in range(len(titles)):
            results.append(''.join([c for c in titles[i] if not(c.islower() | c.isspace())]))
        return np.asarray(results)



dataF = isisDataFetcher()
tAndLArray = dataF.getCourseAndLinks()

print(tAndLArray)
print(tAndLArray[:,0])
print(dataF.makeFolderTitle(tAndLArray[:,0]))