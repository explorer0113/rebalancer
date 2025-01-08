import json
import os

DATA_FOLDER = "data"

def save_data(filename, data):
    """JSON 파일로 데이터를 저장"""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_data(filename):
    """JSON 파일로부터 데이터를 로드"""
    filepath = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filename} 파일이 존재하지 않습니다.")
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def list_files():
    """data 폴더에 있는 JSON 파일 목록 반환"""
    if not os.path.exists(DATA_FOLDER):
        return []
    return [f for f in os.listdir(DATA_FOLDER) if f.endswith(".json")]
