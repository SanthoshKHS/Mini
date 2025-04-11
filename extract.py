from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from amazoncaptcha import AmazonCaptcha
import time
def extractor(url):
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
       
        button1=driver.find_element(By.XPATH, '//a[@data-hook="see-all-reviews-link-foot"]')
        button1.click()
        link=driver.find_element(By.XPATH,"//div[@class='a-row a-text-center']//img").get_attribute('src')
        capt=AmazonCaptcha.fromlink(link)
        value=AmazonCaptcha.solve(capt)
        input_field=driver.find_element(By.ID,"captchacharacters").send_keys(value)
        
        input_field2=driver.find_element(By.ID,"ap_email_login").send_keys("")
        button2=driver.find_element(By.ID,"continue")
        button2.click()
        
        input_field3=driver.find_element(By.XPATH, "//input[@id='ap_password']").send_keys("")
        if input_field3:
            print("hello")
        button3=driver.find_element(By.ID,"signInSubmit")
        button3.click()
        time.sleep(10)
        reviewsbutton = driver.find_element(By.CSS_SELECTOR, 'a[data-hook="see-all-reviews-link-foot"]')
        reviewsbutton.click()
        reviews=[]
        for i in range(6):
            review_elements=driver.find_element(By.XPATH, "//span[@data-hook='review-body']")
            for k in review_elements:
                reviews.append(k.text)
            print(reviews)
            next_page_button = driver.find_element(By.XPATH, "//li[@class='a-last']/a")
            time.sleep(2)
            next_page_button.click()
            time.sleep(3)
        return reviews
    except Exception as e:
        print(e)

