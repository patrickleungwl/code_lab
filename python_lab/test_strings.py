import unittest

class TestStringMethods(unittest.TestCase):

    def test_concatenate(self):
        self.assertEqual(   "helloworld", 
                            "hello" + "world",
                            "Concatenate result not expected")


    def test_concatenate_single_quotes(self):
        self.assertEqual(   'helloworld', 
                            'hello' + 'world',
                            'Concatenate single quote result not expected')


    def test_multiply_string(self):
        self.assertEqual(   'hello' * 3,
                            'hellohellohello',
                            'Multiple string result not expected')


    def test_string_concat(self):
        self.assertEqual(   'hello 42',
                            'hello ' + str(42),
                            'String concat result not expected')


    def test_string_compare(self):
        str1 = 'hello'
        str2 = 'hello'
        self.assertTrue(    str1 == str2,
                            'Expect two strings to match' )


    def test_string_compare_diff(self):
        str1 = 'hello'
        str2 = 'hello2'
        self.assertFalse(   str1 == str2,
                            'Expect two strings to not match' )


    def test_string_in(self):
        str1 = 'hello'
        str2 = 'el'
        self.assertTrue(    str2 in str1,
                            'Expect to see str2 in str1' )


    def test_string_find(self):
        str1 = 'hello'
        str2 = 'el'
        self.assertEqual(   str1.find( str2 ),
                            1,
                            'Expect to find string' )
        self.assertEqual(   str1.find( 'notme' ),
                            -1,
                            'Expect to not find string' )



if __name__ == '__main__':
    unittest.main()



