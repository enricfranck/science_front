from kivy.network.urlrequest import UrlRequest
import urllib
import json


def create_json(num_carte: str, nom: str, prenom: str, sexe: str, date_naiss: str, lieu_naiss: str, nation: str,
                adresse: str, num_cin: str, date_cin: str, lieu_cin: str, quintance: str, date_quintance: str,
                montant: str, etat: str, moyenne: float, uuid_mention: str, uuid_parcours: str, bacc_anne: str,
                semestre_petit: str, semestre_grand: str) -> dict:
    etudiant = {
        "uuid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
        "photo": f"{num_carte}.jpg",
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


def success(req, result):
    print('success')


def fail(req, result):
    print('fail')


def error(req, result):
    print('error')


def progress(req, result, chunk):
    print('loading')


def get_all_ancien(url: str, annee: str, token: str):
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


def get_ancien_by_mention(url: str, annee: str, uuid_mention: str, token: str):
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


def delete_ancien_etudiant(url: str, annee: str, num_carte: str, token: str):
    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}', "num_carte": f'{num_carte}'}
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


def save_etudiant(url: str, annee: str, token: str, methode: str, num_carte: str, nom: str, prenom: str, sexe: str,
                  date_naiss: str, lieu_naiss: str, nation: str,
                  adresse: str, num_cin: str, date_cin: str, lieu_cin: str, quintance: str, date_quintance: str,
                  montant: str, etat: str, moyenne: float, uuid_mention: str, uuid_parcours: str, bacc_anne: str,
                  semestre_petit: str, semestre_grand: str):
    payload = json.dumps(
        create_json(num_carte, nom, prenom, sexe, date_naiss, lieu_naiss, nation, adresse, num_cin, date_cin,
                    lieu_cin, quintance, date_quintance, montant, etat, moyenne, uuid_mention, uuid_parcours,
                    bacc_anne, semestre_petit, semestre_grand))

    schemas = "anne_" + annee[0:4] + "_" + annee[5:9]
    values = {'schema': f'{schemas}'}
    params = urllib.parse.urlencode(values)
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}'
               }
    url = f"{url}?{params}"
    print(url, payload)
    req = UrlRequest(url, on_success=success, on_failure=fail, on_error=error, on_progress=progress,
                     req_headers=headers, req_body=payload, verify=False, method=methode)
    req.wait()
    return req.result
