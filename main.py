#!/usr/bin/python3
import sys
import re
import ast

class MakeTests():
    def __init__(self, file: str):
        """
        This is a class to automate your tests

        TESTS

        ENDTESTS


        Tests:


        /*
        tests
            model: self.assertEqual(int(X1, 2), X2)
            cases:
                - "1" ==> 1
                - "110" ==> 2

            model: self.assertIsInstance(int(X1, 2), X2)
            cases:
                - "1" ==> int
                - "10" ==> int
        */
        """
        self.file = file
        classes = self.get_docstrings()
        self.output = ""

        for class_ in classes:
            self.write_class(class_[0])
            for methods in class_[1]:
                self.write_method(methods)
        open("test.py", "w").write(self.output)

    def docstring_to_test(docstring: str, function_name: str) -> tuple:
        models = MakeTests.get_models(docstring)
        docstring = r"""

            model: self.assertEqual(int(X1, 2), X2)
            cases:
                - "1" ==> 1
                - "110" ==> 2

            model: self.assertIsInstance(int(X1, 2), X2)
            cases:
                - "1" ==> int
                - "10" ==> int
                    """
        all_cases = re.findall(r"(?<=cases:\n)((\s*- .*\n)*)", docstring, re.MULTILINE)
        if all_cases is None:
            raise ValueError(f"Testcases must be pressent after each model. Missing in docstring of function {function_name}.")
            sys.exit()
        idx = 0
        final_cases = []
        for cases in all_cases:
            cases = cases[0]
            print(cases)
            cases = cases.split("\n")
            cases = [case for case in cases if len(case) > 0 and case != "\n"]
            cases = [case[case.find("- ") + len("- "):] for case in cases if len(case) > 0]
            cases = [case.split("==>") for case in cases]
            cases = [case for case in cases if len(case) > 0 and case != "\n"]
            if len(cases) > 0:
                final_cases.append(cases)
        return models, final_cases

    def write_class(self, classname):
        self.output += open("class_model.py").read().replace("NAME", classname)

    def write_method(self, method):
        name, (models, cases) = method
        print(cases)
        assert len(models) == len(cases)
        self.output += f"\n    def test_{name}(self):"
        for i in range(len(models)):
            for case in cases[i]:
                case_string = f"\n        {models[i]}"
                for x in range(len(case)):
                    case_string = case_string.replace(f"X{x + 1}", case[x])
                self.output += case_string.strip(" ")

    def get_models(docstring):
        m = re.findall("(?<=model:)[\S\W\D]*?(?=cases:)", docstring, re.MULTILINE)
        if m is None:
            raise ValueError(f"A model must be present in every docstring. Missing in docstring of function {function[1]}.")
            sys.exit()
        return [i for i in m if len(i) > 0]

    def get_docstrings(self):
        parsed = ast.parse(self.file)
        docstrings = []

        functions = [n for n in parsed.body if isinstance(n, ast.FunctionDef)]
        classes = [n for n in parsed.body if isinstance(n, ast.ClassDef)]

        # for function in functions:
            # docstrings.append(ast.get_docstring(function))

        idx = 0
        for class_ in  classes:
            #                  classname  methods
            docstrings.append((class_.name, []))
            methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
            for method in methods:
                docstring = ast.get_docstring(method)
                if docstring is not None:
                    m = re.search("\/\*\n*\t*tests[\W\D\S]*\*\/", docstring)
                    if m is not None:
                        docstrings[idx][1].append((method.name, MakeTests.docstring_to_test(docstring, method.name)))
            if docstrings[len(docstrings) - 1][1] == 0:
                docstrings.pop()
            idx += 1

        return docstrings

if __name__ == "__main__":
    try:
        #TODO: substitute with good args
        try:
            file = open(sys.argv[1]).read()
        except IndexError:
            print("Make sure to call the file with ./ and dont' forget to add the file")
            sys.exit()

    except FileNotFoundError:
        print("The file was not found")
        sys.exit()
    MakeTests(file)
