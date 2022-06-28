import os.path
from typing import Any

from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from requests_toolbelt import MultipartEncoder
import urllib
import json
import requests

from all_requests.request_utils import create_connection


def create_json(num_carte: str, nom: str, prenom: str, sexe: str, date_naiss: str, lieu_naiss: str, nation: str,
                adresse: str, num_cin: str, date_cin: str, lieu_cin: str, quintance: str, date_quintance: str,
                montant: str, photo: str, etat: str, moyenne: float, uuid_mention: str, uuid_parcours: str,
                bacc_anne: str, semestre_petit: str, semestre_grand: str) -> dict:
    etudiant = {
        "nom": nom,
        "prenom": prenom,
        "date_naiss": date_naiss,
        "lieu_naiss": lieu_naiss,
        "adresse": adresse,
        "sexe": sexe,
        "nation": nation,
        "num_cin": num_cin,
        "date_cin": date_cin,
        "lieu_cin": lieu_cin,
        "montant": montant,
        "etat": etat,
        "photo": photo,
        "num_quitance": quintance,
        "date_quitance": date_quintance,
        "num_carte": num_carte,
        "moyenne": moyenne,
        "bacc_anne": bacc_anne,
        "uuid_mention": uuid_mention,
        "uuid_parcours": uuid_parcours,
        "semestre_petit": semestre_petit,
        "semestre_grand": semestre_grand
    }
    return etudiant


def create_json_pre_select(num_select: str, nom: str, prenom: str, date_naiss: str, lieu_naiss: str, adresse: str,
                           num_cin: str, date_cin: str, lieu_cin: str, uuid_mention: str, niveau: str, branche: str,
                           nation: str, sexe: str, select: bool = False):
    """
    Function to create a json object for the selection
    :param num_select:
    :param nom:
    :param prenom:
    :param date_naiss:
    :param lieu_naiss:
    :param adresse:
    :param num_cin:
    :param date_cin:
    :param lieu_cin:
    :param uuid_mention:
    :param niveau:
    :param branche:
    :param nation:
    :param sexe:
    :param select:
    :return:
    """
    etudiant = {
        "num_select": num_select,
        "nom": nom,
        "prenom": prenom,
        "date_naiss": date_naiss,
        "lieu_naiss": lieu_naiss,
        "adresse": adresse,
        "num_cin": num_cin,
        "date_cin": date_cin,
        "lieu_cin": lieu_cin,
        "uuid_mention": uuid_mention,
        "niveau": niveau,
        "branche": branche,
        "select": select,
        "nation": nation,
        "sexe": sexe
    }
    return etudiant


def creare_json_select(nom: str, prenom: str, date_naiss: str, lieu_naiss: str, adresse: str, sexe: str, nation: str,
                       num_cin: str, date_cin: str, lieu_cin: str, montant: str, etat: str,
                       num_quitance: str, date_quitance: str, situation: str, telephone: str, bacc_num: str,
                       bacc_centre: str, bacc_anne: str, bacc_serie: str, proffession: str, nom_pere: str,
                       proffession_pere: str, nom_mere: str, proffession_mere: str, adresse_parent: str, branche: str,
                       uuid_mention: str, uuid_parcours: str, niveau: str, select: bool = True):
    etudiant = {
        "nom": nom,
        "prenom": prenom,
        "date_naiss": date_naiss,
        "lieu_naiss": lieu_naiss,
        "adresse": adresse,
        "sexe": sexe,
        "nation": nation,
        "num_cin": num_cin,
        "date_cin": date_cin,
        "lieu_cin": lieu_cin,
        "montant": montant,
        "etat": etat,
        "niveau": niveau,
        "num_quitance": num_quitance,
        "date_quitance": date_quitance,
        "situation": situation,
        "telephone": telephone,
        "bacc_num": bacc_num,
        "bacc_centre": bacc_centre,
        "bacc_anne": bacc_anne,
        "bacc_serie": bacc_serie,
        "proffession": proffession,
        "nom_pere": nom_pere,
        "proffession_pere": proffession_pere,
        "nom_mere": nom_mere,
        "proffession_mere": proffession_mere,
        "adresse_parent": adresse_parent,
        "branche": branche,
        "uuid_mention": uuid_mention,
        "uuid_parcours": uuid_parcours,
        "select": select
    }
    return etudiant


def success(req, result):
    print('success')
    MDApp.get_running_app().ERROR = ""


def fail(req, result):
    """
    when a request failed
    :param req:
    :param result:
    :return:
    """
    print(req, result)
    MDApp.get_running_app().ERROR = result


def error(req, result):
    """
    when a request got an error
    :param req:
    :param result:
    :return:
    """
    print(req, result)
    MDApp.get_running_app().ERROR = result


def progress(req, result, chunk):
    """
    call this during progressing request
    :param req:
    :param result:
    :param chunk:
    :return:
    """
    print('loading')


def get_all_ancien(url: str, annee: str, token: str):
    """
    To get all
    :param url:
    :param annee:
    :param token:
    :return:
    """
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}'}
    # converted data to json type 
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    return req.result


def get_by_mention(url: str, annee: str, uuid_mention: str, token: str):
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', "uuid_mention": f'{uuid_mention}'}
    # converted data to json type 
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='GET')
    req.wait()
    return req.result


