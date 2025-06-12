headers = {'x-api-key': 'reqres-free-v1'}

local_url = 'http://localhost:8000'

unknown_users = [{'id': 23, 'name': 'some_user'}, {'id': 5, 'name': 'aboba_user'}]

user_ids = {'exist': [2, 4, 5, 7, 8],
            'not_exist': [123456, 798564, 85273, 87446, 228]}

id_with_status = [(10, 200), (5, 200), (1, 200), (188, 404), (132456, 404), (123546987, 404)]

data_for_test_pagination = [(1, 5, [1, 2, 3, 4, 5]),
                            (2, 5, [6, 7, 8, 9, 10]),
                            (1, 2, [1, 2]),
                            (2, 2, [3, 4]),
                            (3, 2, [5, 6]),
                            (4, 2, [7, 8]),
                            (5, 2, [9, 10]),]

users_for_create = [
    {
        "name": "Johnny Silverhand",
        "role": "Rockerboy",
        "status": "active",
        "email": "johnny@afterlife.net",
        "avatar": "https://i.imgur.com/KeJjF3a.jpg"
    },
    {
        "name": "Alt Cunningham",
        "role": "Netrunner",
        "status": "inactive",
        "email": "alt@soulkiller.ai",
        "avatar": "https://i.imgur.com/9Rk8YfN.jpg"
    },
    {
        "name": "Rogue Amendiares",
        "role": "Fixer",
        "status": "active",
        "email": "rogue@afterlife.net",
        "avatar": "https://i.imgur.com/JrTJ5yW.jpg"
    },
    {
        "name": "Adam Smasher",
        "role": "Cyborg",
        "status": "wanted",
        "email": "smasher@arasaka.com",
        "avatar": "https://i.imgur.com/Vm4Bd9L.jpg"
    },
    {
        "name": "Judy Alvarez",
        "role": "Techie",
        "status": "active",
        "email": "judy@lizzies.mox",
        "avatar": "https://i.imgur.com/XyT7k8R.jpg"
    },
    {
        "name": "V",
        "role": "Mercenary",
        "status": "Wanted",
        "email": "v@nomad.tech",
        "avatar": "https://i.imgur.com/LpZ3vQ2.jpg"
    },
    {
        "name": "Panam Palmer",
        "role": "Nomad",
        "status": "On Mission",
        "email": "panam@aldecaldos.net",
        "avatar": "https://i.imgur.com/QzY9vGp.jpg"
    },
    {
        "name": "River Ward",
        "role": "Cop",
        "status": "On Duty",
        "email": "river@ncpd.gov",
        "avatar": "https://i.imgur.com/2sPm7dT.jpg"
    },
    {
        "name": "Takemura Goro",
        "role": "Ex-Arasaka Agent",
        "status": "Laying Low",
        "email": "takemura@ronin.jp",
        "avatar": "https://i.imgur.com/5vZb1Yx.jpg"
    },
    {
        "name": "Hanako Arasaka",
        "role": "Corpo",
        "status": "In Meeting",
        "email": "hanako@arasaka.corp",
        "avatar": "https://i.imgur.com/7KmWt6F.jpg"
    }
]

updated_users = [
    (1, {
         "name": "Walter",
         "role": "teacher",
         "status": "non-active",
         "email": None,
         "avatar": "https://example.com/avatars/walter.png"}),
    (3, {
         "name": "Jesse",
         "role": "cook",
         "status": None,
         "email": "j3$$3@example.com",
         "avatar": "https://example.com/avatars/jesse.png"}),
    (6, {
         "name": "Saul",
         "role": None,
         "status": "active",
         "email": "goodman@example.com",
         "avatar": "https://example.com/avatars/saul.png"}),
    (9, {
         "name": None,
         "role": "bodyguard",
         "status": "non-active",
         "email": "mik3@example.com",
         "avatar": "https://example.com/avatars/mike.png"}),
    (10, {
         "name": "Gus",
         "role": None,
         "status": None,
         "email": "amogus@example.com",
         "avatar": None})
]

invalid_data = [
    {"name": "Test", "role": "Tester", "status": "active", "email": "invalid-email", "avatar": "https://valid.url"},
    {"name": "Test", "role": "Tester", "status": "active", "email": "valid@example.com", "avatar": "invalid-url"},
    {"name": "Test", "role": "Tester", "status": "active", "email": "valid@example.com"}
]