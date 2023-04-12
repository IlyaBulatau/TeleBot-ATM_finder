import json

def users_db(data):
    with open(r'database\db.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def in_user_db(user_id):
    with open(r'database\db.json', encoding='utf-8') as file:
        try:
            src = json.load(file)
            for row in src:
                if user_id in row:
                    return True
            return False
        except:
            return False
        
def save_coordinate_user(user_id, lat, lon):
        with open(r'database\db.json', encoding='utf-8') as file:
            src = json.load(file)
            for user in src:
                    if user == user_id:
                    #   src[user] = {'lat': str(lat), 'lon': str(lon)}
                        src[user].update({'lat': str(lat), 'lon': str(lon)})
        with open(r'database\db.json', 'w', encoding='utf-8') as file:
            json.dump(src, file, indent=4, ensure_ascii=False)

