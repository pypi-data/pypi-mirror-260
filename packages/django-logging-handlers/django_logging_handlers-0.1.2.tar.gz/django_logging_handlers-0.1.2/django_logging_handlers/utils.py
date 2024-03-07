import sys

from django.views import debug


def retrieve_traceback_html(record):
    """
    This method allows to retrieve the HTML traceback even if the django project is set
    to DEBUG=False.
    """

    request = record.request

    if request is None:
        return None

    exc_type, exc_value, tb = sys.exc_info()
    reporter = debug.ExceptionReporter(record.request, exc_type, exc_value, tb)
    return reporter.get_traceback_html()
