
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube
import os


driver_path = "" #give the path to the geckodriver executable 

def video_voice_only(url):
    '''
    Downloads the audio from a youtube video and returns the path to the audio file.
    '''
    file_paths = []
    new_path = ''
    video_caller = YouTube(url)
    try:
        audio = video_caller.streams.filter(only_audio=True).first()
        out_path = audio.download(output_path = 'audio_out/', filename = video_caller.title)
        new_path = 'audio_out/' + video_caller.title + '.mp3'
        os.rename(out_path, new_path)
    except:
        pass
    file_paths.append(new_path)
    return file_paths

#use selenium to get the urls of the video 
def get_urls(search_keyword, num_videos=1):
    '''
    This function uses Selenium to get the URLs of the videos from YouTube.
    '''
    driver = webdriver.Edge()

    url = f'https://www.youtube.com/results?search_query={search_keyword}'
    
    video_urls = []

    driver.get(url)

    while len(video_urls) < num_videos:
        try:
            # Wait for the presence of all video elements
            video_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a#video-title')))
            for element in video_elements:
                # Find all the elements
                vurl = element.get_attribute('href')
                video_urls.append(vurl)
                if len(video_urls) >= num_videos:
                    break
        except Exception as e:
            print("An error occurred:", e)
            break
    
    driver.quit()
    
    return video_urls


