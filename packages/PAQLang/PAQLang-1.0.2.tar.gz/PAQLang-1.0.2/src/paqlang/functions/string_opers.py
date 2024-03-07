import logging
import re
# Установить текущи логгер
logger = logging.getLogger(__name__)

from .util_opers import get_attr

class StringOpers:

    async def single_search(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Отобрать элементы из очереди, удовлетворяющие условию

        in_queue - входная очередь
        attr:str - если указано, то анализировать атрибут из элемента очереди
        regex:str или param:str - условия отбора
        """
        attr = param.get_string("attr")
        regex = param.get_string("regex") or param.get_string()
        assert regex is not None, 'Не задан атрибут поиска "regex"'
        for elem in in_queue:
            m = re.match(regex, get_attr(attr, elem))
            if m:
                out_queue.append(elem)
        return ['success']

    async def single_match(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Вырезать из элемента, заданный regex подстроку

        in_queue - входная очередь
        regex:str или param:str - условие получения подстроки, группа 1
        """
        regex = param.get_string("regex") or param.get_string()
        assert regex is not None, 'Не задан атрибут поиска "regex"'
        for elem in in_queue:
            m = re.match(regex, elem)
            if m:
                out_queue.append(m.group(1))
        return ['success']

    async def single_replace(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Заменить во входной очереди, в строках, заданный regex на подстроку

        in_queue - входная очередь
        regex:str или param:str - условие получения подстроки
        dest:str - на что заменять, если не указано, заменяем на пустую строку
        """
        regex = param.get_string("regex") or param.get_string()
        dest = param.get_string("dest") or ""
        assert regex is not None, 'Не задан атрибут поиска "regex"'
        for text in in_queue:
            out_queue.append(re.sub(regex, dest, text))
        return ['success']

    async def single_subst(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Заменить в заданной строке :1, на элементы из входной очереди

        in_queue - входная очередь
        text:str или param:str - строка шаблон
        """
        text = param.get_string("text") or param.get_string()
        assert text is not None, 'Не задана исходная строка - шаблон'
        for elem in in_queue:
            out_queue.append(text.replace(":1", str(elem)))
        return ['success']

    async def single_split(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Разбить строку на элементы

        param:str - строка разбиения, по умолчанию \n"""
        attr = param.get_string("attr")
        split_str = param.get_string() or '\n'
        while len(in_queue):
            # Получить файл
            text = in_queue.pop(0)
            # Распарсить атрибут 
            text = get_attr(attr = attr, elem = text, is_raise = False) if attr else text
            if isinstance(text, str):
                #logger.info(f'{text=}')
                pass
            else:
                logger.error(f'{text=}')    
            # Проскочить заданные объекты    
            for line in text.split(split_str):
                _line = line.replace("\\", "/").strip()
                if len(_line):
                    out_queue.append(_line)
        return ['success']

    async def single_join(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Соединить элементы массива в строку

        param:str - строка объединения, по умолчанию \n
        """
        join_str = param.get_string() or '\n'
        out_queue.append(join_str.join([f'{elem}' for elem in in_queue if len(f'{elem}') > 0]))
        return ['success']

    async def single_transform(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Найти в списке элемент, независимо от регистра и вернуть правильное наименование

        """
        transform = {}
        for elem in param.list:
            if isinstance(elem, str):
                transform[elem.lower()] = elem
        for elem in in_queue:        
            if isinstance(elem, str):
                if elem.lower() in transform:
                    out_queue.append(transform[elem.lower()])
        return ['success']
