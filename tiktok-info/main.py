from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import sys




driver = webdriver.Chrome()


base_url = 'https://www.tiktok.com/'


def main(user_name):
    try: 
        datas = []
        print(f"Getting {username}'s metrics")
        driver.get(f'{base_url}@{user_name}')


        latest_posts_class_name = 'css-1cwtd61-5e6d46e3--DivVideoFeedV2'
        single_video_container_class_name = 'css-11p5e9y-5e6d46e3--DivItemContainerV2'
        wait = WebDriverWait(driver, 30)

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'css-17tvrad-5e6d46e3--H3CountInfos')))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, latest_posts_class_name)))

        h3 = driver.find_element(By.CLASS_NAME, 'css-17tvrad-5e6d46e3--H3CountInfos')

        divs = h3.find_elements(By.TAG_NAME, 'div')

        print(divs)
        data = {}
        data['name'] = username
        for div in divs:
            title = div.find_element(By.TAG_NAME, 'span').text
            print(title)
            val = div.find_element(By.TAG_NAME, 'strong').text
            data[title] = val

        

        print(latest_posts_class_name)

        driver.implicitly_wait(30)
        posts_container = driver.find_element(By.CLASS_NAME, latest_posts_class_name)
        posts = posts_container.find_elements(By.CLASS_NAME, single_video_container_class_name)

        print("POSTS", posts)
        latest_videos = []
        threashold = 10

        for pidx, post in enumerate(posts, start=1):
            if pidx > threashold:
                break
            video_link = post.find_element(By.TAG_NAME, 'a').get_attribute('href')
            latest_videos.append(video_link)

        data['latest_videos'] = latest_videos



        
        print(data)
        datas.append(data)


        print(datas)
        df = pd.DataFrame(datas)

        df.to_csv('output.csv', index=False)
            

        print("Hello from web-scraping!", data)
    except Exception as e:
        print(e)
    
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("please provide tiktoker username")
        sys.exit(1)

    username = sys.argv[1]
    main(username)
