import unittest
class TestNAME(unittest.TestCase):
    """Unit testing of class NAME."""

    def selftest(self) -> bool:
        """Perform self test by running various test cases.

         Binary uses module unittest for unit testing.
         See https://docs.python.org/3/library/unittest.html for details.

         Parameters:
         none

         Returns:
         bool: True if all tests pass, False if any single test fails
        """

        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestNAME)
        test_result = unittest.TextTestRunner().run(suite)
        err = len(test_result.errors)
        fail = len(test_result.failures)
        skip = len(test_result.skipped)
        run = test_result.testsRun
        ttl = suite.countTestCases()
        success = test_result.wasSuccessful()
        print("")
        print(f"Test results for class NAME are: ")
        print(f"    Total number of individual tests = {_BINARY_TOTAL_TESTS}")
        print(f"    Total number of unit tests       = {ttl}")
        print(f"    Unit tests executed              = {run}")
        print(f"    Unit tests skipped               = {skip}")
        print(f"    Unit tests failed                = {fail}")
        print(f"    Unit tests with error            = {err}")
        if success:
            result = f"Self-Test: 😃 All {run} out of {ttl} unit tests passed ✅"
            ret = True
        else:
            plural = "" if run - err - fail == 1 else "s"
            result = f"Self-Test: {run-err-fail} unit test{plural} passed ✅\n"
            plural = "" if err + fail == 1 else "s"
            result += f"Self-Test: {err+fail} unit test{plural} failed  ❌"
            ret = False
            print(f"{result}")
            return ret
