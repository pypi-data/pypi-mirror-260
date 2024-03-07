import unittest
from .test_base import TestConfig
from .test_client import TestClient
from .test_field import TestESField
from .test_es_door import TestESDoor
from .test_es_param import TestESParam
from .test_operators import TestOperators
from .test_es_builder import TestESBuilder
from .test_mock import TestESMockDSLInterface
from .test_es_query_util import TestESQueryUtil
from .test_in_query_param import TestInQueryParam


def whole_suite():
    # 创建测试加载器
    loader = unittest.TestLoader()
    # 创建测试包
    suite = unittest.TestSuite()
    # 遍历所有测试类

    test_cases = [
        TestConfig,
        TestESMockDSLInterface,
        TestOperators,
        TestESField,
        TestInQueryParam,
        TestESParam,
        TestESQueryUtil,
        TestClient,
        TestESBuilder,
        TestESDoor,
    ]

    for test_class in test_cases:
        # 从测试类中加载测试用例
        tests = loader.loadTestsFromTestCase(test_class)
        # 将测试用例添加到测试包中
        suite.addTests(tests)
    return suite


def test_es_util():
    ''' 运行所有的ES组件测试用例 '''
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(whole_suite())


if __name__ == '__main__':
    test_es_util()
