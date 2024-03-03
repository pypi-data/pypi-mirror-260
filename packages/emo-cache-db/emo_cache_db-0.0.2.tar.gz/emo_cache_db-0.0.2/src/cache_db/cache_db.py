import json
from file_system.file import File


class CacheDB:

    def __init__(self, file_path):
        self.file_path = file_path
        self.cache = {}
        File.create_file_directory(file_path)

    def load_cache(self, mode="r", encoding="utf-8"):
        if File.exists(self.file_path):
            with open(self.file_path, mode, encoding=encoding) as file:
                self.cache = json.load(file)

    def save_cache(self, mode="w", encoding="utf-8"):
        with open(self.file_path, mode, encoding=encoding) as file:
            json.dump(self.cache, file, ensure_ascii=False)

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def all(self) -> dict:
        if not self.cache:
            self.load_cache()

        return self.cache