def post_photo(url: str, num_carte: str, token: str, path: str):
    values = {"num_carte": f'{num_carte}'}
    # converted data to json type
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    req = requests.post(url=url, headers=headers, files={"uploaded_file": open(f'{path}', 'rb')})
    return req.json()


def delete(url: str, annee: str, key: str, value: str, token: str):
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', f"{key}": f'{value}'}
    # converted data to json type
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, verify=False, method='DELETE')
    req.wait()
    return req.result


def save_etudiant(url: str, annee: str, token: str, num_carte: str, nom: str, prenom: str, sexe: str,
                  date_naiss: str, lieu_naiss: str, nation: str,
                  adresse: str, num_cin: str, date_cin: str, lieu_cin: str, quintance: str, date_quintance: str,
                  montant: str, photo: str, etat: str, moyenne: float, uuid_mention: str, uuid_parcours: str,
                  bacc_anne: str, semestre_petit: str, semestre_grand: str):
    etudiant = create_json(num_carte, nom, prenom, sexe, date_naiss, lieu_naiss, nation, adresse, num_cin, date_cin,
                           lieu_cin, quintance, date_quintance, montant, photo, etat, moyenne, uuid_mention,
                           uuid_parcours,
                           bacc_anne, semestre_petit, semestre_grand)
    etudiant["uuid"] = "993e2bd1-8608-4885-aed9-3436d1736373"

    payload = json.dumps(etudiant)

    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}'}
    return create_connection(url, values, payload, token, "POST")


def save_etudiant_select(url: str, annee: str, token: str, num_select: str, nom: str, prenom: str, sexe: str,
                         date_naiss: str, lieu_naiss: str, branche: str, nation: str,
                         adresse: str, num_cin: str, date_cin: str, lieu_cin: str, uuid_mention: str, niveau: str):
    etudiant = create_json_pre_select(num_select, nom, prenom, date_naiss, lieu_naiss, adresse,
                                      num_cin, date_cin, lieu_cin, uuid_mention, niveau, branche, nation, sexe)
    etudiant["uuid"] = "993e2bd1-8608-4885-aed9-3436d1736373"

    payload = json.dumps(etudiant)

    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}'}
    return create_connection(url, values, payload, token, "POST")


def update_select_etudiant(url: str, annee: str, token: str, num_select: str, nom: str, prenom: str, sexe: str,
                           date_naiss: str, lieu_naiss: str, branche: str, nation: str, adresse: str, num_cin: str,
                           date_cin: str, lieu_cin: str, uuid_mention: str, niveau: str, select: bool):
    etudiant = create_json_pre_select(num_select, nom, prenom, date_naiss, lieu_naiss, adresse,
                                      num_cin, date_cin, lieu_cin, uuid_mention, niveau, branche, nation, sexe, select)

    payload = json.dumps(etudiant)

    print(payload)
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', 'num_select': num_select}
    return create_connection(url, values, payload, token, "PUT")


def update_selected_etudiant(url: str, annee: str, token: str, num_select: str, nom: str, prenom: str, date_naiss: str,
                             lieu_naiss: str, adresse: str, sexe: str, nation: str, num_cin: str, date_cin: str,
                             lieu_cin: str, montant: str, etat: str, num_quitance: str, date_quitance: str,
                             situation: str, telephone: str, bacc_num: str, bacc_centre: str, bacc_anne: str,
                             bacc_serie: str, proffession: str, nom_pere: str, proffession_pere: str, nom_mere: str,
                             proffession_mere: str, adresse_parent: str, branche: str, uuid_mention: str,
                             uuid_parcours: str, niveau: str, select: bool):
    etudiant = creare_json_select(nom, prenom, date_naiss, lieu_naiss, adresse, sexe, nation, num_cin, date_cin,
                                  lieu_cin, montant, etat, num_quitance, date_quitance, situation, telephone,
                                  bacc_num, bacc_centre, bacc_anne, bacc_serie, proffession, nom_pere,
                                  proffession_pere, nom_mere, proffession_mere, adresse_parent, branche, uuid_mention,
                                  uuid_parcours, niveau, select)

    payload = json.dumps(etudiant)

    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', 'num_select': num_select}
    return create_connection(url, values, payload, token, "PUT")


def update_etudiant(url: str, annee: str, token: str, num_carte: str, nom: str, prenom: str, sexe: str,
                    date_naiss: str, lieu_naiss: str, nation: str,
                    adresse: str, num_cin: str, date_cin: str, lieu_cin: str, quintance: str, date_quintance: str,
                    montant: str, photo: str, etat: str, moyenne: float, uuid_mention: str, uuid_parcours: str,
                    bacc_anne: str, semestre_petit: str, semestre_grand: str):
    payload = json.dumps(
        create_json(num_carte, nom, prenom, sexe, date_naiss, lieu_naiss, nation, adresse, num_cin, date_cin,
                    lieu_cin, quintance, date_quintance, montant, photo, etat, moyenne, uuid_mention, uuid_parcours,
                    bacc_anne, semestre_petit, semestre_grand))

    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', 'num_carte': f'{num_carte}'}
    return create_connection(url, values, payload, token, "PUT")

