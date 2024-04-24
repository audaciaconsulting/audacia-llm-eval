from typing import List, Optional

import pandas
from arthur_bench.run.testsuite import TestSuite

from audacia_llm_eval.models.runnable_test import RunnableTest
from audacia_llm_eval.services.path_handler import create_file_path


def read_file(file_path: str) -> str:
    """
    Retrieve file contents as a string.

    Parameters:
        file_path (str): File to read.

    Returns:
        str: file contents as a string.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"File content read successfully: {file_path}")
            return content
    except FileNotFoundError:
        print(f"The file does not exist: {file_path}")
        raise


class TestList:
    runnable_tests: List[RunnableTest] = []

    def add_test_from_txt(self,
                          test_name: str,
                          scoring_method: str,
                          csv_path: str,
                          txt_file_root: Optional[str] = None,
                          input_column: str = "input",
                          txt_path_column: str = "txt_file") -> None:
        print(f'Adding test {test_name} from txt files...')
        data = pandas.read_csv(csv_path)
        inputs = data[input_column]
        txt_files = data[txt_path_column]

        expected_outputs = []
        for txt_file in txt_files:
            txt_path = txt_file
            if txt_file_root is not None:
                txt_path = create_file_path(txt_file_root, txt_file)
            content = read_file(txt_path)
            expected_outputs.append(content)

        self._add_test(test_name, scoring_method, inputs, expected_outputs)

    def add_test(self,
                 test_name: str,
                 scoring_method: str,
                 csv_path: str,
                 input_column: str = "input",
                 expected_output_column: str = "expected_output") -> None:
        data = pandas.read_csv(csv_path)
        inputs = data[input_column]
        reference_data = data[expected_output_column]

        self._add_test(test_name, scoring_method, inputs, reference_data)

    def _add_test(self,
                  test_name: str,
                  scoring_method: str,
                  inputs: List[str],
                  expected_outputs: List[str]):
        suite_name = f'{test_name}'
        test_suite = TestSuite(
            name=suite_name,
            scoring_method=scoring_method,
            input_text_list=inputs,
            reference_output_list=expected_outputs
        )

        test = RunnableTest(test_name, test_suite)
        self.runnable_tests.append(test)
