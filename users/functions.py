import requests
from .models import User, Preferences

API_URL = 'https://invelonjobinterview.herokuapp.com/api/post_test'

EMAIL_REGEX = r'^[\w-_\.]+@([\w-]+\.)+[\w-]$'
AFFILIATE_CHOICES = ['true', 'false']

ERROR_EMPTY_FIELDS = {"error": "Fill all fields",}
ERROR_INVALID_PREFERENCES = {"error": "Invalid preferences",}
ERROR_DUPLICATED_PREFERENCES = {"error": "Duplicated preferences",}
ERROR_DUPLICATED_USER = {"error": "User already exist",}
ERROR_DUPLICATED_EMAIL = {"error": "Email already exist",}
ERROR_AFFILIATE_NOT_BOOL = {"error": "Expected string bool affiliate",}


def __empty_fileds(name: str, email: str, prefereces: str, affiliate: str) -> bool:
    return name.strip() == "" or email.strip() == "" or prefereces.strip() == "" or affiliate.strip() == ""


def __is_invalid(preferences: list) -> bool:
    l_pref = preferences.split(',')
    greater = [0 <= int(x) <= 7 for x in l_pref]
    both = [int(x)%2 == 0 for x in l_pref]
    return all(greater) and (not True in both or not False in both)


def __is_repeated(preferences: str) -> bool:
    preferences.strip()
    l_pref = preferences.split(',')
    l_pref.sort()
    for i, n in enumerate(l_pref[:-1]):
        if n == l_pref[i+1]:
            return True
    return False


def __exists_user(name: str) -> bool:
    return User.objects.filter(name=name).exists()


def __exists_email(email: str) -> bool:
    return User.objects.filter(email=email).exists()


def __is_bool_str(affiliate: str) -> bool:
    return affiliate in AFFILIATE_CHOICES


def __get_adapted_json(name: str, email:str, preferences: str, affiliate: str) -> dict:
    data = {
        "name": name,
        "email": email,
        "preferences": preferences,
        "affiliate": affiliate,
        }
    
    response = requests.post(url=API_URL, data=data)

    return response.json()


def f_post_user(name: str, email:str, preferences: str, affiliate: str) -> dict:
    if __empty_fileds(name, email, preferences, affiliate):
        return ERROR_EMPTY_FIELDS

    if __exists_user(name):
        return ERROR_DUPLICATED_USER
    
    if __exists_email(name):
        return ERROR_DUPLICATED_EMAIL
    
    if __is_invalid(preferences):
        return ERROR_INVALID_PREFERENCES
    
    if __is_repeated(preferences):
        return ERROR_DUPLICATED_PREFERENCES
    
    if not __is_bool_str(affiliate):
        return ERROR_AFFILIATE_NOT_BOOL
    
    json = __get_adapted_json(name, email, preferences, affiliate)

    user = User(name=json['name'],
                email=json['email'],
                affiliate=json['affiliate'])
    user.save()

    for preference in json['preferences']:
        tmp_pref = Preferences(user=user, name=preference)
        tmp_pref.save()
    
    return json


def __get_user_dict(user: User, preferences: list[Preferences]) -> dict:
    return {
        'name': user.name,
        'email': user.email,
        'preferences': [pref['name'] for pref in preferences],
        'affiliate': user.affiliate,
    }


def f_get_users() -> list[str, dict]:
    _return = {'users':[]}

    users = User.objects.all()

    for user in users:
        preferences = Preferences.objects.filter(user=user).values()
        _return['users'].append(__get_user_dict(user, preferences))

    return _return
