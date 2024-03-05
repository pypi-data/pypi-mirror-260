import toml
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
from datetime import datetime


class TextToImageGenerator:
    def __init__(self,prompt:str, n:int=3):
        self.prompt = prompt
        self.images_urls = []
        self.n = n
        self.load_config()
        self.initialize()





    def load_config(self):
        with open('config.toml', 'r') as file:
            self.config = toml.load(file)
        print("Configuration Done")

    def initialize(self):
        options = ChromeOptions()
        options.add_argument('--headless')
       
        self.driver = Chrome(options=options)

        print("Initialization")

    def startBot(self):
        print("1- The Bot has started")
        try:
            self.driver.get(self.config['urls']['generate'])
        except Exception as e:
            print("Error in Website Access\n", str(e))

        try:
            input_box = self.driver.find_element(By.XPATH,self.config['elements']['prompt_box'])
            input_box.send_keys(self.prompt)
            sleep(1)
            input_box.send_keys(Keys.ENTER)
            sleep(1)
        except Exception as e:
            print("Error in finding the input search box\n",str(e))

        print("2- Getting the Images")
        try:
            # get the specified images
            images = self.driver.find_elements(By.XPATH,self.config['elements']['results_imgs'])

            for i, image in enumerate(images[:self.n]):
                img = image.find_element(By.TAG_NAME,'img')
                # get the src value
                url = img.get_attribute("src")
                self.images_urls.append(url)
                # print(f'Image {i+1}:\t{url}')

            sleep(5)
        except Exception as e:
            print("Error in Getting Images")
        
        self.driver.quit()

        print("3- Operation Completed Successfully")

    def get_urls(self):
        return self.images_urls


    def download_images(self):
        try:
            for image_url in self.images_urls:
                destination_file = f"downloaded_image_{str(datetime.now()).split('.')[0].replace('-','_').replace(':','_').replace(' ','_')}.jpg"
                response = requests.get(image_url)

                if response.status_code == 200:
                    with open(destination_file, 'wb') as f:
                        f.write(response.content)
                    print(f"Image downloaded successfully and saved as {destination_file}")
                else:
                    print(f"Failed to download image. Status code: {response.status_code}")

        except Exception as e:
            print("4- Error in Downloading Images")

            
if __name__ == '__main__':
    generator = TextToImageGenerator('A dog with glasses',5)
    generator.startBot()
    generator.download_images()
    
    