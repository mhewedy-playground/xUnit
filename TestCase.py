class TestCase:
    def __init__(self, name):
        self.name = name

    def setup(self):
        pass

    def run(self):
        self.setup()
        getattr(self, self.name)()
        self.tearDown()

    def tearDown(self):
        pass


class WasRun(TestCase):

    def setup(self):
        self.log = "setUp "

    def testMethod(self):
        self.log = self.log + "testMethod "
    
    def tearDown(self):
        self.log = self.log + "tearDown "


class TestCaseTest(TestCase):

    def testTemplateMethod(self):
        test = WasRun("testMethod")
        test.run()
        assert(test.log == "setUp testMethod tearDown ")


TestCaseTest("testTemplateMethod").run()
