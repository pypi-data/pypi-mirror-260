

# 生成测试
import unittest
import mipx


class TestMultidict(unittest.TestCase):

    def test_debug_var(self):
        model = mipx.Model()
        x = model.addVars(1, 3, name='x')
        y = model.addVar(name='y')
        status = model.optimize()
        mipx.debug_var(x.select("*", 2), False)
        mipx.debug_var(y, False)
        mipx.debug_var(x, False)
        mipx.debug_var([y], False)


if __name__ == '__main__':
    unittest.main()
