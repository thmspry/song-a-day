from dotenv import dotenv_values

import manager.file_manager as fm

DOTENV_PATH = ".env"
expected_variable_names = ["SPREADSHEET_ID", "API_KEY", "SESSION_ID_TIKTOK"]

def load_env() -> list[dict]:    
    if not fm.file_exists(DOTENV_PATH):
        raise Exception("Le fichier .env n'existe pas.")
    
    config = dotenv_values(DOTENV_PATH)
    
    env: list[dict] = []
    
    for v_name in expected_variable_names:
        value = None
        if v_name in config:
            value = config[v_name]
        env_variable = {"name": v_name, "value": value}
        env.append(env_variable)
        
    return env