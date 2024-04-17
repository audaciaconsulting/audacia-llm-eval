import datetime as dt
from langchain_openai import AzureChatOpenAI

from audacia_llm_eval.services.test_list import TestList


class TestRunner:
    openai_client: AzureChatOpenAI
    system_prompt: str

    def __init__(self,
                 azure_deployment: str,
                 openai_api_version: str,
                 system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.openai_client = AzureChatOpenAI(
            azure_deployment=azure_deployment,
            openai_api_version=openai_api_version
        )

    def run_tests(self, test_list: TestList) -> None:
        print(f"Running {len(test_list.runnable_tests)} tests...")
        for runnable_test in test_list.runnable_tests:
            input_texts = runnable_test.test_suite.input_texts
            count = len(input_texts)

            print(f"Generating {count} responses for test {runnable_test.test_name}")

            candidate_outputs = [self.get_openai_result(input_text, index, count) for index, input_text in
                                 enumerate(input_texts)]
            print("Responses generated.")
            date = dt.datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
            run_name = f"{runnable_test.test_name}_{date}"
            runnable_test.test_suite.run(
                run_name=run_name,
                candidate_output_list=candidate_outputs)

    def get_openai_result(self, input_text: str, index: int, count: int) -> str:
        print(f"Requesting {index + 1}/{count} input responses.")
        messages = [
            ("system", self.system_prompt),
            ("human", input_text),
        ]
        result = self.openai_client.invoke(messages)
        return result.content
