from .utils import save_object
import asyncio
import re
import datetime

from .param import Param
from .data import Data, mems
from .functions.other_opers import OtherOpers
from .functions.math_opers import MathOpers
from .functions.string_opers import StringOpers
from .functions.date_opers import DateOpers
from .functions.queue_opers import QueueOpers
from .functions.bool_opers import BoolOpers
from .functions.control_opers import ControlOpers
from .functions.io_opers import IoOpers
from .functions.dict_opers import DictOpers

import inspect

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

def log(mess:str):
    # stage_desc = f'{datetime.datetime.now()}:{mess}'
    stage_desc = f'{mess}'
    logger.debug(f'{stage_desc}')


class Pgm:
    """Класс выполнения программы
    """
    # Внешние процедуры параллельной обработки
    multiple_opers = None
    # Список внутренних процедур обработки
    single_opers = None
    # Список подпрограмм
    macros = None
    #
    result = None

    def __init__(self):
        """Создать объект выполняемая программа

        :param str text: текст программы на языке YAML, defaults to None
        """
        # Получить список внутренних процедур программы
        self.multiple_opers = {}
        # Список внутренних процедур обработки
        self.single_opers = {}
        # Список подпрограмм
        self.macros = {}
        for cls in [
            OtherOpers, 
            MathOpers, 
            StringOpers, 
            DateOpers, 
            QueueOpers, 
            ControlOpers, 
            IoOpers,
            BoolOpers,
            DictOpers]:
            self.append_opers(in_class = cls)

    def append_macros(self, macros:dict):
        if macros:
            for key, value in macros.items():
                self.macros[key] = value

    def append_opers(self, in_class:object):
        if in_class:
            for fullname, coroutine in inspect.getmembers(in_class, predicate = inspect.isfunction):
                if fullname[0:1] == "_":
                    continue
                name = fullname.replace("multiple_", "").replace("single_", "")
                value = {
                    "group": in_class.__name__,
                    "coroutine": coroutine,
                    "doc": coroutine.__doc__,
                    "name": name,
                    "fullname": fullname,
                    "multiple": "multiple_" in fullname,
                }
                if value["multiple"]:
                    self.multiple_opers[name] = value
                else:       
                    self.single_opers[name] = value
    
    def get_data(self, name: str):
        """Вернуть результат выполнения заданного stage

        :param str stage_name: наименование stage
        :return list: данные stage
        """
        return mems.get_data(name = name)
        
    def set_data(self, name:str, data:list):
        """Запомнить результат выполнения stage

        :param str stage_name: наименование stage
        :param list data: результат выполнения stage
        """
        mems.set_data(name = name, value = data)

    def get_lines(self, in_list: list):
        out_list = []
        for text in in_list:
            # Проскочить заданные объекты    
            for line in text.split("\n"):
                _line = line.replace("\\", "/").strip()
                if len(_line):
                    out_list.append(_line)
        return out_list            

    def context(self, result, queue, date_start, stack = None):
        return {"result": result, "queue": queue, "start": date_start, "stop": datetime.datetime.now(), "stack": stack}

    async def function(self, stage_name:str, coroutine:object, pgm: dict, param: Param, p_queue: Param, in_queue: list, backtrace:list):
        out_queue = []
        date_start = datetime.datetime.now()
        _backtrace = " -> ".join(backtrace)
        try:
            # logger.info(f'++ "{_backtrace}" : in: "{len(in_queue)}"')
            result = await coroutine(pgm = pgm, param = param, p_queue = p_queue, in_queue = in_queue, out_queue = out_queue)
            # logger.info(f'-- "{_backtrace}": "{result}" out: "{len(out_queue)}"')
        except Exception as e:
            logger.error(f'backtraces: {" -> ".join(backtrace)}, error: {e}')    
            raise
        return self.context(result = result, queue = out_queue, date_start = date_start)

    async def execute(self, pgm:dict, in_queue:list, step:int = 0, options:dict = None, backtrace:list = None) -> list:
        """Выполнить блок программы

        :param dict pgm: блок программы
        :param list in_queue: входная очередь
        :param list out_queue: выходная очередь
        :param dict sub: массив библиотек
        :return bool: Если истина, то ветка выполняется дальше, иначе прерывается
        """
        # Операция выполнена нормально
        result = []
        stack_list = []
        stack_dict = {}
        out_queue = []
        start_date = datetime.datetime.now()
        if options and options.get("while"):
            # logger.info(f'while: {pgm=}')
            # Выполнить задачи в цикле
            __out_queue = []
            i = 0
            while 1:
                # Создать входную и выходную очередь для задач
                __in_queue = []
                # Скопировать первый раз входную очередь, далее результат предыдущего блока
                __in_queue.extend(in_queue if __out_queue is None else __out_queue)
                name = f'while'
                # Выполнить пакет задач
                _result = await self.execute(pgm = pgm, in_queue = __in_queue, step = step, backtrace = backtrace +[name])
                i += 1
                stack_list.append({f'iter {i}': _result})
                # Прервать выполнение далее блоков программы
                # break
                if 'break' in _result["result"]:
                    break
                # continue
                if 'continue' in _result["result"]:
                    continue
                __out_queue = _result["queue"]
            # Вернуть последнюю очередь, как результат, если все блоки были выполнены
            out_queue.extend(__out_queue)    
            result = ['success']
        elif isinstance(pgm, str):
            # Блок программы строка, сформируем словарь из команды и пустого параметра и рекурсивно вызовем себя
            _result = await self.execute(pgm = {pgm: None}, in_queue = in_queue, step = step, backtrace = backtrace)
            return _result
        elif isinstance(pgm, dict):
            # Блок программы словарь, если несколько задая, то выполнить параллельно
            # Создать входную и выходную очередь
            __in_queue = []
            __in_queue.extend(in_queue)
            __out_queue = []
            # Массив задач
            async_tasks = []
            # Сформируем список параллельно выполняемых блоков
            stages = ",".join([key for key in pgm])
            # Перебрать параллельные блоки 
            for stage_name, stage_data in pgm.items():
                # stage_name - наименование блока или функции
                # stage_data - параметры функции или тело блока
                if stage_name == "call":
                    # Вызвать подпрограмму из библиотеки, рекурсивно выполнить код функции
                    # Функция есть в классе Opers внутренних функций обработчика
                    __out_queue = []
                    name = f'{stage_name}'
                    async_tasks.append({"name": name, "out": __out_queue, "func": asyncio.create_task(self.execute(pgm = self.macros[Param(stage_data).string], in_queue = __in_queue, step = step + 1, backtrace = backtrace + [name]))})
                elif stage_name in self.single_opers:
                    # Функция есть в классе Opers внутренних функций обработчика
                    # Создать асинхронную задачу по функции и добавить в спсиок задач
                    # Param(stage_data) - параметры функции
                    # Param(__in_queue) - получить параметры входной очеререди
                    name = f'{stage_name}'
                    async_tasks.append({"name": name, "param": Param(stage_data).list, "out": __out_queue, "func": asyncio.create_task(self.function(stage_name = name, coroutine = self.single_opers[stage_name]["coroutine"], pgm = self, param = Param(stage_data), p_queue = Param(__in_queue), in_queue = __in_queue, backtrace = backtrace + [name]))})
                elif stage_name in self.multiple_opers:
                    # Функция есть в классе Opers внутренних функций обработчика
                    # Получить функцию 
                    # Создать асинхронную задачу по функции и добавить в спсиок задач
                    # Кол-во задач
                    task_count = 10 if len(__in_queue) > 10 else len(__in_queue)
                    # Param(stage_data) - параметры функции
                    # Param(__in_queue) - получить параметры входной очеререди
                    params = Param(stage_data)
                    if params.dict:
                        if params.get_float("tasks"):
                            task_count = int(params.get_float("tasks"))
                    for i in range(0, task_count):
                        name = f'{stage_name}[{i}]'
                        async_tasks.append({"name": name, "param": params.list, "out": __out_queue, "func": asyncio.create_task(self.function(stage_name = name, coroutine = self.multiple_opers[stage_name]["coroutine"], pgm = self, param = params, p_queue = Param(__in_queue), in_queue = __in_queue, backtrace = backtrace + [name]))})
                else:
                    # Если функция не найдена, то считаем, что пришел блок программы и создаем асинхронную задачу на его выполнение
                    name = f'{stage_name}'
                    async_tasks.append({"stage": 1, "out": __out_queue, "name": name, "func": asyncio.create_task(self.execute(pgm = stage_data, in_queue = __in_queue, step = step + 1, options = {"while": "while" in stage_name}, backtrace = backtrace + [name]))})
            # Выполнить пул задач
            # Время старта блока
            for task in async_tasks:
                _result = await task["func"]
                # if "st1" == task["name"]:
                #     logger.info(f'st1: {_result}')
                # "success" in _result
                if "stage" in task:
                    mems.set_data(task["name"], _result["queue"])
                if 'success' in _result["result"]:
                    out_queue.extend(_result["queue"])    
                if "param" in task:    
                    _result["param"] = task["param"]
                stack_dict[f'{task["name"]}'] = _result
                try:
                    result = result + _result["result"]
                except:
                    logger.info(f'error: {async_tasks=}, {result=}, {_result=}')   
                    raise 
                # Зафиксировать время выполнения всех задач в блоке    
        elif isinstance(pgm, list):
            # Последовательно выполнить задачи
            __out_queue = None
            for stage in pgm:
                # Создать входную и выходную очередь для задач
                __in_queue = []
                # Скопировать первый раз входную очередь, далее результат предыдущего блока
                __in_queue.extend(in_queue if __out_queue is None else __out_queue)
                __out_queue = []
                # Выполнить пакет задач
                # logger.debug(f'- ++{stage}')
                _result = await self.execute(pgm = stage, in_queue = __in_queue, step = step + 2, backtrace = backtrace + ['-'])
                # logger.debug(f'- --{stage}')
                __out_queue = _result["queue"]
                stack_list = stack_list + [_result]
                result = _result["result"]
                # Прервать выполнение далее блоков программы
                # result == "exit"
                if 'exit' in result:
                    break
                # result == "when"
                if 'when' in result:
                    break
                # result == "break"
                if 'break' in result:
                    break
                # result == "continue"
                if 'continue' in result:
                    break
            result = list(set(result))    
            # result == "success"
            if ['success'] == result:    
                # Вернуть последнюю очередь, как результат, если все блоки были выполнены
                out_queue.extend(__out_queue)    
            # "when" флаг вычеркнуть из результата
            result = ['success' if 'when' == elem else elem for elem in result]    
        return self.context(result = list(set(result)), queue = out_queue, date_start = start_date, stack = stack_list if stack_list else stack_dict)

    def traces(self, in_obj, short = True):
        if isinstance(in_obj, list):
            return [self.traces(t, short) for t in in_obj]
        elif isinstance(in_obj, dict):
            if "stack" in in_obj:
                return self.traces(in_obj["stack"], short)
            else:
                res_dict = {}
                for key in in_obj:
                    res = self.traces(in_obj[key], short)
                    obj = in_obj[key]
                    params = []
                    if not short:
                        if "result" in obj:
                            params.append(f'r:[{",".join(obj["result"])}]')
                        if "param" in obj and obj["param"]:
                            params.append(f'p:{obj["param"]}')
                        if "queue" in obj and obj["queue"]:
                            params.append(f'q:{obj["queue"]}')
                    param = ", ".join(params)
                    if res is None:
                        if len(param) > 0:
                            res_dict[key] = param
                        else:    
                            res_dict[key] = None
                    else:
                        if len(param) > 0:
                            res_dict[f'{key} % {param}'] = res
                        else:    
                            res_dict[f'{key}'] = res
                return res_dict
                    
    def get_stack(self, short = True):   
        return self.traces(self.result, short)             

    def get_queue(self):   
        return self.result["queue"]

    def get_seconds(self):   
        delta = self.result["stop"] - self.result["start"]
        return delta.total_seconds()
    
    def get_data_keys(self):
        return mems.get_data_keys()

    async def aio_go(self, pgm:dict):
        in_queue = []
        self.result = await self.execute(pgm = pgm, in_queue = in_queue, backtrace = [])
        return self.result

    def __getattr__(self, attr):
        if attr == "queue":
            return self.get_queue()
        elif attr == "mem":
            return self.get_data_keys()
        elif attr == "seconds":
            return self.get_seconds()
        elif attr == "stack":
            return self.get_stack()
        elif attr == "opers":
            return {**(self.multiple_opers or {}), **(self.single_opers or {})}

    def save_short_stack(self, request = None):
        if request:
            file_name = f'{request.node.module.__name__} {request.node.name}'
        else:    
            file_name = f'test'
        save_object(self.get_stack(short = True), f"{file_name} - stack")

    def save_stack(self, request = None):
        if request:
            file_name = f'{request.node.module.__name__} {request.node.name}'
        else:    
            file_name = f'test'
        save_object(self.get_stack(short = False), f"{file_name} - stack")

