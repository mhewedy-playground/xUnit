import traceback


def list_test_methods(clazz):
    return filter(lambda x: not x.startswith("_")
                            and x not in ("setup", "run", "tear_down"), dir(clazz))


class TestResult:

    def __init__(self):
        self.runCount = 0
        self.failedCount = 0

    def test_started(self):
        self.runCount = self.runCount + 1

    def test_failed(self):
        self.failedCount = self.failedCount + 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.failedCount)


class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self, result):
        result.test_started()
        self.setup()
        try:
            getattr(self, self.name)()
        except AssertionError as ex:
            print "Assertion Failed: '%s' in %s.%s" % (ex, self.__class__.__name__, self.name)
            result.test_failed()
        except:
            print traceback.format_exc()
            result.test_failed()
        self.tear_down()

    def tear_down(self):
        pass


class TestSuite(TestCase):

    def __init__(self):
        self.tests = []
        TestCase.__init__(self, "TestSuite")

    def add(self, method_obj_or_class):
        if self.__is_method_object(method_obj_or_class):
            self.tests.append(method_obj_or_class)
        else:
            self.tests.extend(map(lambda x: globals()[method_obj_or_class.__name__](x),
                                  list_test_methods(method_obj_or_class)))

    def run(self, result):
        for test in self.tests:
            test.run(result)

    @staticmethod
    def __is_method_object(method_obj):
        return hasattr(method_obj, "name")


class WasRun(TestCase):

    def setup(self):
        self.log = "setUp "

    def test_method(self):
        self.log = self.log + "testMethod "

    def test_broken_method(self):
        raise Exception

    def tear_down(self):
        self.log = self.log + "tearDown "


def assert_equals(expected, actual):
    if expected != actual:
        raise AssertionError("%s is not equal to %s" % (expected, actual))


class TestCaseTest(TestCase):

    def setup(self):
        self.result = TestResult()

    def test_template_method(self):
        test = WasRun("test_method")
        test.run(TestResult())
        assert_equals("setUp testMethod tearDown ", test.log)

    def test_result(self):
        test = WasRun("test_method")
        test.run(self.result)
        assert_equals("1 run, 0 failed", self.result.summary())

    def test_failed_result(self):
        test = WasRun("test_broken_method")
        test.run(self.result)
        assert_equals("1 run, 1 failed", self.result.summary())

    def test_failed_result_formatting(self):
        self.result.test_started()
        self.result.test_failed()
        assert_equals("1 run, 1 failed", self.result.summary())

    def test_suite(self):
        suite = TestSuite()
        suite.add(WasRun("test_method"))
        suite.add(WasRun("test_broken_method"))
        suite.run(self.result)
        assert_equals("2 run, 1 failed", self.result.summary())

    def test_suite_by_class(self):
        suite = TestSuite()
        suite.add(WasRun)
        suite.run(self.result)
        assert_equals("2 run, 1 failed", self.result.summary())

    def test_get_all_methods_except_setup_and_tear_down(self):
        assert_equals(['test_broken_method', 'test_method'], list_test_methods(WasRun))

    def test_assert_equals(self):
        try:
            assert_equals(1, 3)
            assert None
        except AssertionError as ex:
            assert 1
            assert ex.args[0] == "1 is not equal to 3"

    def test_assert_equals_2(self):
        assert_equals(3, 3)
        assert 1


suite = TestSuite()
suite.add(TestCaseTest)
results = TestResult()
suite.run(results)
print results.summary()
