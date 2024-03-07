import asyncio
import re
import datetime

from .util_opers import coalesce, get_condition
from ..param import Param, get_param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)


class ControlOpers:

    async def single_exit(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Завершить выполнение программы
        """
        return ['exit']


    async def single_when(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Если условие истино, ты выполнить stage

        Входное значение, если указано "in", иначе входная очередь
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        Если условие не задано, то выполняется, если входная очередб не пустая
        """
        # Скопировать очередь
        out_queue.extend(in_queue)
        if len(param.list) == 0:
            result = len(in_queue) != 0
        else:    
            test_value = coalesce([param.get_float("in"), param.get_string("in"), p_queue.get_float(), p_queue.get_string()])
            result = get_condition(test_value, param)
        if result:
            return ['success']
        else:
            # Откатить стайдж
            return ['when']

    async def single_break(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Если условие истино, ты прервать цикл while (break)

        Входное значение, если указано "in", иначе входная очередь
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        """
        # Скопировать очередь
        out_queue.extend(in_queue)
        if len(param.list) == 0:
            result = len(in_queue) == 0
        else:    
            test_value = coalesce([param.get_float("in"), param.get_string("in"), p_queue.get_float(), p_queue.get_string()])
            result = get_condition(test_value, param)
        if result:
            return ['break']
        else:
            return ['success']

    async def single_continue(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Если условие истино, ты прервать цикл while (continue)

        Входное значение, если указано "in", иначе входная очередь
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        """
        # Скопировать очередь
        out_queue.extend(in_queue)
        test_value = coalesce([param.get_float("in"), param.get_string("in"), p_queue.get_float(), p_queue.get_string()])
        if get_condition(test_value, param):
            return ['continue']
        else:
            return ['success']
