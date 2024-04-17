from arthur_bench.run.testsuite import TestSuite


class RunnableTest:
    test_name: str
    test_suite: TestSuite

    def __init__(self, test_name: str, test_suite: TestSuite):
        self.test_name = test_name
        self.test_suite = test_suite
