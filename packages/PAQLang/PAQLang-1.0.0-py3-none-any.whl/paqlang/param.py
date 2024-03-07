import re
# Стандартное логирование
import logging

from .data import mems

# Установить текущи логгер
logger = logging.getLogger(__name__)

def list2dict(params_as_list: list) -> dict:
    __dict = {}
    for elem in params_as_list:
        if isinstance(elem, dict):
            for key, value in elem.items():
                __dict[key] = value
    return __dict        

class Param:

    def prepare(self, value: dict, key: str = None) -> dict:
        """Скрыть пароли и токены в словаре

        :param dict value: исходный словарь
        :param str key: Ключ
        :return dict: преобразованный словарь
        """
        if value is None:
            return None
        elif isinstance(value, dict):
            return {k: self.prepare(v, k) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.prepare(elem) for elem in value]
        else:
            if isinstance(value, str):
                m = re.match('^~(.+)$', value.strip())
                if m:
                    # logger.info(f'GET DATA {m.group(1)=}')
                    return mems.get_data(m.group(1))
            return (value)        

    def __init__(self, param:dict = None):
        """Инициализировать класс параметра

        :param object pgm: Ссылка на объект программы Pgm
        :param int stage_id: идентификатор stage
        :param str name: наименование параметра
        :param list tps: список доступных типов
        """
        if param is not None:
            # Рекурсивно разобрать косвенную адресацию
            self.param = self.prepare(value = param)

    def as_list(self):
        if self.param is None:
            return []
        else:    
            if isinstance(self.param, list):
                result = []
                for elem in self.param:
                    if isinstance(elem, list):
                        result.extend(elem)
                    else:
                        result.append(elem)
                return result        
            else:
                return [self.param]    

    def as_list2(self):
        return self.as_list()

    def as_string(self):
        return "\n".join([f'{s}' for s in self.as_list2()])

    def as_dict(self):
        return list2dict(self.as_list())

    def as_int(self):
        if len(self.as_list2()) == 1:
            try:
                return int(self.as_list2()[0])
            except:
                return 0
        else:
            return 0

    def as_float(self):
        if len(self.as_list2()) == 1:
            try:
                return float(self.as_list2()[0])
            except:
                return 0
        else:
            return 0

    def __getattr__(self, attr):
        if attr == "list":
            return self.as_list()
        elif attr == "list2":
            return self.as_list2()
        elif attr == "dict":
            return self.as_dict()
        elif attr == "string":
            return self.as_string()
        elif attr == "int":
            return self.as_int()
        elif attr == "float":
            return self.as_float()

    def get_string(self, name:str = None) -> str:
        if name:
            if (name in self.dict):
                return Param(self.dict[name]).get_string()
        else:
            # if isinstance(self.param, str):
            #     return self.string
            # elif isinstance(self.param, list):
            #     if len(self.param) > 0:
            #         if isinstance(self.param[0], (str)):
            #             return Param(self.param[0]).string
            if self.param is None:
                return None
            elif isinstance(self.param, list):
                if len(self.param) > 0:
                    if isinstance(self.param[0], (str)):
                        return Param(self.param[0]).string
            elif isinstance(self.param, dict):
                return None
            else:        
                return self.string
        return None

    def get_list(self, name:str = None) -> str:
        if name:
            if (name in self.dict):
                return Param(self.dict[name]).get_list()
        else:
            if self.param is None:
                return None
            elif isinstance(self.param, list):
                return self.param
        return None

    def get_float(self, name:str = None) -> float:
        if name:
            if name in self.dict:
                return Param(self.dict[name]).get_float()
        else:
            if self.param is None:
                return None
            elif isinstance(self.param, dict):
                return None
            elif isinstance(self.param, int) or isinstance(self.param, float):
                return self.float
            elif isinstance(self.param, list):
                if len(self.param) > 0:
                    if isinstance(self.param[0], (int, float)):
                        return Param(self.param[0]).float
        return None

def get_param(value:dict, name:str) -> Param:
    if name in value:
        return Param(value[name])
    else:
        return Param([])

