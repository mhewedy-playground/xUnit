import traceback


def listTestMethods(Class):
    return filter(lambda x: not x.startswith("_")
                            and x not in ("setup", "run", "tearDown"), dir(Class))


class TestResult:

    def __init__(self):
        self.runCount = 0
        self.failedCount = 0

    def testStarted(self):
        self.runCount = self.runCount + 1

    def testFailed(self):
        self.failedCount = self.failedCount + 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.failedCount)


class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self, result):
        result.testStarted()
        self.setup()
        try:
            getattr(self, self.name)()
        except AssertionError:
            # print "Assertion Failed: %s.%s" % (self.__class__.__name__, self.name)
            result.testFailed()
        except:
            # traceback.print_exc()
            result.testFailed()
        self.tearDown()

    def tearDown(self):
        pass


class TestSuite(TestCase):

    def __init__(self):
        self.tests = []
        TestCase.__init__(self, "TestSuite")

    def add(self, textElement):
        if hasattr(textElement, "name"):
            self.tests.append(textElement)
        else:
            self.tests.extend(map(lambda x: globals()[textElement.__name__](x),
                                  listTestMethods(textElement)))

    def run(self, result):
        for test in self.tests:
            test.run(result)


class WasRun(TestCase):

    def setup(self):
        self.log = "setUp "

    def testMethod(self):
        self.log = self.log + "testMethod "

    def testBrokenMethod(self):
        raise Exception

    def tearDown(self):
        self.log = self.log + "tearDown "


class TestCaseTest(TestCase):

    def setup(self):
        self.result = TestResult()

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run(TestResult())
        assert (test.log == "setUp testMethod tearDown ")

    def testResult(self):
        test = WasRun("testMethod")
        test.run(self.result)
        assert ("1 run, 0 failed" == self.result.summary())

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        test.run(self.result)
        assert ("1 run, 1 failed" == self.result.summary())

    def testFailedResultFormatting(self):
        self.result.testStarted()
        self.result.testFailed()
        assert (self.result.summary() == "1 run, 1 failed")

    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBrokenMethod"))
        suite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())

    def testSuiteByClass(self):
        suite = TestSuite()
        suite.add(WasRun)
        suite.run(self.result)
        assert ("2 run, 1 failed" == self.result.summary())

    def getAllMethodsExceptSetupAndTearDown(self):
        assert (listTestMethods(WasRun) == ['testBrokenMethod', 'testMethod'])


suite = TestSuite()
suite.add(TestCaseTest)
results = TestResult()
suite.run(results)
print results.summary()
