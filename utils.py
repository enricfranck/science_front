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
