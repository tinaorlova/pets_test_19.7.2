from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_email(email='', password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_get_api_key_for_invalid_password(email=valid_email, password=''):
    status, _ = pf.get_api_key(email, password)

    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert 'pets' in result


def test_get_pets_with_invalid_filter(filter='invalid_filter'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 400


def test_get_all_pets_with_invalid_key(filter=''):
    status, result = pf.get_list_of_pets({'key': ''}, filter)

    assert status == 403


def test_add_new_pet_with_valid_data(
    name='Полкан',
    animal_type='лютоволк',
    age='4',
    pet_photo='images/dog.jpg',
):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_key(
    name='Полкан',
    animal_type='лютоволк',
    age='4',
    pet_photo='images/dog.jpg',
):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet({'key': ''}, name, animal_type, age, pet_photo)

    assert status == 403


def test_add_new_pet_simple_with_valid_data(
    name='Полкан Иванович',
    animal_type='волк',
    age=5,
):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_new_pet_simple_with_invalid_key(
    name='Полкан Иванович',
    animal_type='волк',
    age=5,
):
    status, result = pf.add_new_pet_simple({'key': ''}, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_successful_add_pet_photo(
    pet_photo='images/dog.jpg',
):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Полкан", "волк", 4)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200


def test_failed_add_pet_photo(
    pet_photo='images/dog.jpg',
):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, _ = pf.add_pet_photo(auth_key, '', pet_photo)

    assert status == 404


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_failed_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.delete_pet(auth_key, '')

    assert status == 404


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_failed_update_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.update_pet_info(auth_key, '', name, animal_type, age)

    assert status == 404
