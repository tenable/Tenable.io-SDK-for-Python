import sys


class Logger(object):

    @staticmethod
    def error(message, context=None):
        Logger.log(message, context, True)

    @staticmethod
    def warn(message, context=None):
        Logger.log(message, context, True)

    @staticmethod
    def info(message, context=None):
        Logger.log(message, context)

    @staticmethod
    def log(message, context=None, error=False):
        if context:
            name = context.__name__ if hasattr(context, '__name__') else type(context).__name__
        else:
            name = sys._getframe().f_back.f_code.co_name
        message = '[%s] %s' % (name, message)

        if error:
            sys.stderr.write(message + '\n')
        print(message)


def payload_filter(payload, filter_):
    if callable(filter_):
        payload = {k: v for k, v in payload.items() if filter_(v, k)}
    elif filter:
        payload = {k: v for k, v in payload.items() if v is not None}
    return payload
