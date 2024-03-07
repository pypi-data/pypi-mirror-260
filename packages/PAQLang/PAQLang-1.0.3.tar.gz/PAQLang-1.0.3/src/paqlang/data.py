from .utils import getenv, save_object

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class Data:

    data = {}

    def set_data(self, name: str, value: list):
        if name == '':
            raise Exception(f'Попытка записать в переменную памяти с именем ""')
        self.data[name.lower()] = []
        self.data[name.lower()].extend(value)
        # Залогируем выполненныю задачу
        if getenv("SAVE_OBJECTS", "0") == "1":        
            save_object(value_dict = value, filename = name)

    def get_data(self, name: str) -> list:
        if name.lower() in self.data:
            return self.data[name.lower()]
        else:
            raise Exception(f'Не определена переменная {name}')
        
    def get_data_keys(self) -> list:
        return [key for key in self.data]    

mems = Data()