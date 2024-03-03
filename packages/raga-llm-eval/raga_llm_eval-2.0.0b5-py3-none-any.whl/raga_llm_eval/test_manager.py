"""
TestManager: Manages and Executes the tests
"""

import json
import os
import pkgutil
import time
import warnings
from pathlib import Path

import toml
from prettytable import ALL, PrettyTable

from .tests.test_executor import TestExecutor
from .utils.utils import generate_fingerprint


class TestManager:
    """Class for managing and executing tests"""

    def __init__(self, openai_client):
        """
        Constructor for the class, initializes the openai_client and sets up supported_tests, test_executor, and test_methods.
        """
        self._openai_client = openai_client
        self.supported_tests = self._load_supported_tests()
        self._test_executor = TestExecutor(openai_client=self._openai_client)
        self._test_methods = self.__generate_test_methods()

    def __generate_test_methods(self):
        """
        Generate test methods based on supported tests and test executor.
        """
        test_method_prefix = "run_"
        test_names = self._supported_tests.keys()
        return {
            test_name: getattr(self._test_executor, test_method_prefix + test_name)
            for test_name in test_names
        }

    def _load_supported_tests(self):
        """
        Load supported tests from the test details TOML file and return the supported tests.
        """
        data = pkgutil.get_data("raga_llm_eval", "tests/test_details.toml")
        if data is not None:  # Check if data was successfully loaded
            data_str = data.decode("utf-8")  # Decode bytes to string
            self._supported_tests = toml.loads(data_str)
        else:
            raise FileNotFoundError("Could not load the test_details.toml file.")

        return self._supported_tests

    def _add_test(self, data=None, test_names=None, test_category=None, arguments=None):
        """
        Add a test to the execution queue with the given parameters and return the modified instance of the object.
        The data parameter can now also be a path to a JSON file containing the test data.

        Parameters:
            test_names (str or list): The name of the test or a list of test names to be added.
            data (dict or str or Path): A dictionary containing the prompt, response, expected_response, context, and concept_set for the test,
                                        or a string path or Path object to a JSON file with the same structure.
            arguments (dict, optional): Additional arguments for the test (default is None).

        Returns:
            self: The modified instance of the object with the test added to the execution queue.
        """

        tests_to_execute = []

        # check if the data is provided by the user or not
        if data is None or data == {}:
            for test_name in test_names:
                tests_to_execute.append(
                    {
                        "test_name": test_name,
                        "prompt": None,
                        "response": None,
                        "expected_response": None,
                        "context": None,
                        "concept_set": None,
                        "cost": None,
                        "latency": None,
                        "expected_context": None,
                        "substrings": None,
                        "competitors": None,
                        "topics": None,
                        "test_arguments": arguments or {},
                    }
                )
            return tests_to_execute

        # Check if data is a string or Path object assuming it could be a file path
        if isinstance(data, (str, Path)):
            data_path = str(data)
            if os.path.isfile(data_path):
                with open(data_path, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError as exc:
                        raise ValueError(
                            "The JSON file is not properly formatted."
                        ) from exc
            else:
                raise FileNotFoundError(
                    f"The specified file does not exist: {data_path}"
                )

        # Ensure inputs are in list form for uniform processing
        for key in data.keys():
            # ensure concept set is a list
            if key == "concept_set":
                if not isinstance(data[key], list):
                    raise ValueError("concept_set must be a list")

            if not isinstance(data[key], list):
                data[key] = [data[key]]

            if data[key] == [None]:
                data[key] = []

        # check if any of these is not present in the dict
        for val in [
            "prompt",
            "response",
            "expected_response",
            "context",
            "concept_set",
            "cost",
            "latency",
            "expected_context",
            "substrings",
            "competitors",
            "topics",
        ]:
            if val not in data.keys():
                data[val] = []

        # Check if test_category and test_names are both None
        if test_category is None and test_names is None:
            raise ValueError("test_category and test_names cannot both be None.")

        # Check if test_category and test_names are both not None
        if test_category is not None and test_names is not None:
            raise ValueError("test_category and test_names cannot both be specified.")

        # In case the test_category is all, then add all the test that the data can be run on
        if test_category is not None and "all" in test_category:
            test_names = []
            for name, details in self._supported_tests.items():
                # check if details["required_data"] is present in data and key is not none
                data_with_values = {
                    key: value for key, value in data.items() if len(value) != 0
                }
                if set(details["required_data"]).issubset(set(data_with_values.keys())):
                    test_names.append(name)

        elif (
            test_category is not None
        ):  # Find the test_names in the given test_categories
            test_names = []
            for name, details in self._supported_tests.items():
                for category in test_category:
                    if category in details["test_tags"]:
                        test_names.append(name)

        elif test_category is None:
            # Validate test names
            unsupported_tests = set(test_names) - set(self._supported_tests.keys())
            if unsupported_tests:
                raise ValueError(
                    f"Unsupported test(s): {unsupported_tests}. Supported tests: {list(self._supported_tests.keys())}."
                )

        prompt = data["prompt"]
        response = data["response"]
        expected_response = data["expected_response"]
        context = data["context"]
        concept_set = data["concept_set"]
        cost = data["cost"]
        latency = data["latency"]
        expected_context = data["expected_context"]
        substrings = data["substrings"]
        competitors = data["competitors"]
        topics = data["topics"]

        # handle none values
        max_length = max(
            len(x)
            for x in [
                prompt,
                response,
                expected_response,
                context,
                concept_set,
                cost,
                latency,
                expected_context,
                substrings,
                competitors,
                topics,
            ]
            if x is not None
        )

        prompt = [None] * max_length if len(prompt) == 0 else prompt
        response = [None] * max_length if len(response) == 0 else response
        expected_response = (
            [None] * max_length if len(expected_response) == 0 else expected_response
        )
        context = [None] * max_length if context is None else context
        expected_context = (
            [None] * max_length if len(expected_context) == 0 else expected_context
        )
        substrings = [None] * max_length if len(substrings) == 0 else substrings

        concept_set = [None] * max_length if len(concept_set) == 0 else concept_set
        cost = [None] * max_length if len(cost) == 0 else cost
        latency = [None] * max_length if len(latency) == 0 else latency
        competitors = [None] * max_length if len(competitors) == 0 else competitors
        topics = [None] * max_length if len(topics) == 0 else topics

        # if context is empty, fill it with None
        if len(context) == 0:
            context = [None] * max_length
        # if context has only a single element, make it a list
        if isinstance(context, list) and len(context) == 1:
            context = context * max_length

        if len(concept_set) != 1:
            concept_set = [concept_set] * max_length

        # Add each test to the execution queue
        for (
            cur_prompt,
            cur_response,
            cur_expected_response,
            cur_context,
            cur_concept_set,
            cur_cost,
            cur_latency,
            cur_expected_context,
            cur_substrings,
            cur_competitors,
            cur_topics,
        ) in zip(
            prompt,
            response,
            expected_response,
            context,
            concept_set,
            cost,
            latency,
            expected_context,
            substrings,
            competitors,
            topics,
        ):
            for test_name in test_names:
                tests_to_execute.append(
                    {
                        "test_name": test_name,
                        "prompt": cur_prompt,
                        "response": cur_response,
                        "expected_response": cur_expected_response,
                        "context": cur_context,
                        "concept_set": cur_concept_set,
                        "cost": cur_cost,
                        "latency": cur_latency,
                        "expected_context": cur_expected_context,
                        "substrings": cur_substrings,
                        "competitors": cur_competitors,
                        "topics": cur_topics,
                        "test_arguments": arguments or {},
                    }
                )

        return tests_to_execute

    def _run(self, tests_to_execute, eval_id=None):
        """
        Run the tests in the test suite.
        """
        results = []

        if not tests_to_execute:
            raise ValueError("🚫 No tests to execute.")

        # Start message
        total_tests = sum(
            (
                len(test_details["test_name"])
                if isinstance(test_details["test_name"], list)
                else 1
            )
            for test_details in tests_to_execute
        )
        print(f"🚀 Starting execution of {total_tests} tests...")

        test_counter = 0  # Initialize a counter for the tests
        for test_details in tests_to_execute:
            test_names = test_details["test_name"]
            if isinstance(test_names, str):
                test_names = [test_names]

            for each_test in test_names:
                test_counter += 1  # Increment the test counter
                print(
                    f"\n🔍 Test {test_counter} of {total_tests}: {each_test} starts..."
                )  # Show the count and name of the test

                if each_test in self._test_methods:
                    method = self._test_methods[each_test]
                    result = method(test_details)
                    result["test_name"] = each_test

                    # add the ids
                    result["evaluation_id"] = eval_id

                    # test_id
                    result["test_id"] = generate_fingerprint(each_test)

                    # test_run_id
                    test_details_for_test_run_id = {
                        key: value
                        for key, value in test_details.items()
                        if key in ["test_name", "test_arguments"]
                    }
                    result["test_run_id"] = generate_fingerprint(
                        test_details_for_test_run_id
                    )

                    # dataset_id
                    test_details_for_dataset_id = {
                        key: value
                        for key, value in test_details.items()
                        if key not in ["test_name", "test_arguments"]
                    }
                    result["dataset_id"] = generate_fingerprint(
                        test_details_for_dataset_id
                    )

                    results.append(result)
                    print(f"✅ Test completed: {each_test}.")
                else:
                    warnings.warn(
                        f"⚠️ Warning: Test method for {each_test} not implemented."
                    )

        # End message
        print(f"✨ All tests completed. Total tests executed: {test_counter}.")

        return results

    def list_available_tests(self):
        """
        List available tests and their details in a formatted table.
        """
        print(
            "📋 Below is the list of tests currently supported by our system. Stay tuned for more updates and additions!"
        )

        table = PrettyTable()
        table.field_names = ["SNo.", "Test Name", "Description"]

        try:
            for field_name in table.field_names:
                table.max_width[field_name] = {
                    "SNo.": 5,
                    "Test Name": 25,
                    "Description": 50,
                }.get(field_name, 20)
        except AttributeError:
            # pylint: disable=protected-access
            table._max_width = {"SNo.": 5, "Test Name": 25, "Description": 50}
        table.hrules = ALL

        for idx, (test_name, details) in enumerate(
            self._supported_tests.items(), start=1
        ):  # Start indexing from 1 for better readability
            table.add_row([idx, test_name, details["description"]])

        print(table)
        print()
