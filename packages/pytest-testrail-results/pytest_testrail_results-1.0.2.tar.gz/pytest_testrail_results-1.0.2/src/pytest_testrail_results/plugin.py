# -*- coding: UTF-8 -*-
from datetime import datetime
from operator import itemgetter
from typing import Tuple, Optional, Any

import _pytest
from _pytest.nodes import Node
from _pytest.mark.structures import MarkDecorator
from _pytest.python import Function
from _pytest.config import Config
from _pytest.main import Session
from _pytest.runner import CallInfo
import pytest
import re
import warnings

from .testrail_api import APIClient

import logging

# Turn on if you want to see the logs

# Create a folder for logs if it does not already exist
# if "BITBUCKET_CLONE_DIR" in os.environ:
#     log_directory = os.path.join(os.environ["BITBUCKET_CLONE_DIR"], "logs")
# else:
#     log_directory = os.path.abspath("test_reports/logs/")
#
# if not os.path.exists(log_directory):
#     os.makedirs(log_directory)
#
# # Log file name
# log_file_name = os.path.join(log_directory, "testrail_plugin.log")
#
# # Logger setup
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# # Formatter for logs
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#
# # Handler for writing logs to a file
# file_handler = logging.FileHandler(log_file_name)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Formatter for logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# # Handler for writing logs to a file
# file_handler = logging.FileHandler(log_file_name)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


CUSTOM_TESTRAIL_STATUS = {
    "passed": 1,
    "blocked": 2,
    "untested": 3,
    "retest": 4,
    "failed": 5,
    "xfailed": 5,  # Mark expected failures as failed
    "xpassed": 1,  # Mark unexpected passes as passed
}

PYTEST_TO_TESTRAIL_STATUS = {
    "passed": CUSTOM_TESTRAIL_STATUS["passed"],
    "failed": CUSTOM_TESTRAIL_STATUS["failed"],
    "skipped": CUSTOM_TESTRAIL_STATUS["blocked"],
    "xpassed": CUSTOM_TESTRAIL_STATUS["passed"],
    "xfailed": CUSTOM_TESTRAIL_STATUS["failed"],
}

DT_FORMAT = "%d-%m-%Y %H:%M:%S"

TESTRAIL_PREFIX = "testrail"
TESTRAIL_DEFECTS_PREFIX = "testrail_defects"
ADD_RESULTS_URL = "add_results_for_cases/{}"
ADD_TESTRUN_URL = "add_run/{}"
CLOSE_TESTRUN_URL = "close_run/{}"
CLOSE_TESTPLAN_URL = "close_plan/{}"
GET_TESTRUN_URL = "get_run/{}"
GET_TESTPLAN_URL = "get_plan/{}"
GET_TESTS_URL = "get_tests/{}"

COMMENT_SIZE_LIMIT = 4000


class DeprecatedTestDecorator(DeprecationWarning):
    pass


warnings.simplefilter(action="once", category=DeprecatedTestDecorator, lineno=0)


class pytestrail(object):
    """
    An alternative to using the testrail function as a decorator for test cases, since pytest may confuse it as a test
    function since it has the 'test' prefix
    """

    @staticmethod
    def case(*ids: str) -> MarkDecorator:
        """
        Decorator to mark tests with testcase ids.

        i.e., @pytestrail.case('C123', 'C12345')

        :return pytest.mark:
        """
        return pytest.mark.testrail(ids=ids)

    @staticmethod
    def defect(*defect_ids: str) -> MarkDecorator:
        """
        Decorator to mark defects with defect ids.

        i.e. @pytestrail.defect('PF-513', 'BR-3255')

        :return pytest.mark:
        """
        return pytest.mark.testrail_defects(defect_ids=defect_ids)


def testrail(*ids: str) -> MarkDecorator:
    """
    Decorator to mark tests with testcase ids.

    ie. @testrail('C123', 'C12345')

    :return pytest.mark:
    """
    deprecation_msg = (
        "pytest_testrail: the @testrail decorator is deprecated and will be removed. Please use the "
        "@pytestrail.case decorator instead."
    )
    warnings.warn(deprecation_msg, DeprecatedTestDecorator)
    return pytestrail.case(*ids)


