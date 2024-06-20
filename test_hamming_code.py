import unittest
from hamming_code import HCResult, HammingCode


class TestHammingCode(unittest.TestCase):
    def test_instance(self):
        """ Essential: Test class instantiation """
        test1=HammingCode()
        if not isinstance(test1, HammingCode):
            self.fail('Unable to instantiate')

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        test2=HammingCode()
        a,b=test2.decode((1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1))
        a_expected=(1, 0, 1, 1, 0, 1)
        self.assertEqual(a,a_expected)
        self.assertEqual(b,HCResult.VALID)

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        test3=HammingCode()
        a,b=test3.decode((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
        a_expected=(0, 0, 0, 0, 0, 0)
        c,d=test3.decode((1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1))
        c_expected=(1, 1, 1, 1, 1, 0)
        e,f=test3.decode((0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0))
        e_expected=(0, 1, 1, 0, 1, 1)
        self.assertEqual(a,a_expected)
        self.assertEqual(b,HCResult.CORRECTED)
        self.assertEqual(c,c_expected)
        self.assertEqual(d,HCResult.CORRECTED)
        self.assertEqual(e,e_expected)
        self.assertEqual(f,HCResult.CORRECTED)
        f,g=test3.decode((1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1))
        self.assertEqual(f,(1, 0, 1, 1, 0, 1))
        self.assertEqual(g,HCResult.CORRECTED)

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        test4=HammingCode()
        a,b=test4.decode((1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1))
        self.assertEqual(a,None)
        self.assertEqual(b,HCResult.UNCORRECTABLE)

    def test_encode(self):
        """ Essential: Test method encode() """
        test5=HammingCode()
        a=test5.encode((0,1,1,0,1,1))
        a_expected=(0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)
        b=test5.encode((0,0,0,0,0,0))
        b_expected=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        c=test5.encode((1,0,1,1,0,1))
        c_expected=(1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)
        d=test5.encode((1,1,1,1,1,0))
        d_expected=(1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)
        self.assertEqual(a,a_expected)
        self.assertEqual(b,b_expected)
        self.assertEqual(c,c_expected)
        self.assertEqual(d,d_expected)


if __name__ == '__main__':
    unittest.main()