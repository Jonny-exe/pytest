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
                - "10" ==> 2
        */
        """
        self.file = file
        classes = self.get_docstrings()
        # classes = MakeTests.filter_tests(classes)
        self.output = ""

        for class_ in classes:
            self.write_class(class_[0])
            for methods in class_[1]:
                self.write_method(methods)
        open("test.py", "w").write(self.output)

    def docstring_to_test(docstring: str, function_name: str) -> tuple:
        model = MakeTests.get_model(docstring)
        cases = re.search("(?<=cases:(\r|\n))((\t|\s)*- .*(\n|\r))*", docstring)
        if cases is None:
            raise ValueError(f"Testcases must be pressent after each model. Missing in docstring of function {function_name}.")
            sys.exit()
        cases = cases.group(0).split("\n")
        print(cases)
        cases = [case[case.find("- ") + len("- "):] for case in cases if len(case) > 0]
        cases = [case.split("==>") for case in cases]
        return model, cases

    def write_class(self, classname):
        self.output += open("class_model.py").read().replace("NAME", classname)

    def write_method(self, method):
        name, (model, cases) = method
        self.output += f"\n\tdef test_{name}(self):"
        print(model)
        for case in cases:
            case_string = f"\n\t\t{model}"
            for i in range(len(case)):
                case_string = case_string.replace(f"X{i + 1}", case[i])
            print(case_string, type(case_string))
            self.output += case_string.strip(" ")

    def get_model(docstring):
        m = re.findall("(?<=model:)[\W\D\S]*(?=cases:)", docstring)
        if m is None:
            raise ValueError(f"A model must be present in every docstring. Missing in docstring of function {function[1]}.")
            sys.exit()
        return m[0]

    def get_cases(docstring):
        m = re.findall("(?<=model:)[\W\D\S]*(?=cases:)", docstring)
        if m is None:
            raise ValueError(f"A model must be present in every docstring. Missing in docstring of function {function[1]}.")
        return m

    # def filter_tests(classes):
        # for i in range(len(classes)):
            # functions = classes[i][1]
            # for x in range(len(functions)):
                # print(functions[x][1])
                # m = re.search("\/\*\n*\t*tests[\W\D\S]*\*\/", functions[x][1])
                # if m is None:
                    # classes[i][1][x].pop(x)
            # if len(classes[i][1]) == 0:
                # classes.pop(i)
        # return classes

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

    except FileNotFoundError:
        print("The file was not found")
        sys.exit()
    MakeTests(file)
