import asyncio
import re
import httpx
import urllib
import chardet
import codecs
from datetime import date, datetime

import logging
logger = logging.getLogger(__name__)

class GitlabAsync:

    project = None
    
    async def httpx_get(self, url, raw = False):
        # logger.info(f'get: {url}')
        async with httpx.AsyncClient() as client:
            try:
                response =  await client.get(f'{url}', headers = {'Private-Token': self.token})
                # Если код возврата, ошибка, то поднять ошибку
                response.raise_for_status()
                if raw:
                    return response.content
                else:
                    return response.json()
            except httpx.HTTPError as exc:
                # Не поднимать ошибку, если нет доступа к teams
                logger.error(f'HTTP Exception for "{exc.request.url}" - "{exc}"')
                raise

    async def build_url(self, resources, **kwargs):
        url = []
        # Список проектов
        url += ["/projects" if resources.get("projects") else ""]
        # Проект зафиксирован
        url += [f"/projects/{resources.get('project_id')}" if resources.get("project_id") else ""]
        # Список веток
        url += ["/repository/branches" if resources.get("branches") else ""]
        url += ["/repository/commits" if resources.get("commits") else ""]
        # Список файлов
        url += ["/repository/tree" if resources.get("tree") else ""]
        # Спсиок tags
        url += ["/repository/tags" if resources.get("tags") else ""]
        # Получить содержимое файла
        url += [f"/repository/files/{resources.get('raw')}/raw" if resources.get("raw") else ""]
        # Получить diff коммита
        url += [f"/repository/commits/{resources.get('diff')}/diff" if resources.get("diff") else ""]
        # Получить параметры api, None не включать
        kwargs2 = urllib.parse.urlencode({key: value for key, value in kwargs.items() if value is not None})
        parameters = f"{kwargs2}"
        # Сформировать url строку запроса
        url_string = f"{self.url}/api/v4{''.join(url)}"
        # Вернуть строку запроса с параметрами
        return f"{url_string}?{parameters}" if parameters else url_string

    async def set_project(self, url, token, name):
        """Найти проект в репозитории и запомнить в классе

        :param str url: путь к gitlab
        :param str token: токен
        :param str name: имя репозитория
        """
        self.url = url
        self.token = token
        for project in await self.httpx_get(await self.build_url(resources = {"projects": True}, search = name)):
            self.project = project

    async def get_raw(self, resources, **kwarg):
        return await self.httpx_get(await self.build_url(resources = resources, **kwarg), raw = True)

    async def get_pages(self, resources, **kwarg):
        page = 0
        per_page = 50
        result = []
        while 1:
            page += 1
            records = await self.httpx_get(await self.build_url(resources = resources, **kwarg, page = page, per_page = per_page, pagination = "legacy"))
            if records:
                result.extend(records)
            if len(records) < per_page:
                break    
        return result

    async def get_branches(self, param):
        return await self.get_pages(
            resources = {
                "project_id": self.project["id"], 
                "branches": True}, 
            regex = param.get_string("regex"),
            search = param.get_string("search"))

    async def get_projects(self, param):
        result = []
        regex = param.get_string("regex")
        for project in await self.get_pages(
            resources = {
                "projects": True}, 
            search = param.get_string("search")):
            if regex and not re.match(regex, project["name"]):
                continue
            result.append(project["name"])
        return result    


    async def get_tags(self, param):
        result = []
        regex = param.get_string("regex")
        for tag in await self.get_pages(
            resources = {
                "project_id": self.project["id"], 
                "tags": True}, 
            search = param.get_string("search")):
            if regex and not re.match(regex, tag["name"]):
                continue
            result.append(tag["name"])
        return result    

# https://gitlabci.dpd.ru/api/v4/projects/260/repository/tree?id=260&iterator=true&page=2&pagination=legacy&path=Views%2F&per_page=20&recursive=true&ref=tests%2F2.133.0.0
    async def get_tree(self, param, path):
        result = []
        regex = param.get_string("regex")
        for file in await self.get_pages(
            resources = {
                "project_id": self.project["id"], 
                "tree": True}, 
            path = path, 
            recursive = "true",
            ref = param.get_string("git_branch")):
            if file["type"] == "tree":
                continue
            if regex and not re.match(regex, file["path"]):
                continue
            result.append({"path": file["path"], "name": file["name"]})
        return result

#https://gitlabci.dpd.ru/api/v4/projects/260/repository/files/!release%2FDSORT2-439%2F_source_upd%2Esql/raw?ref=tests%2F2.133.0.0 "HTTP/1.1 200 OK"
#https://gitlabci.dpd.ru/api/v4/projects/260/repository/files/Materialized+view+logs%2Farg_state%2Esql/raw?ref=tests%2F2.133.0.0'
    async def get_file(self, param, path):
        branch = param.get_string("git_branch")
        file_bytes = await self.get_raw(
            resources = {"project_id": self.project["id"], 
                         "raw": path.replace("/", "%2F").replace(".", "%2E")}, 
            ref = branch)
        # Определить кодировку файла
        file_encoding = chardet.detect(file_bytes)["encoding"]
        file_encoding = file_encoding.upper() if file_encoding else None
        # Определение формата входного файла и BOM
        # Переменная для определения BOM для UTF8 фалов
        bom = 0
        # Формат входного файла
        encode = "cp1251"
        if file_encoding in ["UTF-8-SIG", "UTF-8", "MACROMAN"]:
            encode = "utf-8"
            if file_bytes[0] == 239:  # Первый байт BOM
                bom = 1
        # Раскодировать входную байтовую строку, во внутренний формат
        file_str = ""                        
        encoding = 0
        try:
            file_str = codecs.decode(file_bytes, encode)
            encoding = 1
        except Exception:
            pass
        return {
            "branch": branch,
            "path": path,
            "encode_detect": file_encoding,
            "encode": encode,
            "bom": bom,
            "encoding": encoding,
            "text": file_str
        }    

    async def get_commits(self, param, branch):
        result = []
        for commit in await self.get_pages(
            resources = {
                "project_id": self.project["id"], 
                "commits": True}, 
            ref_name = branch, 
            since = date.fromisoformat(param.get_string("since")).isoformat() if param.get_string("since") else None):
            result.append(commit)
        return result

    async def get_diff(self, param, sha):
        result = []
        for diff in await self.get_pages(
            resources = {
                "project_id": self.project["id"], 
                "diff": sha}):
            result.append(diff["new_path"])
        return result


class Pool:

    pools = None

    def __init__(self):
        self.pools = {}

    async def get_project(self, param):
        url = param.get_string("git_url")
        token = param.get_string("git_token")
        repo = param.get_string("git_repo")
        key = f'{url=}::{token=}::{repo=}'
        if key not in self.pools:
            # Подключиться к репозиторию
            gl = GitlabAsync()
            await gl.set_project(url = url, token = token, name = repo)
            # Подключиться к проекту
            self.pools[key] = gl
        # logger.info(f'gitlab pool : {repo}@{url}')    
        return self.pools[key]
        
git_pool = Pool()  
