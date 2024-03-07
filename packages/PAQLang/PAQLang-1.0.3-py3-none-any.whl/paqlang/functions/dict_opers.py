import asyncio
import datetime

from .util_opers import get_attr
from ..data import mems
from ..param import Param

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class DictOpers:

    def attr(l, elems, keys):
        if len(keys) == 0:
            return {}
        elif isinstance(elems, dict):
            result = {}
            for key in elems:
                if key in keys:
                    result[key] = elems[key]
            for key in elems:
                if isinstance(elems[key], list):
                    for elem in elems[key]:
                        x = DictOpers.attr(elem, keys)
                        if x:
                            result = {**result, **DictOpers.attr(elem, keys)}
            return result        

    def _plane(elem):
        if isinstance(elem, dict):
            result = {}
            ext = []
            for key in elem:
                el = elem[key]
                if isinstance(el, list):
                    for el1 in el:
                        ext.append(DictOpers._plane(el1))
                else:    
                    result[key] = el
            if len(ext) > 0:
                l = []
                for e in ext:
                    l.append({**result, **e})
                return l
            else:            
                return result

    async def single_plane(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Сделать плоскую таблицу. Каждый элемент рекурсивно раскрыть до элементов

        """
        for elem in in_queue:
            out_queue.extend(DictOpers._plane(elem))
        return ['success']

    async def single_attr(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить атрибут элемента

        param:str = None - если задан один атрибут, то вернуть его значение
        param:list = None - если задано несколько атрибутов, то вернуть словарь из этих атрибутов
        param:dict = None - вернуть набор заданных атрибутов, с возможностью замены на новый атрибут
        """
        # Задано два и более элемента
        if len(param.list) >= 2:
            # Перебрать очередь 
            for elem in in_queue:
                # Получить словарное представление очереди
                src_elem = Param(elem).dict
                result = {}
                # Перебрать все требуемы атрибуты
                for key in param.list:
                    # Атрибут найден, добавить его в словарь
                    if key in src_elem:
                        result[key] = src_elem[key]
                # Положить в результирующую очередь        
                if result:        
                    out_queue.append(result)
        #  Задан словарь            
        elif param.dict:
            # Перебрать элементы очереди
            for elem in in_queue:
                result = {}
                # Перебрать все требуемы атрибуты
                for key, result_key in param.dict.items():
                    # Если атрибут есть в очереди
                    if key in elem:
                        # Если задан атибут подмены
                        if result_key:
                            # Подменить ключ элемента
                            result[result_key] = elem[key]
                        else:    
                            # Добавить значение с атрибутом
                            result[key] = elem[key]
                # Положить в результирующую очередь        
                if result:        
                    out_queue.append(result)
        else:   
            # Получить наименование атрибута
            attr = param.get_string()
            if attr:
                # Перебрать очередь
                for elem in in_queue:
                    # Если атрибут входит в очередь, то вернуть в поток его значение
                    if isinstance(elem, dict) and attr in elem:
                        out_queue.append(elem[attr])

        return ['success']
