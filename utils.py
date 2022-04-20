import datetime
import json
import uuid


def create_list(text: str) -> list:
    """
    Create a list from a String
    :param text:
    :return:
    """
    return text.split(", ")


def delete_string(text: str, str_delet: str) -> str:
    list_text = create_list(text)
    list_text.remove(str_delet)
    return creat_str_from_list(list_text)


def creat_str_from_list(list_text: list) -> str:
    """
    Create a String from a list
    :param list_text:
    :return:
    """
    response = ""
    for index, string_ in enumerate(list_text):
        if index != len(list_text) - 1:
            response += f'{string_}, '
        else:
            response += f'{string_}'
    return response


def ajout_list(string: str, str_ajout: str) -> str:
    if string != "":
        list_text = create_list(string)
    else:
        list_text = []
    list_text.append(str_ajout)
    return creat_str_from_list(list_text)


def select_str(string: str, text: str) -> str:
    list_str = create_list(string)
    test: bool = False
    for str_ in list_str:
        if str_ == text:
            test = True
    if test:
        return delete_string(string, text)
    else:
        return ajout_list(string, text)


def load_data(name: str):
    """
    load the json file
    :param name:
    :return:
    """
    with open(f'data/{name}.json') as f:
        return json.load(f)


def save_data(name: str, json_data):
    """
        Save the json file with new data
        :param name:
        :param json_data:
        :return:
    """
    with open(f'data/{name}.json', "w") as f:
        json.dump(json_data, f, indent=4)


def get_data_from_json(name: str, key: str):
    """
        Save the json file with new data
        :param name:
        :param key:
        :return:
    """
    json_data = load_data(name)
    return list(json_data[key])


def create_one_item_in_json(name: str, data, key: str):
    json_data = load_data(name)
    id = uuid.uuid4()
    data['uuid'] = str(id)
    json_data[key].append(data)
    save_data(name, json_data)


def delete_item_from_json(uuid: str, key: str, name: str):
    json_data = load_data(name)
    data_old = json_data[key]
    for item in data_old:
        if item['uuid'] == uuid:
            data_old.remove(item)
    json_data[key] = data_old
    save_data(name, json_data)


def get_item_by_title_from_json(title: str, key: str, name: str):
    json_data = load_data(name)
    data_old = json_data[key]
    for item in data_old:
        if item['title'] == title:
            return item


if __name__ == "__main__":
    data = {
        "title": "Serveur ubuntu",
        "address": "192.168.88.30"
    }
    # create_one_item_in_json("server", data, 'server')
    # print(get_data_from_json('server', 'server'))
    delete_item_from_json("9dc4d059-6f4d-4328-bef1-565f6239ebdd", "server", "server")
