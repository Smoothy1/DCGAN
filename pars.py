import json
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re



def avito_get_first_news():
    host = 'https://www.avito.ru'
    options = Options()
    options.add_argument('--headless')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Chrome(executable_path=r'C:/Users/Admin/geckodriver.exe', options=options)
    driver.implicitly_wait(10)
    url = "https://www.avito.ru/samara/avtomobili/do-200000-rubley-ASgCAgECAUXGmgwWeyJmcm9tIjowLCJ0byI6MjAwMDAwfQ?cd=1&moreExpensive=1&radius=100&s=104&user=1"
    driver.get(url)
    soup = bs(driver.page_source, "lxml")
    articles_cards = soup.find_all('div', class_ = 'iva-item-content-rejJg')
    driver.close()
    avito_dict = {}
    for article in articles_cards:
        url_class = article.find('a', class_='iva-item-sliderLink-uLz1v')
        infa = article.find('div', class_ = 'iva-item-autoParamsStep-WzfS8').text
        ad_y = article.find('div', class_ = 'iva-item-titleStep-pdebR').text
        price1 = article.find('span', class_ = 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL').text
        price_str = ''.join(re.findall('\d', price1))
        price = int(price_str)
        inf_split = infa.split(',')
        if inf_split[0] == 'Битый':
            probeg_tmp = inf_split[1]
        else:
            probeg_tmp = inf_split[0]
        prob = probeg_tmp.replace("\xa0", "")
        probeg = int(prob[:-2])
        name_m, year_str = ad_y.split(', ')
        year = int(year_str)
        name_url = host + url_class.get('href')
        article_id = name_url.split("/")[-1]


        avito_dict[article_id] = {
            "name_url": name_url,
            "name_m": name_m,
            "year": year,
            "price": price,
            "probeg": probeg
        }

    with open("avito_dict.json", "w") as file:
        json.dump(avito_dict, file, indent=4, ensure_ascii=False)
        
        
def avito_check_news_update():
    with open("avito_dict.json") as file:
        avito_dict = json.load(file)

    host = 'https://www.avito.ru'
    options = Options()
    options.add_argument('--headless')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver = webdriver.Chrome(executable_path=r'C:/Users/Admin/geckodriver.exe', options=options)
    driver.implicitly_wait(10)
    url = "https://www.avito.ru/samara/avtomobili/do-200000-rubley-ASgCAgECAUXGmgwWeyJmcm9tIjowLCJ0byI6MjAwMDAwfQ?cd=1&moreExpensive=1&radius=100&s=104&user=1"
    driver.get(url)
    #driver.execute_script(f"location.href='{url}';")
    soup = bs(driver.page_source, "lxml")
    articles_cards = soup.find_all('div', class_ = 'iva-item-content-rejJg')
    driver.close()
    
    avito_fresh_news = {}
    for article in articles_cards:
        url_class = article.find('a', class_='iva-item-sliderLink-uLz1v')
        name_url = host + url_class.get('href')
        article_id = name_url.split("/")[-1]

        if article_id in avito_dict:
            continue
        else:
            infa = article.find('div', class_ = 'iva-item-autoParamsStep-WzfS8').text
            ad_y = article.find('div', class_ = 'iva-item-titleStep-pdebR').text
            price1 = article.find('span', class_ = 'price-text-_YGDY text-text-LurtD text-size-s-BxGpL').text
            price_str = ''.join(re.findall('\d', price1))
            price = int(price_str)
            inf_split = infa.split(',')
            if inf_split[0] == 'Битый':
                probeg_tmp = inf_split[1]
            else:
                probeg_tmp = inf_split[0]
            prob = probeg_tmp.replace("\xa0", "")
            probeg = int(prob[:-2])
            name_m, year_str = ad_y.split(', ')
            year = int(year_str)

            avito_dict[article_id] = {
                "name_url": name_url,
                "name_m": name_m,
                "year": year,
                "price": price,
                "probeg": probeg
            }

            avito_fresh_news[article_id] = {
                "name_url": name_url,
                "name_m": name_m,
                "year": year,
                "price": price,
                "probeg": probeg
            }

    with open("avito_dict.json", "w") as file:
        json.dump(avito_dict, file, indent=4, ensure_ascii=False)

    return avito_fresh_news




def drom_get_first_news():
    url = "https://samara.drom.ru/auto/all/?maxprice=200000&owner_type=1&distance=100"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    articles_cards = soup.find_all('a', class_='css-xb5nz8 ewrty961')
    drom_dict = {}
    for article in articles_cards:
        name_url = article.get('href')
        article_id = name_url.split("/")[-1]
        #req_s = requests.get(name_url)
        #soup_s = bs(req_s.text, "html.parser")
        #date = soup_s.find('div', class_ = 'css-pxeubi evnwjo70').text
        ad = article.find('div', class_ = 'css-1dv8s3l eyvqki91')
        ad_year = article.find('div', class_ = 'css-17lk78h e3f4v4l2')
        if ad_year == None: 
            continue
        else: 
            ad_y = ad_year.find('span').text
        price1 = ad.find('span', class_ = 'css-46itwz e162wx9x0').text
        price = ''.join(re.findall('\d', price1))
        name, year = ad_y.split(', ')


        drom_dict[article_id] = {
            "name_url": name_url,
            "name": name,
            "year": year,
            "price": price
            #"probeg": probeg
        }

    with open("drom_dict.json", "w") as file:
        json.dump(drom_dict, file, indent=4, ensure_ascii=False)
        
        
        
def drom_check_news_update():
    with open("drom_dict.json") as file:
        drom_dict = json.load(file)

    url = "https://samara.drom.ru/auto/all/?maxprice=200000&owner_type=1&distance=100"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    articles_cards = soup.find_all('a', class_='css-xb5nz8 ewrty961')
    
    drom_fresh_news = {}
    for article in articles_cards:
        name_url = article.get('href')
        article_id = name_url.split("/")[-1]

        if article_id in drom_dict:
            continue
        else:
            ad = article.find('div', class_ = 'css-1dv8s3l eyvqki91')
            ad_year = article.find('div', class_ = 'css-17lk78h e3f4v4l2')
            if ad_year == None: 
                continue
            else: 
                ad_y = ad_year.find('span').text
            price1 = ad.find('span', class_ = 'css-46itwz e162wx9x0').text
            price = ''.join(re.findall('\d', price1))
            name, year = ad_y.split(', ')

            drom_dict[article_id] = {
                "name_url": name_url,
                "name": name,
                "year": year,
                "price": price
                #"probeg": probeg
            }

            drom_fresh_news[article_id] = {
                "name_url": name_url,
                "name": name,
                "year": year,
                "price": price
                #"probeg": probeg
            }

    with open("drom_dict.json", "w") as file:
        json.dump(drom_dict, file, indent=4, ensure_ascii=False)

    return drom_fresh_news