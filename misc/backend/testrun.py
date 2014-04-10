from newrun import *
#This file is used for testing only
tmpdir = create_temp_dir("/home/smack/")

tests = []

test1 = TestCase("2 3 4 5 6 7", "4 9 16 25 36 49")
test2 = TestCase("5 4 3 2 0 3", "25 16 9 4 0 9")

tests.append(test1)
tests.append(test2)



c_sol       = Submission(tmpdir, "test.c",      "a.out",    100)
cpp_sol     = Submission(tmpdir, "test.cpp",    "b.out",    100)
java_sol    = Submission(tmpdir, "Test.java",   "Test",     100)
py_sol      = Submission(tmpdir, "test.py",     "test.py",  100)

c       = CompilerProfile("C",      ["c"],      "gcc {FILENAME} -o {BASENAME}", "", "./{BASENAME}","", "gcc")
cpp     = CompilerProfile("C++",    ["cpp"],    "g++ {FILENAME} -o {BASENAME}", "", "./{BASENAME}","", "g++")
java    = CompilerProfile("java",   ["java"],   "javac {FILENAME}", "", "java {BASENAME}","", "openjdk-6-jdk")
py      = CompilerProfile("python", ["py"],     "",                 "", "python {BASENAME}", "", "python")

compile(java_sol,   java)
compile(c_sol,      c)
compile(cpp_sol,    cpp)
compile(py_sol,     py)


for test in tests:
    run_test(py_sol,    py,     test)
    run_test(c_sol,     c,      test)
    run_test(cpp_sol,   cpp,    test)
    run_test(java_sol,  java,   test)



remove_temp_dir(tmpdir)