def get_test_outcome(outcome: str) -> int:
    """
    Return numerical value of a test outcome.

    :param str outcome: pytest reported test outcome value.
    :returns: int relating to a test outcome.
    """
    if outcome == "xfailed":
        logger.debug(
            f"Test outcome 'xfailed' is mapped to TestRail status {CUSTOM_TESTRAIL_STATUS['failed']}"
        )
        return CUSTOM_TESTRAIL_STATUS["failed"]
    elif outcome == "xpassed":
        logger.debug(
            f"Test outcome 'xpassed' is mapped to TestRail status {CUSTOM_TESTRAIL_STATUS['passed']}"
        )
        return CUSTOM_TESTRAIL_STATUS["passed"]
    logger.debug(
        f"Test outcome '{outcome}' is mapped to TestRail status {PYTEST_TO_TESTRAIL_STATUS[outcome]}"
    )
    return PYTEST_TO_TESTRAIL_STATUS[outcome]


def testrun_name() -> str:
    """Returns testrun name with timestamp"""
    now = datetime.utcnow()
    return "Automated Run {}".format(now.strftime(DT_FORMAT))


def clean_test_ids(test_ids: list[str]) -> list[int]:
    """
    Clean pytest marker containing testrail testcase ids.

    :param list test_ids: list of test_ids.
    :return list ints: contains a list of test_ids as ints.
    """
    return [
        int(match.groupdict()["test_id"])
        for test_id in test_ids
        if (match := re.search("(?P<test_id>[0-9]+$)", test_id)) is not None
        and "test_id" in match.groupdict()
    ]


def clean_test_defects(defect_ids: list[str]) -> list[str]:
    """
    Clean pytest marker containing testrail defects ids.

    :param list defect_ids: list of defect_ids.
    :return list str: contains a list of defect_ids as str.
    """
    return [
        match.groupdict()["defect_id"]
        for defect_id in defect_ids
        if (match := re.search("(?P<defect_id>.*)", defect_id)) is not None
        and "defect_id" in match.groupdict()
    ]


def get_testrail_keys(items: list[Node]) -> list[Tuple[Node, list[int]]]:
    """Return Tuple of Pytest nodes and TestRail ids from pytests markers"""
    testcaseids = []
    for item in items:
        marker = item.get_closest_marker(TESTRAIL_PREFIX)
        if marker is not None and hasattr(marker, "kwargs"):
            ids = marker.kwargs.get("ids")
            if ids is not None and isinstance(ids, list):
                testcaseids.append(
                    (
                        item,
                        clean_test_ids(ids),
                    )
                )
    return testcaseids


