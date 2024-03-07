import asyncio
import re
import datetime

from ..param import Param, get_param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class BoolOpers:

    async def single_bool_true(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Положить в очередь истина, любой не пустой массив
        """
        out_queue.extend([1])
        return ['success']
    
    async def single_bool_false(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Положить в очередь ложь. Пустой массив
        """
        out_queue.extend([])
        return ['success']

    async def single_not(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Инвертировать логическую операцию
        """
        if len(in_queue) == 0:
            out_queue.append(1)
        return ['success']
