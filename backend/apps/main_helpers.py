import hashlib


def model_to_dict(model):
    new_dict = {}
    model_dict = model.__dict__
    for key in model_dict:
        if not key.startswith('_'):
            new_dict[key] = model_dict[key]
    return new_dict


def models_to_dict(models: list):
    new_list = []
    for model in models:
        new_list.append(model_to_dict(model))
    return new_list


def get_hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = hashlib.sha512(password.encode("utf-8")).hexdigest()
    return hash_pass
