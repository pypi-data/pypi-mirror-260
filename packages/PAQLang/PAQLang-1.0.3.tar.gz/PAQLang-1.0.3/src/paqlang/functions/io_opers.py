import asyncio
import re
import datetime
import os
from ..utils import aio_reads, get_json
from .util_opers import get_attr

from ..param import Param, get_param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class IoOpers:

    async def single_walk(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список файлов в директории
        
        path:str или param:str - корневой маршрут поиска файлов
        regex:str - шаблон отбора файлов, если не задан, то все файлы
        """
        regex = param.get_string("regex")
        while len(in_queue):
            # Получить файл
            path = in_queue.pop(0)
            if isinstance(path, str):
                for root, dirs, files in os.walk(path):
                    for file_name in [os.path.join(root, name) for name in files]:
                        if regex and not re.match(regex, file_name):
                                continue
                        out_queue.append(file_name)
        return ['success']

    async def multiple_freads(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Прочитать файл и положить содержимое в выходную очередь {fname, text}

        encoding:str, если не задано, то param:str - по умолчанию utf-8
        кодировка для windows файлов cp1251
        """
        encoding = param.get_string("encoding") or param.get_string()
        while len(in_queue):
            # Получить файл
            file_name = in_queue.pop(0)
            if isinstance(file_name, str):
                out_queue.append({
                    "path": file_name, 
                    "text": await aio_reads(file_name = file_name, encoding = encoding)})
        return ['success']

    async def single_to_json(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Распарсить JSON или YAML строковый элемент и положить в очередь

        Входная строка преобразуется в JSON, несколько массивов склеиваются
        attr:str = None или param:str = None - задает имя атрибута текста JSON или YAML
        """
        # Если задан параметр атрибут
        attr = param.get_string("attr") or param.get_string()
        while len(in_queue):
            # Получить элемент из очереди, с начала списка
            text = in_queue.pop(0)
            js_text = get_attr(attr = attr, elem = text, is_raise = False) if attr else text
            if js_text:
                js = get_json(text = js_text)
                if isinstance(js, list):
                    for elem in js:
                        if elem:
                            out_queue.append(elem)
                else:
                    out_queue.append(js)
        return ['success']
