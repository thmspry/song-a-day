import os

def remove_file(file_path: str):
    if file_exists(file_path):
        os.remove(file_path)
        
def file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)