def pgm(pgm_code:dict, pgm_libs:dict = None, in_classes:list = None, datas:dict = None, request = None):
    # Создать объект управления выполнением задач, загрузив исходный текст программы
    # save_object(value_dict = pgm_code, filename = "pgm_code", tp = "json")
    __pgm = Pgm()
    # Добавить обработчик
    if in_classes:
        for in_class in in_classes:
            __pgm.append_opers(in_class = in_class)
    # Разобрать код макросов    
    if pgm_libs:        
        if isinstance(pgm_libs, dict):
            if "macros" in pgm_libs:
                pgm_libs = pgm_libs["macros"]
            # Добавит макросы в задачу
            __pgm.append_macros(pgm_libs)
    # Преобразовать исходный код    
    if isinstance(pgm_code, dict):
        if "macros" in pgm_code:
            __pgm.append_macros(pgm_code["macros"])
        if "main" in pgm_code:
            pgm_code = pgm_code["main"]
    # Установить начальные переменные
    mems.data.clear()
    if datas:
        for key, value in datas.items():
            mems.set_data(key, value)
    # Запустить лавный модуль программы
    result = asyncio.get_event_loop().run_until_complete(__pgm.aio_go(pgm = pgm_code))
    # if request:
    #     file_name = f'{request.node.module.__name__} {request.node.name}'
    #     # zilog_utils.save_object(result, f"{file_name} - result")
    #     zilog_utils.save_object(pgm.get_stack(short = True), f"{file_name} - stack")
    # logger.info(__pgm.queue)
    return __pgm
