#!/usr/bin/env python3
import io
import unittest.mock
import unittest
from stack_machine import *

class TestStackMachine(unittest.TestCase):
    def setUp(self):
        self.sm = StackMachine()
    
    def test_instance(self):
        if not isinstance(self.sm, StackMachine):
            self.fail('Unable to instantiate')

    def test_top(self):
        self.sm.do((0,0,1,0,1,0))
        actual_value=self.sm.top()
        actual_type=type(self.sm.top())
        actual_length=len(actual_value)
        self.assertEqual(actual_type,tuple)
        self.assertEqual(actual_length,8)
        
    def test_do(self):
        self.sm.do((0,0,1,0,1,0))
        self.sm.do((0,1,0,0,0,1))
        self.sm.do((0,1,0,0,0,1))
        self.sm.do((0,1,0,1,1,0))
        self.sm.do((0,1,1,1,1,1))
        self.sm.do((0,0,0,1,0,0))
        self.sm.do((0,1,1,0,1,1))
        self.sm.do((0,0,0,1,0,0))
        self.sm.do((0,1,1,0,0,1))
        self.sm.do((0,0,0,1,1,0))
        self.sm.do((0,1,1,0,0,0))
        self.sm.do((1,0,0,0,1,0))
        self.sm.do((1,1,0,1,1,0))
        self.sm.do((1,0,1,0,0,0))
        self.sm.do((1,1,0,1,0,1))
        self.sm.do((0,0,0,1,0,1))
        self.sm.do((1,0,0,0,0,1))
        self.sm.do((0,1,0,0,0,0))
        final_result=self.sm.stack
        self.assertEqual(final_result,[])

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.sm.do((0,0,1,0,1,0))
            self.sm.do((0,0,0,0,0,0))
            self.sm.do((0,1,0,1,1,1))
            
    def test_not_enough_operands(self):
        with self.assertRaises(RangeError):
            self.sm.do((0,0,1,0,1,0))
            self.sm.do((0,1,0,1,1,1))
            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_func(self, mock_stdout):
        self.sm.do((1,1,0,1,0,1))
        self.sm.do((0,0,0,0,0,1))
        self.sm.do((1,0,0,0,0,1))
        actual_output=mock_stdout.getvalue()[:-1]
        self.assertEqual(actual_output,"R")
        self.assertEqual(0,self.sm.do((0,1,0,0,0,0)))
        self.sm.do((0,0,0,0,0,0))
        self.assertEqual(1,self.sm.do((0,1,0,0,0,1)))
        self.assertEqual(1,self.sm.do((0,1,0,0,1,0)))
        self.sm.do((0,0,0,0,1,0))
        self.assertEqual(1,self.sm.do((0,1,0,0,1,1)))
        self.assertEqual(1,self.sm.do((0,1,0,1,0,0)))
        self.sm.do((0,0,0,0,0,1))
        self.assertEqual(1,self.sm.do((0,1,0,1,0,1)))
        self.sm.do((0,0,0,1,0,0))
        self.assertEqual(1,self.sm.do((0,1,0,1,1,0)))
        self.sm.do((0,0,0,0,1,0))
        self.assertEqual(1,self.sm.do((0,1,0,1,1,1)))
        self.sm.do((0,0,0,0,1,1))
        self.assertEqual(1,self.sm.do((0,1,1,0,0,0)))
        self.sm.do((0,0,0,1,0,1))
        self.assertEqual(1,self.sm.do((0,1,1,0,0,1)))
        self.sm.do((0,0,0,0,0,1))
        self.assertEqual(1,self.sm.do((0,1,1,0,1,0)))
        self.sm.do((0,0,0,0,0,1))
        self.assertEqual(1,self.sm.do((0,1,1,0,1,1)))
        self.sm.do((1,0,1,0,0,1))
        self.assertEqual(1,self.sm.do((0,1,1,1,0,0)))
        self.sm.do((0,0,0,1,0,1))
        self.assertEqual(1,self.sm.do((0,1,1,1,0,1)))
        self.assertEqual(1,self.sm.do((0,1,1,1,1,0)))
        self.assertEqual(1,self.sm.do((0,1,1,1,1,1)))
        
if __name__ == '__main__':
    unittest.main()
