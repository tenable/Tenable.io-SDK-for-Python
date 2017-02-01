from time import sleep, time


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
        value = expression()
        max_check = 20
        while not condition(value) and max_check > 0:
            sleep(2 + max_check)
            max_check -= 1
            value = expression()
        assert condition(value), u'Timeout waiting for a condition.'
        return value
