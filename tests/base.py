from time import sleep, time
from tests.config import TenableIOTestConfig

WAIT_TIMEOUT = int(TenableIOTestConfig.get('wait_timeout'))


class BaseTest(object):

    def setup_method(self, method):
        if not hasattr(self, '_timer'):
            self._timer = {}
        print("\n%s:%s is running." % (type(self).__name__, method.__name__))
        self._timer[method.__name__] = time()

    def teardown_method(self, method):
        duration = time() - self._timer[method.__name__]
        print("\n%s:%s took (%s seconds)." % (type(self).__name__, method.__name__, duration))

    @staticmethod
    def wait_until(expression, condition):
        assert WAIT_TIMEOUT >= 0, u'Invalid wait_timeout value.'

        value = expression()
        start_time = time()
        wait_interval = 20
        elapsed = 0
        while not condition(value) and elapsed <= WAIT_TIMEOUT:
            sleep(wait_interval)
            if wait_interval > 2:  # Wait no less than 2 seconds in between.
                wait_interval -= 1
            value = expression()
            elapsed = time() - start_time
        assert condition(value), u'Timeout waiting for a condition (%d seconds elapsed).' % elapsed
        return value
