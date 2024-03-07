import asyncio
import re
import datetime

from ..utils import save_object
from ..param import Param, get_param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class QueueOpers:

    async def single_print(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Распечатать текущую очередь данных, в loggin.info

        in_queue - входная очередь
        ps: очередь не изменяется
        """
        name = param.get_string()
        for elem in in_queue:
            if name:
                logger.info(f'print({name}): {elem}')
            else:    
                logger.info(f'print: {elem}')
        out_queue.extend(in_queue)
        return ['success']

    async def single_in(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Положить данные в очередь как список
        
        Результат в выходную очередь out_queue
        """
        out_queue.extend(param.list)
        # logger.info(f'in: {len(param.list)}')
        return ['success']

    async def single_out(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Содержимое очереди записать в переменную памяти

        in_queue - входная очередь
        param:str - наименование переменной памяти
        ps: очередь не изменяется
        """
        out_queue.extend(in_queue)
        mem_name = param.get_string()
        assert mem_name is not None, "Не указано наименование переменной памяти"
        logger.info(f'out: {mem_name}')
        mems.set_data(mem_name, in_queue)
        return ['success']
    
    async def single_sort(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Отсортировать список
        
        in_queue - входная очередь
        param:str - направление сортировки "desc", "asc" - по умолчанию
        """
        if param.get_string() and param.get_string() == "desc":
            out_queue.extend(sorted(in_queue, reverse = True))
        else:    
            out_queue.extend(sorted(in_queue))
        return ['success']

    async def single_distinct(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить уникальные элементы очереди и отсортировать по возрастанию
        
        in_queue - входная очередь
        """
        out_queue.extend(sorted(list(set(in_queue))))
        return ['success']

    async def single_len(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вернуть размер входной очереди
        
        in_queue - входная очередь
        """
        out_queue.append(len(in_queue))
        return ['success']

    async def single_push(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Добавить элементы в конец текущей очереди

        in_queue - входная очередь
        param - добавляемое значение в очередь
        """
        out_queue.extend(in_queue)
        out_queue.extend(param.list)
        return ['success']

    async def single_first(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вернуть первый элемент очереди
        
        in_queue - входная очередь
        param:str - если задано значение, то взять очередь из переменной
        """
        mem_name = param.get_string()
        if mem_name:
            __in_queue = mems.get_data(mem_name)
        else:    
            __in_queue = in_queue
        if len(__in_queue) > 0:
            out_queue.append(__in_queue.pop(0))
        return ['success']

    async def single_last(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вернуть последний элемент очереди

        in_queue - входная очередь
        param:str - если задано значение, то взять очередь из переменной
        """
        mem_name = param.get_string()
        if mem_name:
            __in_queue = mems.get_data(mem_name)
        else:    
            __in_queue = in_queue
        if len(__in_queue) > 0:
            out_queue.append(__in_queue.pop())
        return ['success']

    async def single_pop(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вытолкнуть последний элемент из очереди

        in_queue - входная очередь
        param:str - если задано значение, то взять очередь из переменной
        """
        mem_name = param.get_string()
        if mem_name:
            __in_queue = mems.get_data(mem_name)
        else:    
            __in_queue = in_queue
        if len(__in_queue) > 0:
            out_queue.append(__in_queue.pop())
        if mem_name:
            mems.set_data(mem_name, __in_queue)
        return ['success']

    async def single_save(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Сохранить очередь на диске

        in_queue - входная очередь
        param:str - наименование файла данных
        """
        out_queue.extend(in_queue)
        save_name = param.get_string()
        assert save_name is not None, "Не указано имя файла результата"
        save_object(value_dict = in_queue, filename = save_name)
        return ['success']

    async def single_minus(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вычесть очередь из очереди

        in_queue - входная очередь
        param:list - вычитаемая очередь
        """
        # Скопировать очередь
        __in_queue = in_queue.copy()
        # Пробежать вычитаемую очередь
        for x in param.list:
            # Если есть элемент во входной очереди
            while x in __in_queue:
                # Убрать элемент из исходной очереди
                __in_queue.remove(x)
        # Положить элемент во входную очередь        
        out_queue.extend(__in_queue)
        return ['success']

    async def single_intersect(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вернуть только пересекаемые элементы очереди

        in_queue - первая очередь
        param:list - вторая очередь
        """
        out_queue.extend(list(set(in_queue) & set(param.list)))
        return ['success']

    async def single_union_all(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Объединить очереди

        in_queue - входная очередь
        param - добавляемое значение в очередь
        """
        out_queue.extend(in_queue)
        out_queue.extend(param.list)
        return ['success']

    async def single_union(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Объединить очереди, убрать дубликаты

        in_queue - входная очередь
        param - добавляемое значение в очередь
        """
        # Скопировать очередь
        __in_queue = in_queue.copy()
        # Добавить элементы в очередь
        __in_queue.extend(param.list)
        # Добавить элементы в очередь, убрав дубликаты
        out_queue.extend(list(set(__in_queue)))
        return ['success']

    async def single_expand(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Расширить подмассивы

        in_queue - входная очередь
        param - добавляемое значение в очередь
        """
        # Скопировать очередь
        for item in in_queue:
            if isinstance(item, list):
                out_queue.extend(item)
            else:    
                out_queue.append(item)
        return ['success']
