import requests
from pprint import pprint

# from config import load_config_yandex_key

# yandex_key = load_config_yandex_key()

def get_info_banks_for_city(city):
    url = f'https://belarusbank.by/open-banking/v1.0/atms?city={city}'
    banks = requests.get(url).json()['Data']['ATM']

    data = []

    for bank in banks:
        place = bank['Address']['addressLine']
        address = bank['Address']['streetName'] + ' '+ bank['Address']['buildingNumber']
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
    result = _convert_data_to_text(data)
    return result


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
    responce = requests.get(url).json()
    return responce['Data']['ATM'] != None
    