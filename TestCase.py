class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self):
        getattr(self, self.name)()


class WasRun(TestCase):
    def __init__(self, name):
        self.wasRun = None
        TestCase.__init__(self, name)

    def testMethod(self):
        self.wasRun = 1


class TestCaseTest(TestCase):

    def testRunning(self):
        test = WasRun("testMethod")
        assert(not test.wasRun)
        test.run()
        assert(test.wasRun)

TestCaseTest("testRunning").run()