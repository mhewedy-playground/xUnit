from TestCase import TestSuite, TestResult


class Math:
    pass


if __name__ == '__main__':
    suite = TestSuite()
    suite.add(Math)
    results = TestResult()
    suite.run(results)
    print results.summary()
