import aiofiles
import yaml
import json
import os
import errno
import dataclasses
import datetime
import decimal
from datetime import date, datetime, timedelta
from typing import Any
# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

def get_attr(attr, elem, is_raise:bool = True):
    if attr:
        if attr and isinstance(elem, dict) and (attr in elem):
            return elem[attr]
        else:
            if is_raise:
                raise Exception(f'Не найден атрибут "{attr}" в элементе "{elem}"')    
            else:
                return None
    return elem    

def coalesce(plist: list):
    for elem in plist:
        if elem is not None:
            return elem
    return None    

def get_condition(test_value, param):
    """Проверить условие

    test_value:float:int:str - проверяемое значение
    param:dict - словарь заданных условий
    return bool - результат проверки
    """
    if isinstance(test_value, (float, int)):   
        where = True
        conditions_float = {
            "lt": lambda x, y: x <  y,
            "le": lambda x, y: x <= y,
            "eq": lambda x, y: x == y if y is not None else x is None,
            "ne": lambda x, y: x != y if y is not None else x is not None,
            "gt": lambda x, y: x >  y,
            "ge": lambda x, y: x >= y,
        }
        for key, function in conditions_float.items():
            if key in param.dict:
                where = where and function(test_value, param.get_float(key))
                logger.debug(f'{key=} {test_value=} {param.get_float(key)=} {where=}')
        return where
    elif isinstance(test_value, str):   
        where = True
        conditions_str = {
            "lt": lambda x, y: x <  y,
            "le": lambda x, y: x <= y,
            "eq": lambda x, y: x == y if y is not None else x is None,
            "ne": lambda x, y: x != y if y is not None else x is not None,
            "gt": lambda x, y: x >  y,
            "ge": lambda x, y: x >= y,
            # Входит строка
            "instr": lambda x, y: x in y,
            # Не входит строка
            "notinstr": lambda x, y: x not in y,
        }
        for key, function in conditions_str.items():
            if key in param.dict:
                where = where and function(test_value, param.get_string(key))
                logger.debug(f'{key=} {test_value=} {param.get_string(key)=} {where=}')
        return where
    return False
