from typing import List

import pandas
from arthur_bench.run.testsuite import TestSuite
from audacia_llm_eval.models.runnable_test import RunnableTest


class TestList:
    runnable_tests: List[RunnableTest] = []

    def add_test(self,
                 test_name: str,
                 scoring_method: str,
                 csv_path: str,
                 input_column: str = "input",
                 expected_output_column: str = "expected_output") -> None:

        # Read the CSV
        data = pandas.read_csv(csv_path)
        # Read the input column
        inputs = data[input_column]
        # Read the expected output column
        reference_data = data[expected_output_column]

        suite_name = f'{test_name}'
        test_suite = TestSuite(
            name=suite_name,
            scoring_method=scoring_method,
            input_text_list=inputs,
            reference_output_list=reference_data
        )

        test = RunnableTest(test_name, test_suite)
        self.runnable_tests.append(test)
