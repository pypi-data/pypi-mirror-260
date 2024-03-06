import sys
import traceback

from web_edu.core.tasks import apply_async
from web_edu.plugins.analytic_collector.tasks import CollectorRun

from .utils import ERROR_FILE_NAME
from .utils import META_FILE_NAME
from .utils import get_report_meta_data
from .utils import get_report_provider
from .utils import get_report_xml
from .utils import save_result


@apply_async(queue=CollectorRun.CELERY_QUEUE)
def async_create_content(**kwargs):
    """Сбор показателя и сохранение в xml файл.

    Формирование файла с мета данными построения отчета.
    Или файла с ошибкой построения отчета."""

    report_code, report_uid, file_name = (
        kwargs.get('report_code', None),
        kwargs.get('report_uid', None),
        kwargs.get('file_name', None)
    )
    try:
        report_provider, ctx = get_report_provider(**kwargs)
        xml_string = get_report_xml(report_provider, ctx)
        meta_text = get_report_meta_data(report_provider)
        save_result(xml_string, report_code, report_uid, file_name)
        save_result(meta_text, report_code, report_uid, META_FILE_NAME)
    except Exception as exc:
        tb = traceback.format_exception(*sys.exc_info())
        error_text = ''.join(tb)
        save_result(error_text, report_code, report_uid, ERROR_FILE_NAME)
        raise
