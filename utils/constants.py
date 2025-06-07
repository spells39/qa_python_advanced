headers = {'x-api-key': 'reqres-free-v1'}

local_url = 'http://localhost:8000'

unknown_users = [{'id': 23, 'name': 'some_user'}, {'id': 5, 'name': 'aboba_user'}]

delete_ids = {'exist': [1, 2, 5, 6, 10],
              'not_exist': [123456, 798564, 85273, 87446, 228]}

id_with_status = [(10, 200), (5, 200), (132456, 404), (123546987, 404)]

data_for_test_pagination = [(1, 5, [1, 2, 3, 4, 5]),
                            (2, 5, [6, 7, 8, 9, 10]),
                            (1, 2, [1, 2]),
                            (2, 2, [3, 4]),
                            (3, 2, [5, 6]),
                            (4, 2, [7, 8]),
                            (5, 2, [9, 10]),]

users_for_create = [
    {
        "id": 1,
        "name": "Johnny Silverhand",
        "role": "Rockerboy",
        "status": "active",
        "email": "johnny@afterlife.net"
    },
    {
        "id": 2,
        "name": "Alt Cunningham",
        "role": "Netrunner",
        "status": "inactive",
        "email": "alt@soulkiller.ai"
    },
    {
        "id": 3,
        "name": "Rogue Amendiares",
        "role": "Fixer",
        "status": "active",
        "email": "rogue@afterlife.net"
    },
    {
        "id": 4,
        "name": "Adam Smasher",
        "role": "Cyborg",
        "status": "wanted",
        "email": "smasher@arasaka.com"
    },
    {
        "id": 5,
        "name": "Judy Alvarez",
        "role": "Techie",
        "status": "active",
        "email": "judy@lizzies.mox"
    }
]

updated_users = [
    (1, {"name": "Walter", "role": "teacher", "status": "non-active", "email": "walt3r@example.com"}),
    (2, {"name": "Jesse", "role": "cook", "status": "active", "email": "j3$$3@example.com"}),
    (3, {"name": "Saul", "role": "lawyer", "status": "active", "email": "goodman@example.com"}),
    (4, {"name": "Mike", "role": "bodyguard", "status": "non-active", "email": "mik3@example.com"}),
    (5, {"name": "Gus", "role": "manager", "status": "non-active", "email": "amogus@example.com"})
]