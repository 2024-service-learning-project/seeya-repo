from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time


global chrome_options
chrome_options =webdriver.ChromeOptions()

chrome_options.add_argument('--headless')

# url 주면 이미지 crawled_images 에 저장하고, 후기 (str) return
def get_info(path:str): #delivery, price, size

    service = ChromeService(executable_path=ChromeDriverManager().install())
    # chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options) # <- options로 변경
    driver.get(path)
    driver.find_element(By.CSS_SELECTOR, ".product-detail__sc-12zk8dq-3.izNrin").click() # 팝업창 닫기
    
    scroll_height = 600 # 스크롤 단위 설정 (pixel 단위)
    de = False
    pr = False
    gu = False
    try:
        while True:
            delivery_info = driver.find_elements(By.CSS_SELECTOR, ".product-detail__sc-1ts9zk8-0.ddpAeO")
            price_info = driver.find_elements(By.CSS_SELECTOR, ".product-detail__sc-w5wkld-0.hgCYZm")
            size_info = driver.find_elements(By.CSS_SELECTOR, ".product-detail__sc-swak4b-0.KLfjI")
            guide = driver.find_elements(By.CSS_SELECTOR, ".product-detail__sc-17fds8k-0.PpQGA")
                    
            if delivery_info:
                delivery_info[0].screenshot("../crawled_images/delivery_info.png")
                #print("배송 정보를 찾아 스크린샷을 캡처했습니다.")
                de = True
            if price_info:
                price_info[0].screenshot("../crawled_images/price_info.png")
                #print("가격 정보를 찾아 스크린샷을 캡처했습니다.")
                pr = True
            if size_info:
                price_info[0].screenshot("../crawled_images/size_info.png")
                #print("사이즈 정보를 찾아 스크린샷을 캡처했습니다.")
                pr = True
            if guide:
                guide[0].screenshot("../crawled_images/guide.png")
                #print("Guide를 찾아 스크린샷을 캡처했습니다.")
                gu = True
                
            driver.execute_script(f"window.scrollBy(0, {scroll_height});") # 현재 뷰포트에서 스크롤
        
            end_of_page = driver.execute_script(
                "return window.innerHeight + window.scrollY >= document.body.offsetHeight;")
            if end_of_page:
                #print("페이지 끝에 도달했습니다.")
                break
        
            time.sleep(1)
    finally:
        driver.execute_script("window.scrollTo(0, 0);")  # 맨 위로 스크롤

    action = ActionChains(driver)
    review_contents = []
    
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            review_elements = driver.find_elements(By.CSS_SELECTOR, 'div.review-list-wrap div.review-list')
            
            for element in review_elements:
                review_text_elements = element.find_elements(By.CSS_SELECTOR, 'div.review-contents__text')
                for review_text in review_text_elements:
                    review_contents.append(review_text.text.replace('\n', ' '))
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    finally:
        driver.execute_script("window.scrollTo(0, 0);")
    
    # with open('review_contents.txt', 'w', encoding='utf-8') as file:
    #     for i, content in enumerate(review_contents, start=1):
    #         file.write(f"{i}.\n{content}\n\n")
    reviews = ''
    for i, content in enumerate(review_contents, start=1):
        reviews += f"{i}.\n{content}\n\n"

    return reviews
    

