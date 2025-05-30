headers = {'x-api-key': 'reqres-free-v1'}

local_url = 'http://localhost:8000'

unknown_users = [{'id': 23, 'name': 'some_user'}, {'id': 5, 'name': 'aboba_user'}]

delete_ids = [1, 2, 5, 6, 10]

id_with_status = [(23, 200), (5, 200), (11, 404), (89, 404)]

users_for_create = [
    {
        "id": 1,
        "name": "Tony Soprano",
        "role": "Mob Boss",
        "status": "Active"
    },
    {
        "id": 2,
        "name": "Carmela Soprano",
        "role": "Housewife",
        "status": "Active"
    },
    {
        "id": 3,
        "name": "Christopher Moltisanti",
        "role": "Capo",
        "status": "Deceased"
    },
    {
        "id": 4,
        "name": "Paulie 'Walnuts' Gualtieri",
        "role": "Soldier",
        "status": "Active"
    },
    {
        "id": 5,
        "name": "Dr. Jennifer Melfi",
        "role": "Psychiatrist",
        "status": "Retired"
    }
]

updated_users = [
    (1, {"name": "Walter", "job": "teacher"}),
    (2, {"name": "Jesse", "job": "cook"}),
    (3, {"name": "Saul", "job": "lawyer"}),
    (4, {"name": "Mike", "job": "bodyguard"}),
    (5, {"name": "Gus", "job": "manager"})
]