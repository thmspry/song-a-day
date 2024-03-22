import json
import os
from dotenv import load_dotenv, find_dotenv

import utils

def load_env() -> dict:
    env_expected_variables = __load_env_expected_variables__()
    def list_variables(variables_to_list: list[str], variable_descriptions: dict) -> str:
        r_str = ""
        for v_name in variables_to_list:
            r_str += f"\t- {v_name} : {variable_descriptions[v_name]}"
        return r_str
            
    if not utils.__file_exists__(".env"):
        msg_err = "Le fichier .env n'existe pas. Veuillez le créer en renseignant les variables suivantes :"
        raise Exception(msg_err + list_variables(env_expected_variables.keys(), env_expected_variables))

    load_dotenv(find_dotenv())
    missing_variables = []
    env = {}
    for v_name in env_expected_variables:
        VALUE = os.environ.get(v_name)
        if VALUE is None:
            missing_variables.append(v_name)
        else:
            env[v_name] = VALUE
      
    if len(missing_variables) > 0:
        one_or_two = "des variables" if len(missing_variables) > 1 else "une variable"
        msg_err = f"Il manque {one_or_two} dans le fichier .env :"
        raise Exception(msg_err + list_variables(missing_variables, env_expected_variables))
        
    return env

def __load_env_expected_variables__(file_path: str = "env_description.json") -> dict:
    with open(file_path, 'r') as file_json:
        # Charger le JSON
        json_data = file_json.read()
        data = json.loads(json_data)
        # Transformer en un dictionnaire
        return {item["key"]: item["description"] for item in data}