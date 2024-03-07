import datetime

# Стандартное логирование
import logging
# Установить текущи логгер
logger = logging.getLogger(__name__)

class DateOpers:

    async def single_now(pgm, param, p_queue, in_queue = None, out_queue = None):
        """Текущая дата в ISO формате, как строка

        """
        out_queue.append(datetime.datetime.now().isoformat())
        return ['success']
