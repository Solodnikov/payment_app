import os
from celery import Celery, signals
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('payment_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

logger = logging.getLogger('celery.task')


@signals.task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    """
    Обработчик сигнала, вызываемого перед запуском задачи Celery.

    Логирует имя задачи, её идентификатор и аргументы.

    :param task_id: Уникальный ID задачи
    :param task: Экземпляр задачи
    :param args: Позиционные аргументы задачи
    :param kwargs: Именованные аргументы задачи
    """
    logger.info(
        f'Task STARTED: {task.name}[{task_id}]\n'
        f'Args: {kwargs.get("args")}\n'
        f'Kwargs: {kwargs.get("kwargs")}'
    )


@signals.task_postrun.connect
def task_postrun_handler(task_id, task, retval, state, *args, **kwargs):
    """
    Обработчик сигнала, вызываемого после выполнения задачи Celery.

    Логирует результат задачи и её статус (успех или неудача).

    :param task_id: Уникальный ID задачи
    :param task: Экземпляр задачи
    :param retval: Возвращаемое значение задачи
    :param state: Состояние завершения задачи (например, 'SUCCESS')
    """
    if state == 'SUCCESS':
        logger.info(f'Task COMPLETED: {task.name}[{task_id}]\nResult: {retval}')
    else:
        logger.error(
            f'Task FAILED: {task.name}[{task_id}]\nState: {state}\nResult: {retval}'
        )


@signals.task_failure.connect
def task_failure_handler(sender, task_id, exception, traceback, args, kwargs, einfo, **kw):
    """
    Обработчик сигнала, вызываемого при сбое задачи Celery.

    Логирует исключение, аргументы и трассировку.

    :param sender: Задача, вызвавшая ошибку
    :param task_id: Уникальный ID задачи
    :param exception: Исключение, вызвавшее сбой
    :param traceback: Объект трассировки
    :param args: Позиционные аргументы задачи
    :param kwargs: Именованные аргументы задачи
    :param einfo: Полная информация об исключении (traceback, тип, сообщение)
    """
    logger.error(
        f'Task CRASHED: {sender.name}[{task_id}]\n'
        f'Args: {args}\nKwargs: {kwargs}\n'
        f'Exception: {str(exception)}\n'
        f'Traceback: {traceback}',
        exc_info=einfo,
    )
