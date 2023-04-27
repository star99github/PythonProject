"""
    作用：应用测试框架，创建多个测试用例，执行单元测试
    unittest的测试用例类继承 unittest.TestCase 类，在测试用例类中创建的以 test_ 开头的方法将会被视为测试方法,
    每一个测试方法（名称以 test_ 开头的方法）对应一个要测试的函数 / 功能 / 使用场景;
    内容为空的两个方法很特殊，它们是测试固件，用来执行一些特殊操作（注意这两个方法名称的大小写）:
        setUp() 方法会在每个测试方法执行前被调用，
        tearDown() 方法会在每个测试方法执行后被调用,
    如果把执行测试方法比作战斗，那么准备弹药、规划战术的工作就要在 setUp() 方法里完成，而打扫战场则要在 tearDown() 方法里完成。

    测试脚本编写完成后，执行 python Accoount_Test.py 命令即可执行脚本中的所有测试，并输出测试的结果、通过情况、总耗时等信息。

    用Coverage.py来检查测试覆盖率，先安装：pip install coverage，再执行命令：
        coverage run --source=app Account_Test.py：执行测试并检查测试覆盖率，--source：指定要检查的模块或包。
        coverage report：查看测试覆盖率报告
        coverage html：获取详细的 HTML 格式的覆盖率报告，会在当前目录生成一个 htmlcov 文件夹，打开其中的 index.html 即可查看覆盖率报告
"""
import unittest  # unittest是python标准库中的一个测试框架
from ..WatchList.Account import login
from ..WatchList import app_obj


# 测试用例类
class AppTestCase(unittest.TestCase):
    def setUp(self):
        print("每个测试方法执行前调用该方法")
        self.client = app_obj.test_client()  # 创建测试客户端，对该对象调用 get() 方法就相当于浏览器向服务器发送 GET 请求，调用 post() 则相当于浏览器向服务器发送 POST 请求，以此类推
        self.runner = app_obj.test_cli_runner()  # 创建测试命令运行器，返回一个命令运行器对象，对其调用 invoke() 方法可以执行命令，传入命令函数对象，或是使用 args 关键字直接给出命令参数列表。invoke() 方法返回的命令执行结果对象，它的 output 属性返回命令的输出信息

    def tearDown(self):
        print("每个测试方法执行完成后调用该方法")

    # 测试当前应用程序实例是否存在
    def test_appObjExist(self):
        self.assertIsNot(app_obj)

    # 测试当前应用是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app_obj.config["TESTING"])


class AccountTestCase(unittest.TestCase):
    def setUp(self):  # 测试固件
        print("每个测试方法执行前调用该方法")

    def tearDown(self):  # 测试固件
        print("每个测试方法执行完成后调用该方法")

    def test_login(self):  # 第 1 个测试
        rv = login()
        self.assertEqual(rv, 'Hello!')

    def test_login_to_somebody(self):  # 第 2 个测试
        rv = login(to='Grey')
        self.assertEqual(rv, 'Hello, Grey!')


if __name__ == "main":
    unittest.main()

