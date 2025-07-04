def check_user(id_, users):
    if any(id_ == user.id for user in users):
        return True
    return False