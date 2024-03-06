import datetime
import os
from django.conf import settings
from spyne import Fault

from web_edu.plugins.analytic_collector.models import CollectorProvider
from web_edu.plugins.analytic_collector.helpers import CollectPeriod
from web_edu.plugins.analytic_collector.helpers import ProviderContext
from web_edu.plugins.analytic_collector.xmlutils import pretty_xml

from edu_to_analytics.service.utils import PERIOD_DATE
from edu_to_analytics.service.utils import PERIOD_PERIOD
from edu_to_analytics.service.utils import PERIOD_TODAY
from edu_to_analytics.service.utils import PERIOD_YESTERDAY


ERROR_FILE_NAME = 'error.txt'
META_FILE_NAME = 'meta.txt'

periods_map = {
    PERIOD_TODAY: CollectPeriod.CURRENT_DAY,
    PERIOD_YESTERDAY: CollectPeriod.BEFORE_DAY,
    PERIOD_DATE: CollectPeriod.EXACT_DATE,
    PERIOD_PERIOD: CollectPeriod.EXACT_PERIOD
}


def get_content(**kwargs):
    """Формирование содержимого ответа на запрос и запись в файл."""

    report_provider, ctx = get_report_provider(**kwargs)
    xml_string = get_report_xml(report_provider, ctx)
    content = xml_string.encode('utf8')
    save_result(content, kwargs['report_code'],
                kwargs['report_uid'], kwargs['file_name'])
    return content


def save_result(result, report_code, report_uid=None, file_name=None):
    """Сохранение результата в файл.

    Если определен параметр `report_uid`, то возможно
    задание не уникального имени в `file_name`."""

    if report_uid and file_name:
        dir_name = os.path.join('async', report_uid)
    else:
        now = datetime.datetime.now().strftime('%m_%d_%Y_%H-%M-%S')
        file_name = '{}.xml'.format(now)
        dir_name = report_code

    full_path = os.path.join(
        settings.MEDIA_ROOT, settings.UPLOADS, __name__.split('.')[0],
        dir_name, file_name
    )
    path = os.path.dirname(full_path)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(full_path, 'w') as f:
        f.write(result)


def get_report_provider(**kwargs):
    """Возврат провайдара отчета и контекста формирования."""

    collector_type = periods_map.get(kwargs['period_type'])
    if collector_type == CollectPeriod.EXACT_PERIOD:
        target_dtime = (
            datetime.datetime.combine(kwargs['date_from'], datetime.time.min),
            datetime.datetime.combine(kwargs['date_to'], datetime.time.max)
        )
    elif collector_type == CollectPeriod.EXACT_DATE:
        target_dtime = kwargs['date_from']
    else:
        target_dtime = None

    collector_period = CollectPeriod.get(
        collector_type, target_dtime=target_dtime)
    ctx = ProviderContext(collector_period, collector_type)
    collector_provider = CollectorProvider.objects.get(id=kwargs['report_code'])
    report_provider = collector_provider.cls()

    return report_provider, ctx


def get_report_xml(report_provider, ctx):
    """Сбор показателя и возврат в виде xml."""

    report_data = report_provider.build(ctx)
    result = pretty_xml(report_data)

    return result


def get_report_meta_data(report_provider):
    """Возврат мета данных формирования отчета."""

    assert report_provider.durations.init_time, 'Build report first'

    result = str(report_provider.durations)

    return result


def get_content_by_ident(ctx, report_uid):
    """Возврат сформированного отчета по уникальному идентификатору.

    Если данные не готовы, возвращается пустое имя файла и содержимое.
    В случае наличия ошибки построения отчета генерируется исключение."""

    path_to_result = os.path.join(
        settings.MEDIA_ROOT, settings.UPLOADS,
        __name__.split('.')[0], 'async', report_uid
    )

    content = file_name = None

    file_names = os.path.exists(path_to_result) and os.listdir(path_to_result)
    if file_names:
        if ERROR_FILE_NAME in file_names:
            # среди файлов есть файл с ошибкой
            raise Fault(faultstring='Во время формирования отчета '
                                    'возникла внутренняя ошибка.')
        else:
            # нет ошибки. исключение мета файла. останется отчет.
            file_name = tuple(fname for fname in file_names
                              if fname != META_FILE_NAME)[0]
            full_path = os.path.join(path_to_result, file_name)
            with open(full_path, 'r') as f:
                content = f.read()

    return file_name, content
