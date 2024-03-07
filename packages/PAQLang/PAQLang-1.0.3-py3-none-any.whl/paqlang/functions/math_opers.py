import asyncio
import datetime

from .util_opers import get_attr, get_condition
from ..param import Param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class MathOpers:

    async def single_filter(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Отобрать элементы из числовой очереди, удовлетворяющие условию. Не числовые элементы, отбрасываться из очереди

        attr:str - если указано, то анализировать атрибут из элемента очереди
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        Условия объединяются по "AND"
        """
        # Если задан параметр атрибут
        attr = param.get_string("attr")
        # Перебрать элементы очереди
        for elem in in_queue:
            # Получить проверяемое значение
            test_value = get_attr(attr = attr, elem = elem, is_raise = False) if attr else elem
            # Проверить условие
            result = get_condition(test_value, param)
            if result:
                out_queue.append(elem)
        return ['success']

    def __math_opers(param, in_queue, out_queue, msg, func):
        value = param.get_float()
        assert value is not None, msg
        for elem in in_queue:
            if isinstance(elem, (float, int)):   
                out_queue.append(func(elem, value))
        return ['success']

    async def single_add(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Добавить значение ко всем элементам очереди. Не числовые элементы, отбрасываться из очереди

        param:float - добавляемое значение
        """
        return MathOpers.__math_opers(param, in_queue, out_queue, "Не задано слогаемое", lambda x, y: x + y)

    async def single_sub(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вычесть значение из всех элементов очереди. Не числовые элементы, отбрасываться из очереди

        param:float - вычитаемое значение
        """
        return MathOpers.__math_opers(param, in_queue, out_queue, "Не задано вычитаемое значение", lambda x, y: x - y)

    async def single_mul(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Умножить на значение все элементы очереди. Не числовые элементы, отбрасываться из очереди

        param:float - множитель
        """
        return MathOpers.__math_opers(param, in_queue, out_queue, "Не задан множитель", lambda x, y: x * y)

    async def single_div(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Разделить на значение все элементы очереди. Не числовые элементы, отбрасываться из очереди

        param:float - делитель
        """
        assert param.get_float() != 0, "Делитель равен нулю"
        return MathOpers.__math_opers(param, in_queue, out_queue, "Не задан делитель", lambda x, y: x / y)

    def __inc_dec(param, p_queue, out_queue, sign):
        # Получить шаг приращения, атрибут, параметр в функции или 1
        step = param.get_float("step") or 1
        # Получить имя переменной
        mem_name = param.get_string("mem") or param.get_string()
        if mem_name:
            # Если переменная существует, то взять из нее значение, иначе 0
            result = Param(mems.get_data(mem_name)).float if mem_name in mems.data else 0
        else:
            # Взять значение из очереди
            result = p_queue.float    
        # Операция приращения    
        result += sign * step  
        # Записать значение в переменную
        if mem_name:
            mems.set_data(mem_name, [result])    
        out_queue.extend([result])
        return ['success']

    async def single_inc(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Добавить к очереди, числовое значение

        step:float или param:float или 1 - добавляемое значение
        mem:str - если указана переменная, то добавить значение к переменной, результат также положить в очередь
        """
        return MathOpers.__inc_dec(param = param, p_queue = p_queue, out_queue = out_queue, sign = 1)

    async def single_dec(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Уменьшить значение в очереди

        step:float или param:float или 1 - уменьшаемое значение
        mem:str - если указана переменная, то уменьшить значение переменной, результат также положить в очередь
        """
        return MathOpers.__inc_dec(param = param, p_queue = p_queue, out_queue = out_queue, sign = -1)
