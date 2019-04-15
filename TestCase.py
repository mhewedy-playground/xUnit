class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self):
        result = TestResult()
        result.testStarted()
        self.setup()
        try:
            getattr(self, self.name)()
        except:
            result.testFailed()
        self.tearDown()
        return result

    def tearDown(self):
        pass


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

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert (test.log == "setUp testMethod tearDown ")

    def testResult(self):
        test = WasRun("testMethod")
        result = test.run()
        assert ("1 run, 0 failed" == result.summary())

    def testFailedResult(self):
        test = WasRun("testBrokenMethod")
        result = test.run()
        assert ("1 run, 1 failed" == result.summary())

    def testFailedResultFormatting(self):
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert (result.summary() == "1 run, 1 failed")


print TestCaseTest("testTemplateMethod").run().summary()
print TestCaseTest("testResult").run().summary()
print TestCaseTest("testFailedResult").run().summary()
print TestCaseTest("testFailedResultFormatting").run().summary()
