import requests
from pprint import pprint
from pyppeteer import launch
import asyncio
from random import randint


def get_info_banks_for_city(city):
    url = f'https://belarusbank.by/open-banking/v1.0/atms?city={city}'
    banks = requests.get(url).json()['Data']['ATM']

    data = []
    addresses = []

    for bank in banks:
        place = bank['Address']['addressLine']
        address = bank['Address']['townName'] + ' ' + bank['Address']['streetName'] + ' '+ bank['Address']['buildingNumber']
        latitude_coord = bank['Address']['Geolocation']['GeographicCoordinates']['latitude']
        longitude_coord = bank['Address']['Geolocation']['GeographicCoordinates']['longitude']
        phone = bank['ContactDetails']['phoneNumber']
        services_list = [servic['serviceType'] for servic in bank['Services']]
        cards_list = bank['cards']

        data.append({
            'Место': place,
            'Адрес': address,
            'Координата х': latitude_coord,
            'координата у': longitude_coord,
            'Телефон': phone,
            'Услуги': services_list,
            'Карты': cards_list
        })
        addresses.append(address)
    result = _convert_data_to_text(data)
    
    return result, addresses


def _convert_data_to_text(data):
    result = []
    for bank in data:
        text = f"""
        Место: {bank['Место']}\n\n
Адрес: {bank['Адрес']}\n\n
Телефон: {bank['Телефон']}\n\n
Услуги: {', '.join(bank['Услуги'])}\n\n
'Карты': {', '.join(bank['Карты'])}
        """
        result.append(text)
    return result

def is_valid_city(city):
    url = f'https://belarusbank.by/open-banking/v1.0/atms?city={city}'
    responce = requests.get(url)
    resp_js = responce.json()
    return resp_js['Data']['ATM'] != None
    

async def _get_photo_place(address):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.google.by/maps/')

    send_text = await page.waitForSelector('#gs_lc50')
    await send_text.type(address)
    button = await page.waitForSelector('#searchbox-searchbutton')

    await button.click()
    await asyncio.sleep(3)

    await page.screenshot({'path':f'{address.replace(" ", "_")}.jpg'})

    await browser.close()

async def create_task(adresses):
    tasks = []
    for adress in adresses:
        task = asyncio.create_task(_get_photo_place(adress))
        tasks.append(task)
    asyncio.gather(*tasks)
