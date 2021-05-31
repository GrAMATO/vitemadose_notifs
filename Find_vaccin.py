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
    
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(1)
    # Bouton Cookies
    btn = browser.find_elements_by_xpath("//button[contains(.,'Accepter & Fermer')]")
    btn[0].click()

    # Sélectionner motif
    select_element = browser.find_element_by_id("booking_motive")
    select_object = (Select(select_element))

    text_select = select_object.options[1].text
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
        browser.close()
        return slot
    except:
        print("Pas de rdv dispo")
        browser.close()
        return "non"
   

api_keys = [] # nécessaire pour recevoir les notifications, entrez la clé api donnée par callmebot

def sms_fun(rdv):
    if rdv == "erreur":
        print(rdv)
        build_url_messenger("Erreur, processus interrompu.", api_keys)
    elif rdv == "non":
        pass
    else:
        build_url_messenger("RDV disponible le " + rdv + " au centre " + url, api_keys)
        time.sleep(700)


def build_url_messenger(message, api_keys):
    """Envoie un message par messenger. Vous pouvez tout à fait adapter cette fonction pour whatsapp, telegram ou signal."""
    list_url = []
    for api_key in api_keys:
        part1 = "https://api.callmebot.com/facebook/send.php?&apikey=" 
        part2 = "&text="
        message_clean = message.replace(" ", "+")
        requests.get(part1 +  api_key + part2 + message_clean)


def main(url):
    while True:
        time.sleep(30)
        try:
            rdv = search_slot(url)
            print("phase1 ", rdv)
            sms_fun(rdv)
        except Exception as e:
            print("Exception1 ", e)
            print("erreur 1")
            time.sleep(60)
            try:
                rdv = search_slot(url)
                print("phase2 ", rdv)
                sms_fun(rdv)
            except Exception as e:
                print("Exception2 ", e)
                sms_fun("erreur")
                break
                
                
url = "" # URL du centre de vaccination doctolib 

main(url)
