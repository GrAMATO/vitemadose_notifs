import time
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select
import os


def search_slot(url):
    """Permet de rechercher un créneau dispo, provient de vitemadose."""
    
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
    
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.binary_location = '.apt/usr/bin/google-chrome-stable'
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--remote-debugging-port=9230")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("window-size=1920,1000")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(1)
    browser.maximize_window()
    # Bouton Cookies
    browser.get_screenshot_as_file("screenshotc.png")
    browser.find_element_by_xpath("//button[@id ='didomi-notice-disagree-button']").click()
    #btn = browser.find_elements_by_xpath("//button[contains(.,'ACCEPTER')]")

    # Sélectionner age
    browser.get_screenshot_as_file("screenshot.png")
    select_element = browser.find_element_by_xpath("//select[@id ='booking_motive_category']")
    #select_element = browser.find_element_by_id("booking_motive_category")
    select_object = (Select(select_element))

    text_select = select_object.options[2].text
    select_object.select_by_visible_text(text_select)
    time.sleep(1)
    
   # Sélectionner motif
    select_element = browser.find_element_by_id("booking_motive")
    select_object = (Select(select_element))
    
    text_select = select_object.options[3].text
    select_object.select_by_visible_text(text_select)
    
    time.sleep(1)

    # Bouton prochaines dispos
    try:
        btn = browser.find_elements_by_xpath("//button[contains(.,'Prochain RDV')]")
        btn[0].click()
    except:
        print("Pas de bouton Prochain RDV")

    time.sleep(0)

    # Premier slot dispo
    
    try:
        slots = browser.find_elements_by_class_name("availabilities-slot")
        slot = slots[0].get_attribute("title")
        browser.stop_client()
        browser.close()
        browser.quit()
        return slot
    except:
        print("Pas de rdv dispo")
        browser.stop_client()
        browser.close()
        browser.quit()
        return "non"


def sms_fun(rdv, url):
    if rdv == "erreur":
        print(rdv)
        build_url_messenger("Erreur, processus interrompu.", api_keys)
    elif rdv == "non":
        pass
    else:
        build_url_messenger("RDV disponible le " + rdv + " au centre " + url, api_keys)
        time.sleep(700)


def build_url_messenger(message, api_keys):
    """Envoie un message"""
    list_url = []
    for api_key in api_keys:
        part1 = "https://api.callmebot.com/facebook/send.php?&apikey=" 
        part2 = "&text="
        message_clean = message.replace(" ", "+")
        requests.get(part1 +  api_key + part2 + message_clean)


def main(url):
    while True:
        time.sleep(15)
        try:
            rdv = search_slot(url)
            print("phase1 ", rdv)
            sms_fun(rdv, url)
        except Exception as e:
            print("Exception1 ", e)
            print("erreur 1")
            time.sleep(61)
            while True:
                try:
                    sms_fun(rdv, url)
                except:
                    time.sleep(61)
                    print("Exception1 ", e)
                    print("erreur 1")
            try:
                rdv = search_slot(url)
                print("phase2 ", rdv)
                sms_fun(rdv)
            except Exception as e:
                print("Exception2 ", e)
                sms_fun("erreur")
                break
                
api_keys = []          
                
url = "" # URL du centre de vaccination doctolib 

main(url)

