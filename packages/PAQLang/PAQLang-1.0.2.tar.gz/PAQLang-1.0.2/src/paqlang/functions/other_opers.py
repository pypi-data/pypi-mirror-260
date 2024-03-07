import asyncio
import re
import datetime
import aiofiles
from ..utils import aio_get_json, send_message, file_temp_path
from .util_opers import coalesce, get_condition

from ..param import Param, get_param
from ..data import mems

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class OtherOpers:

    async def single_opers(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вывести словарь операций"""
        group = param.get_string()
        for oper in {**pgm.single_opers, **pgm.multiple_opers}.values():
            if group is None or group == oper["group"]:
                out_queue.append(oper)
        return ['success']

    async def single_popers(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вывести словарь операций"""
        if param.get_list("group"):
            group = param.get_list("group")
        elif param.get_string("group"):
            group = [param.get_string("group")]
        elif param.get_string():
            group = [param.get_string()]
        else:
            group = None    
        file_name = param.get_string("file") or (file_temp_path() + (f"/README.md {group}" if group else "/README.md"))
        for char in ['[', ']', "'"]:
            file_name = file_name.replace(char, "")
        if file_name:
            async with aiofiles.open(file_name, mode = 'w', encoding = "utf-8") as f:
                opers = []
                opers += pgm.single_opers.values()
                opers += pgm.multiple_opers.values()
                for group in sorted(list(set([oper["group"] for oper in opers if group is None or oper["group"] in group]))):
                    logger.info(f'## {group}')
                    await f.write(f'## {group}\n')
                    for oper_name in sorted([oper["name"] for oper in opers if oper["group"] == group]):
                        for oper in [oper for oper in opers if oper["name"] == oper_name]:
                            logger.info(f'### {oper["name"]} {"(multiple)" if oper["multiple"] else ""}')
                            await f.write(f'### {oper["name"]} {"(multiple)" if oper["multiple"] else ""}\n')
                            if oper["doc"]:
                                await f.write(f'```\n')
                                for line in oper["doc"].split('\n'):
                                    await f.write(f'{line.strip()}\n')
                                await f.write(f'```\n')
        return ['success']

    # async def single_desc(pgm, param, p_queue, in_queue = None, out_queue = None):
    #     out_queue.extend(in_queue)
    #     logger.info(f'desc: {param.string}')
    #     return ['success']

    async def _print_message(pgm, param, p_queue, in_queue, out_queue, tp):
        """Отправить сообщение об ошибке или успешное
        """
        out_queue.extend(in_queue)
        # Получить наименование тестируемого атрибута
        test_attr = param.get_string("test-attr")
        send_attr = param.get_string("send-attr")
        # Очередь ошибок
        errors = []
        for elem in in_queue:
            result = True
            if test_attr:
                pelem = Param(elem)
                test_value = coalesce([pelem.get_float(test_attr), pelem.get_string(test_attr)])
                result = get_condition(test_value, param)
            if result:    
                if send_attr:
                    if send_attr in elem:
                        errors.append(f'{elem[send_attr]}')    
                else:        
                    errors.append(f'{elem}')
        if len(errors):        
            name = param.get_string("name") or param.get_string()
            if tp:
                logger.info(f' {name}{": " if name else ""}{errors}')
            else:    
                logger.error(f' {name}{": " if name else ""}{errors}')
        return ['success']    

    async def single_info(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вывести очередь в info поток

        Входная очередь сообщение
        name:str = None or param:str = None - заголовок
        test-attr:str = None - тестируемый аттрибут
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        send-attr:str = None - отправляемый атрибут иначе печатаем весь элемент
        """
        return await OtherOpers._print_message(pgm, param, p_queue, in_queue, out_queue, 1)

    async def single_error(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вывести очередь в error поток

        Входная очередь сообщение
        name:str = None or param:str = None - заголовок
        test-attr:str = None - тестируемый аттрибут
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        send-attr:str = None - отправляемый атрибут иначе печатаем весь элемент
        """
        return await OtherOpers._print_message(pgm, param, p_queue, in_queue, out_queue, 0)

    async def single_sleep(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Асинхронно заснуть на заданное кол-во секунд
        
        param:float - кол-во секунд, если не задано, то 1 секунда
        """
        sleep_sec = param.get_float() or 1
        logger.info(f'sleep: {sleep_sec}')
        await asyncio.sleep(sleep_sec)
        out_queue.extend(in_queue)
        return ['success']

    async def multiple_msleep(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Асинхронно заснуть на заданное кол-во секунд. 
        Запустить несколько потоков, в зависимости от входной очереди.
        Для отладки асинхронности
        
        in_queue:list - очередь задержек
        """
        while len(in_queue):
            # Вычислить время засыпания
            sleep_sec = Param(in_queue.pop(0)).get_float()
            if sleep_sec:
                logger.info(f'msleep: {sleep_sec}')
                await asyncio.sleep(sleep_sec)
        return ['success']

    async def multiple_include(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Загрузить подпрограммы

        Входная очередь - имена json и yaml файлов
        """
        while len(in_queue):
            # Получить имя файла
            file_name = in_queue.pop(0)
            if isinstance(file_name, str):
                subroutines = await aio_get_json(file_name = file_name)
                for key, item in subroutines.items():
                    pgm.macros[key] = item 
                    logger.info(f'include: {key}')
        return ['success']    
   
    async def _send_message(pgm, param, p_queue, in_queue, out_queue, tp):
        """Отправить сообщение об ошибке или успешное
        """
        out_queue.extend(in_queue)
        # Получить наименование тестируемого атрибута
        test_attr = param.get_string("test-attr")
        send_attr = param.get_string("send-attr")
        # Очередь ошибок
        errors = []
        for elem in in_queue:
            result = True
            if test_attr:
                pelem = Param(elem)
                test_value = coalesce([pelem.get_float(test_attr), pelem.get_string(test_attr)])
                result = get_condition(test_value, param)
            if result:    
                if send_attr:
                    if send_attr in elem:
                        errors.append(f'{elem[send_attr]}')    
                else:        
                    errors.append(f'{elem}')
        if len(errors):        
            await send_message(message = "\n".join(errors), success = tp, service = param.get_string("name") or param.get_string() or  "PAQLang")        
        return ['success']    

    async def single_send_errors(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Отправить сообщение об ошибке
        
        Входная очередь сообщение
        name:str = None or param:str = None - сообщение в заголовке, по умолчанию PAQLang
        test-attr:str = None - тестируемый аттрибут
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        send-attr:str = None - отправляемый атрибут иначе печатаем весь элемент
        """
        return await OtherOpers._send_message(pgm = pgm, param = param, p_queue = p_queue, in_queue = in_queue, out_queue = out_queue, tp = 0)

    async def single_send_success(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Отправить успешное сообщение
        
        Входная очередь сообщение
        name:str = None or param:str = None - сообщение в заголовке, по умолчанию PAQLang
        test-attr:str = None - тестируемый аттрибут
        Условие параметры "lt", "le", "eq", "ne", "gt", "ge", "instr", "notinstr"
        send-attr:str = None - отправляемый атрибут иначе печатаем весь элемент
        """
        return await OtherOpers._send_message(pgm = pgm, param = param, p_queue = p_queue, in_queue = in_queue, out_queue = out_queue, tp = 1)