class PyTestRailPlugin(object):
    def __init__(
        self,
        client: APIClient,
        assign_user_id: int,
        project_id: int,
        suite_id: int,
        include_all: bool,
        cert_check: bool,
        tr_name: str,
        tr_description: str = "",
        run_id: int = 0,
        plan_id: int = 0,
        version: str = "",
        close_on_complete: bool = False,
        publish_blocked: bool = True,
        skip_missing: bool = False,
        milestone_id: Optional[int] = None,
        custom_comment: Optional[str] = None,
    ) -> None:
        self.assign_user_id = assign_user_id
        self.cert_check = cert_check
        self.client = client
        self.project_id = project_id
        self.results: list[dict[str, Any]] = []
        self.suite_id = suite_id
        self.include_all = include_all
        self.testrun_name = tr_name
        self.testrun_description = tr_description
        self.testrun_id = run_id
        self.testplan_id = plan_id
        self.version = version
        self.close_on_complete = close_on_complete
        self.publish_blocked = publish_blocked
        self.skip_missing = skip_missing
        self.milestone_id = milestone_id
        self.custom_comment = custom_comment
        self.need_new_testrun = False
        logger.debug("PyTestRailPlugin initialized")
        # pytest hooks

    def pytest_report_header(self, config: _pytest.config.Config, startdir: str) -> str:
        """Add extra-info in header"""
        logger.debug("Creating report header")
        message = "pytest-testrail: "
        if self.testplan_id:
            message += "existing testplan #{} selected".format(self.testplan_id)
        elif self.testrun_id:
            message += "existing testrun #{} selected".format(self.testrun_id)
        else:
            message += "a new testrun will be created"
        logger.debug("Report header created")
        return message

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(
        self, session: Session, config: Config, items: list[Node]
    ) -> None:
        logger.debug("Modifying collected items")
        items_with_tr_keys = get_testrail_keys(items)
        tr_keys = [case_id for item in items_with_tr_keys for case_id in item[1]]

        if self.testplan_id:
            if not self.is_testplan_available():
                self.create_test_run(
                    self.assign_user_id,
                    self.project_id,
                    self.suite_id,
                    self.include_all,
                    self.testrun_name,
                    tr_keys,
                    self.milestone_id,
                    self.testrun_description,
                )
        elif self.testrun_id:
            if not self.is_testrun_available():
                self.create_test_run(
                    self.assign_user_id,
                    self.project_id,
                    self.suite_id,
                    self.include_all,
                    self.testrun_name,
                    tr_keys,
                    self.milestone_id,
                    self.testrun_description,
                )
            elif self.skip_missing:
                tests = self.get_tests(self.testrun_id)
                if tests is not None:
                    tests_list = [test.get("case_id") for test in tests]
                else:
                    tests_list = []
                for item, case_id in items_with_tr_keys:
                    if not set(case_id).intersection(set(tests_list)):
                        mark = pytest.mark.skip("Test is not present in testrun.")
                        item.add_marker(mark)
        else:
            self.create_test_run(
                self.assign_user_id,
                self.project_id,
                self.suite_id,
                self.include_all,
                self.testrun_name,
                tr_keys,
                self.milestone_id,
                self.testrun_description,
            )

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item: Function, call: CallInfo) -> Any:
        """Collect result and associated testcases (TestRail) of an execution"""
        logger.info(f"Creating a test report for {item.name}")
        logger.debug(f"Creating report for test {item.name}")
        outcome = yield
        rep = outcome.get_result()

        # Logging the state of the rep object
        logger.debug(
            f"Test {item.name}: outcome={rep.outcome}, when={rep.when}, failed={rep.failed}, skipped={rep.skipped}, passed={rep.passed}"
        )

        # Check for xfail and change rep.outcome accordingly
        if "xfail" in item.keywords:
            logger.debug(f"Test {item.name} is marked as xfail")
            if rep.when == "call" and (rep.failed or rep.skipped):
                rep.outcome = "failed"
                logger.debug(f"Test {item.name} xfailed and marked as failed")
            elif rep.passed:
                rep.outcome = "passed"
                logger.debug(f"Test {item.name} xpassed")
            else:
                xfail_marker = item.get_closest_marker("xfail")
                if (
                    xfail_marker is not None
                    and xfail_marker.kwargs.get("run", True) == False
                ):
                    rep.outcome = "xfailed"  # Map 'xfail_run_false' to 'xfailed'
                    logger.debug(f"Test {item.name} is marked as xfail with run=False")

        logger.info(f"Completed processing test report for {item.name}")
        logger.debug(f"After xfail processing: {item.name} - Outcome: {rep.outcome}")

        # Add results to TestRail
        defectids = None
        test_parametrize = None
        if "callspec" in dir(item):
            test_parametrize = (
                list(item.callspec.params.values()) if item.callspec.params else None
            )
        comment = rep.longrepr
        defect_marker = item.get_closest_marker(TESTRAIL_DEFECTS_PREFIX)
        if defect_marker is not None:
            defectids = defect_marker.kwargs.get("defect_ids")
        test_marker = item.get_closest_marker(TESTRAIL_PREFIX)
        if test_marker is not None:
            testcaseids = test_marker.kwargs.get("ids")
            if testcaseids is not None:
                # Add results for both 'call' and 'setup' stages
                if rep.when == "call" or (
                    rep.when == "setup"
                    and (rep.outcome == "skipped" or rep.outcome == "xfailed")
                ):
                    if defectids is not None:
                        self.add_result(
                            item,
                            clean_test_ids(testcaseids),
                            rep,
                            comment=comment,
                            duration=rep.duration,
                            defects=str(clean_test_defects(defectids))
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", ""),
                            test_parametrize=test_parametrize,
                        )
                    else:
                        self.add_result(
                            item,
                            clean_test_ids(testcaseids),
                            rep,
                            comment=comment,
                            duration=rep.duration,
                            test_parametrize=test_parametrize,
                        )

    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Publish results in TestRail"""
        logger.debug("Session finished, publishing results")
        print("[{}] Start publishing".format(TESTRAIL_PREFIX))
        if self.results:
            tests_list = [str(result["case_id"]) for result in self.results]
            print(
                "[{}] Testcases to publish: {}".format(
                    TESTRAIL_PREFIX, ", ".join(tests_list)
                )
            )

            if self.testrun_id:
                self.add_results(self.testrun_id)
            elif self.testplan_id:
                testruns = self.get_available_testruns(self.testplan_id)
                print(
                    "[{}] Testruns to update: {}".format(
                        TESTRAIL_PREFIX, ", ".join([str(elt) for elt in testruns])
                    )
                )
                for testrun_id in testruns:
                    self.add_results(testrun_id)
            else:
                print("[{}] No data published".format(TESTRAIL_PREFIX))

            if self.close_on_complete and self.testrun_id:
                self.close_test_run(self.testrun_id)
            elif self.close_on_complete and self.testplan_id:
                self.close_test_plan(self.testplan_id)
        print("[{}] End publishing".format(TESTRAIL_PREFIX))

    def add_result(
        self,
        item: _pytest.python.Function,
        test_ids: list[int],
        rep: _pytest.runner.TestReport,
        comment: str = "",
        defects: Optional[str] = None,
        duration: float = 0,
        test_parametrize: Optional[list[Any]] = None,
    ) -> None:
        """
        Add a new result to result dict to be submitted at the end.

        :param item: The pytest Function object representing the test item.
        :param list test_parametrize: Add test parametrize to test result
        :param defects: Add defects to a test result
        :param list test_ids: list of test_ids.
        :param _pytest.runner.TestReport rep: Pytest report object with test result details.
        :param comment: None or a failure representation.
        :param duration: Time it took to run just the test.
        """
        logger.debug(f"Processing test result, initial outcome: {rep.outcome}")
        for test_id in test_ids:
            xfail_marker = item.get_closest_marker("xfail")
            if xfail_marker is not None and xfail_marker.kwargs.get("run", True):
                # If the test is marked as xfail and run=True
                status = (
                    CUSTOM_TESTRAIL_STATUS["failed"]
                    if rep.wasxfail
                    else CUSTOM_TESTRAIL_STATUS["blocked"]
                )
            else:
                # If the test is marked as xfail and run=False
                status = CUSTOM_TESTRAIL_STATUS["failed"]
            # For all other cases, use the general mapping
            status = get_test_outcome(rep.outcome)

            # Logging before adding result
            logger.debug(
                f"Adding result for test {test_id}: status={status}, outcome={rep.outcome}"
            )

            # Create a result record
            data = {
                "case_id": test_id,
                "status_id": status,
                "comment": comment,
                "duration": duration,
                "defects": defects,
                "test_parametrize": test_parametrize,
            }
            self.results.append(data)

        logger.debug("Test result added")

    def add_results(self, testrun_id: int) -> None:
        """
        Add results one by one to improve error handling.

        :param testrun_id: ID of the testrun to feed
        """
        logger.info(f"Adding results for testrun_id: {testrun_id}")
        logger.debug(f"Adding results for testrun_id: {testrun_id}")
        # Results are sorted by 'case_id' and by 'status_id' (the worst result at the end)
        self.results.sort(key=itemgetter("case_id"))

        # Manage a case of "blocked" testcases
        if self.publish_blocked is False:
            print(
                '[{}] Option "Don\'t publish blocked testcases" activated'.format(
                    TESTRAIL_PREFIX
                )
            )
            tests = self.get_tests(testrun_id)
            if tests is not None:
                blocked_tests_list = [
                    test.get("case_id")
                    for test in tests
                    if test.get("status_id") == CUSTOM_TESTRAIL_STATUS["blocked"]
                ]
            else:
                blocked_tests_list = []
            print(
                "[{}] Blocked testcases excluded: {}".format(
                    TESTRAIL_PREFIX, ", ".join(str(elt) for elt in blocked_tests_list)
                )
            )
            self.results = [
                result
                for result in self.results
                if result.get("case_id") not in blocked_tests_list
            ]

        # prompt enabling include all test cases from the test suite when creating test run
        if self.include_all:
            print(
                '[{}] Option "Include all testcases from test suite for test run" activated'.format(
                    TESTRAIL_PREFIX
                )
            )

        # Publish results
        data: dict[str, Any] = {"results": []}
        for result in self.results:
            logger.debug(
                f"Preparing to send result for case {result['case_id']} with status {result['status_id']}"
            )
            entry = {
                "status_id": result["status_id"],
                "case_id": result["case_id"],
                "defects": result["defects"],
            }
            if self.version:
                entry["version"] = self.version
            comment = result.get("comment", "")
            test_parametrize = result.get("test_parametrize", "")
            entry["comment"] = ""
            if test_parametrize:
                entry["comment"] += "# Test parametrize: #\n"
                entry["comment"] += str(test_parametrize) + "\n\n"
            if comment:
                if self.custom_comment:
                    entry["comment"] += self.custom_comment + "\n"
                    # Indent text to avoid string formatting by TestRail. Limit the size of comment.
                    entry["comment"] += "# Pytest result: #\n"
                    entry["comment"] += (
                        "Log truncated\n...\n"
                        if len(str(comment)) > COMMENT_SIZE_LIMIT
                        else ""
                    )
                    entry["comment"] += "    " + str(comment)[
                        -COMMENT_SIZE_LIMIT:
                    ].replace("\n", "\n    ")
                else:
                    # Indent text to avoid string formatting by TestRail. Limit the size of comment.
                    entry["comment"] += "# Pytest result: #\n"
                    entry["comment"] += (
                        "Log truncated\n...\n"
                        if len(str(comment)) > COMMENT_SIZE_LIMIT
                        else ""
                    )
                    entry["comment"] += "    " + str(comment)[
                        -COMMENT_SIZE_LIMIT:
                    ].replace("\n", "\n    ")
            elif comment == "":
                entry["comment"] = self.custom_comment
            duration = result.get("duration")
            if duration:
                duration = (
                    1 if (duration < 1) else int(round(duration))
                )  # TestRail API doesn't manage milliseconds
                entry["elapsed"] = str(duration) + "s"
            data["results"].append(entry)

        response = self.client.send_post(
            ADD_RESULTS_URL.format(testrun_id), data, cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            logger.error(f"Failed to add results: {error}")
            print(
                '[{}] Info: Testcases not published for following reason: "{}"'.format(
                    TESTRAIL_PREFIX, error
                )
            )
        else:
            logger.info("Results added successfully")

    def create_test_run(
        self,
        assign_user_id: int,
        project_id: int,
        suite_id: int,
        include_all: bool,
        testrun_name: str,
        tr_keys: list[int],
        milestone_id: Optional[int],
        description: str = "",
    ) -> None:
        """
        Create a test run with IDs collected from markers.

        :param assign_user_id: The ID of the user to whom the test run is assigned.
        :param project_id: The ID of the project in which the test run is created.
        :param suite_id: The ID of the test suite for the test run.
        :param include_all: Boolean indicating whether to include all test cases in the test run.
        :param testrun_name: The name of the test run.
        :param tr_keys: Collected TestRail IDs.
        :param milestone_id: The ID of the milestone associated with the test run. Optional.
        :param description: The description of the test run. Optional.
        """
        logger.info(f"Creating a test run named {testrun_name}")
        data = {
            "suite_id": suite_id,
            "name": testrun_name,
            "description": description,
            "assignedto_id": assign_user_id,
            "include_all": include_all,
            "case_ids": tr_keys,
            "milestone_id": milestone_id,
        }

        try:
            response = self.client.send_post(
                ADD_TESTRUN_URL.format(project_id), data, cert_check=self.cert_check
            )
            error = self.client.get_error(response)
            if error:
                # Log an error message if there is a problem with creating the test run
                logger.error(f'[TestRail Plugin] Error creating test run: "{error}"')
            else:
                # Log a success message with the new test run ID
                self.testrun_id = response["id"]
                logger.info(
                    f"[TestRail Plugin] Test run created successfully with ID={self.testrun_id}"
                )
        except Exception as e:
            # Log any unexpected exceptions during the test run creation
            logger.error(
                f"[TestRail Plugin] Unexpected error during test run creation: {e}"
            )

    def close_test_run(self, testrun_id: int) -> None:
        """
        Closes testrun.

        """
        response = self.client.send_post(
            CLOSE_TESTRUN_URL.format(testrun_id), data={}, cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print('[{}] Failed to close test run: "{}"'.format(TESTRAIL_PREFIX, error))
        else:
            print(
                "[{}] Test run with ID={} was closed".format(
                    TESTRAIL_PREFIX, self.testrun_id
                )
            )

    def close_test_plan(self, testplan_id: int) -> None:
        """
        Closes testrun.

        """
        response = self.client.send_post(
            CLOSE_TESTPLAN_URL.format(testplan_id), data={}, cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print('[{}] Failed to close test plan: "{}"'.format(TESTRAIL_PREFIX, error))
        else:
            print(
                "[{}] Test plan with ID={} was closed".format(
                    TESTRAIL_PREFIX, self.testplan_id
                )
            )

    def is_testrun_available(self) -> bool:
        """
        Ask if testrun is available in TestRail.

        :return: True if testrun exists AND is open
        """
        response = self.client.send_get(
            GET_TESTRUN_URL.format(self.testrun_id), cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print(
                '[{}] Failed to retrieve testrun: "{}"'.format(TESTRAIL_PREFIX, error)
            )
            return False

        return response["is_completed"] is False

    def is_testplan_available(self) -> bool:
        """
        Ask if testplan is available in TestRail.

        :return: True if testplan exists AND is open
        """
        response = self.client.send_get(
            GET_TESTPLAN_URL.format(self.testplan_id), cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print(
                '[{}] Failed to retrieve testplan: "{}"'.format(TESTRAIL_PREFIX, error)
            )
            return False

        return response["is_completed"] is False

    def get_available_testruns(self, plan_id: int) -> list[int]:
        """
        :return: a list of available testruns associated to a testplan in TestRail.

        """
        testruns_list = []
        response = self.client.send_get(
            GET_TESTPLAN_URL.format(plan_id), cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print(
                '[{}] Failed to retrieve testplan: "{}"'.format(TESTRAIL_PREFIX, error)
            )
        else:
            for entry in response["entries"]:
                for run in entry["runs"]:
                    if not run["is_completed"]:
                        testruns_list.append(run["id"])
        return testruns_list

    def get_tests(self, run_id: int) -> Optional[list[dict]]:
        """
        :return: the list of tests containing in a testrun.
        """
        response = self.client.send_get(
            GET_TESTS_URL.format(run_id), cert_check=self.cert_check
        )
        error = self.client.get_error(response)
        if error:
            print('[{}] Failed to get tests: "{}"'.format(TESTRAIL_PREFIX, error))
            return None
        return response
