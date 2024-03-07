from datetime import datetime

from .aio_gitlab import git_pool

import logging
logger = logging.getLogger(__name__)

def str2date(date:str) -> datetime:
    """Преобразовать строку с датой в поле даты, отбросить временную зону

    :param str date: строка даты
    :return datetime: результат как дата
    """
    return datetime.fromisoformat(date).replace(tzinfo=None)

def my_strip(s: str) -> str:
    """Убрать переводы строк и сжать строку справа
    """
    return ' '.join(s.split()).rstrip()

class GitlabOpers:

    async def single_gitlab_projects(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список проектов в репозитории

        git_url:str - Подключение к gitlab
        git_token:str
        search:str = None - наименование проекта
        regex:str = None - regex шаблон отбора веток

        Входная очередь - не используется
        
        Результат массив проектов
        """
        gl = await git_pool.get_project(param = param)
        out_queue.extend(await gl.get_projects(param = param))
        return ['success']

    async def single_gitlab_branches(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список веток в репозитории

        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        search:str = None - наименование ветки
        regex:str = None - regex шаблон отбора веток

        Входная очередь - не используется
        
        Результат массив веток
        """
        gl = await git_pool.get_project(param = param)
        for branch in await gl.get_branches(param):
            out_queue.append(branch["name"])
        return ['success']

    async def multiple_gitlab_walk(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список файлов в репозитории

        tasks:int = None - Максимальное кол-во потоков обработки операций
        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        git_branch:str - ветка
        regex:str = None - regex шаблон отбора файлов

        Входная очередь, содержит список корневых узлов, от которых запускается процесс
        Все файлы в репозитории идут от "/"
        
        Результат массив
        - name: - имя файла
          path: - полный маршрут файла
        """
        if len(in_queue):
            gl = await git_pool.get_project(param = param)
        while len(in_queue):
            # Получить список файлов
            out_queue.extend(await gl.get_tree(param = param, path = in_queue.pop(0)))
        return ['success']

    async def multiple_gitlab_freads(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить содержимое файлов в репозитории

        tasks:int = None - Максимальное кол-во потоков обработки операций
        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        git_branch:str - ветка

        Входная очередь, содержит список файлов, полный маршрут от корня

        Результат массив
        - bom: 0
          branch: - ветка
          encode: cp1251 - найденная кодировка
          encode_detect: ASCII 
          encoding: 1 - файл раскодирован 
          path: - полный путь файла
          text: - содержимое файла 
        """
        if len(in_queue):
            gl = await git_pool.get_project(param = param)
            while len(in_queue):
                # Получить файл
                out_queue.append(await gl.get_file(param, in_queue.pop(0)))
        return ['success']


    async def single_gitlab_tags(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список тегов в репозитории

        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        search:str = None - наименование тега
        regex:str = None - regex шаблон отбора тегов

        Входная очередь - не используется
        
        Результат массив тегов
        """
        gl = await git_pool.get_project(param = param)
        out_queue.extend(await gl.get_tags(param))
        return ['success']


    async def multiple_gitlab_commits(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список тегов в репозитории

        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        
        Результат массив тегов
        """
        if len(in_queue):
            gl = await git_pool.get_project(param = param)
            while len(in_queue):
                # Получить ветку
                branch = in_queue.pop(0)
                if isinstance(branch, str) and len(branch) > 0:
                    for commit in await gl.get_commits(param, branch):
                        out_queue.append({
                            "branch": branch,
                            "id": commit["id"],
                            "last_committed_date": commit["committed_date"], # Commit, при rebase не изменяется
                            "last_committed_date2": str2date(commit["committed_date"]),
                            "committer_name": commit["committer_name"],
                            "authored_date": commit["authored_date"], # Commit, при rebase не изменяется
                            "authored_date2": str2date(commit["authored_date"]), # Commit, при rebase не изменяется
                            "author_name": commit["author_name"],
                            "last_message": my_strip(commit["message"]),
                            # "diff": await gl.get_diff(param, commit["id"]),
                        })
        return ['success']

    async def multiple_gitlab_diff(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Получить список измененых файлов по SHA commit

        tasks:int = None - кол-во потоков
        git_url:str - Подключение к gitlab
        git_token:str
        git_repo:str - проект репозитория
        
        Входная очередь массив sha или {"id":}
        Результат массив новых файлов
        """
        if len(in_queue):
            gl = await git_pool.get_project(param = param)
            while len(in_queue):
                # Получить ветку
                item = in_queue.pop(0)
                sha = item if isinstance(item, str) else item.get("id")
                if sha:
                    out_queue.extend(await gl.get_diff(param, sha))
        return ['success']
