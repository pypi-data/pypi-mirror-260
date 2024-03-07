import asyncio

from paqlang.utils import aio_reads
from .gitlab_opers import git_pool

import cx_Oracle_async
import cx_Oracle

import logging
logger = logging.getLogger(__name__)

def split_blocks(text:str):
    """Разбить запрос на блоки выполнения по символу /
    """
    result = []
    delim = "-----/----EXECUTE-----/----"
    text2 = "\n".join([delim if line.strip() == "/" else line for line in text.split("\n")])
    # text4 = "\n".join([delim if line.strip() == ";" else line for line in text2.split("\n")])
    for code in text2.split(delim):
        if code.strip():
            result.append(code)
    return result        

class Pool:

    pools = None

    def __init__(self):
        self.pools = {}

    async def get(self, user, password, dsn):
        # Получить ключ pool
        key = f'{user=}::{password=}::{dsn=}'
        if key not in self.pools:
            self.pools[key] = await cx_Oracle_async.create_pool(
                    user = user, 
                    password = password, 
                    dsn = dsn,
                    min = 2,
                    max = 10)
        return self.pools[key]

pool = Pool()

class OracleOpers:

    async def execute(pgm, param, p_queue, in_queue = None, out_queue = None, fetch = None):
        if len(in_queue):
            # Получить подключение из pool коннекций
            oracle_pool = await pool.get(
                user = param.get_string("oracle_user"),
                password = param.get_string("oracle_password"),
                dsn = param.get_string("oracle_dsn"))
            # Если указано в параметрах подключение  gitlab, то подключиться к pool git
            gl = await git_pool.get_project(param = param) if "git_url" in param.dict else None
            # Провалится до курсора
            async with oracle_pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Пока входная очередь запросов или файлов не пустая
                    while len(in_queue):
                        # Получить первое значение из очереди
                        in_param = in_queue.pop(0)
                        if gl:
                            # Работаем с gitlab
                            try:
                                # Прочитать файл из git, передаем имя файла
                                file = await gl.get_file(param, in_param)
                            except Exception as e:
                                logger.error(f'get file: {in_param} - {e}')
                                raise    
                            # Имя файла
                            fname = file["path"]
                            # Содержимое файла
                            sql = file["text"]
                        else:   
                            # Если задана атрибут path, значит считать файл с локального диска 
                            if "path" in param.dict:
                                # Возможность задать кодировку файла
                                encoding = param.get_string("encoding") or "utf-8"
                                # 
                                path = param.get_string("path")
                                # Если path содержит, то сделать подстановку, иначе подставить имя файла как есть в очереди
                                fname = path.replace(":1", in_param) if path and (":1" in path) else in_param
                                # Прочитать содержимое файла
                                sql = await aio_reads(file_name = fname, encoding = encoding)
                            else:
                                # Запрос из потока, не из файла данных
                                fname = None
                                sql = in_param    
                        if fetch == "all":
                            # Получить все записи из запроса
                            await cursor.execute(sql)
                            columns = [col[0].lower() for col in cursor._cursor.description]
                            cursor._cursor.rowfactory = lambda *args: dict(zip(columns, args))
                            for row in await cursor.fetchall():
                                out_queue.append(row)
                        elif fetch == "one":
                            # Получить первую запись из запроса
                            await cursor.execute(sql)
                            columns = [col[0].lower() for col in cursor._cursor.description]
                            cursor._cursor.rowfactory = lambda *args: dict(zip(columns, args))
                            row = await cursor.fetchone()
                            if row:
                                out_queue.append(row)
                        else:
                            # Включить dbms_output
                            await cursor.callproc("dbms_output.enable")
                            try:
                                # Разбить запрос на подзапросы и выполнить каждый
                                for code in split_blocks(sql):
                                    logger.info(f'{code=}')
                                    await cursor.execute(code)
                                # Подготовить dbms_output
                                dbms_output = []
                                # Размер чтения порции строк из dbms_output
                                chunk_size = 100
                                # Создать преременные для чтения
                                lines_var = cursor._cursor.arrayvar(str, chunk_size)
                                num_lines_var = cursor._cursor.var(int)
                                num_lines_var.setvalue(0, chunk_size)
                                # Прочитать порциями dbms_output
                                while True:
                                    await cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                                    num_lines = num_lines_var.getvalue()
                                    lines = lines_var.getvalue()[:num_lines]
                                    for line in lines:
                                        dbms_output.append(line or "")
                                    if num_lines < chunk_size:
                                        break
                                # Вернуть все хорошо, с dbms_output    
                                result = {
                                    "result": 1,
                                    "output": '\n'.join(dbms_output)
                                }    
                            except  cx_Oracle.DatabaseError as e:            
                                # Заполнить ошибку выполнения
                                error, = e.args
                                result = {
                                    "errmsg": error.message,
                                    "result": 0
                                }
                            # Если запрос из файла, то добавить в результат имени файла
                            if fname:
                                logger.info(f'oracle exec: "{fname}"')
                                result["file"] = fname     
                            out_queue.append(result)

    async def multiple_oracle_execute(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Выполнить SQL запрос. Запросы разбиваются на подзапросы "/" и ";"

        oracle_user:str - Подключение к oracle
        oracle_password:str
        oracle_dsn:str

        Входная очередь:
        - если не заданы параметры, то список текстов запросов. 
        - если git_url:str, то список файлов из getlab. Файл загружается из git и выполняется. 
          Необходимы также git_token, git_repo, git_branch
        - если path:str, то список файлов из директория на диске. 
          Формат атрибута "...:1...". Вместо :1 подставляется заданный файл.
        
        Результат массив выполенных запросов
        {"result": 0 или 1, # 0 - error execute, 1 - succes execute
         "output":str, # строки dbms_output потока
         "errmsg":str, # ошибка выполнения, если result = 0
         "file":str, # путь к файлу, если запрос был загружен из файла или git
        }
        """
        await OracleOpers.execute(pgm, param, p_queue, in_queue, out_queue, fetch = False)
        return ['success']

    async def multiple_oracle_fetchall(pgm, param, p_queue, in_queue = None, out_queue = None):
        await OracleOpers.execute(pgm, param, p_queue, in_queue, out_queue, fetch = "all")
        return ['success']

    async def multiple_oracle_fetchone(pgm, param, p_queue, in_queue = None, out_queue = None):
        await OracleOpers.execute(pgm, param, p_queue, in_queue, out_queue, fetch = "one")
        return ['success']
