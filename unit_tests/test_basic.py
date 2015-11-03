import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.message = "Starting..."
        print(self.message)

    def test_upper(self):
        ''' Test for upper'''
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)
            
    def tearDown(self):
        print("Exiting...")

if __name__ == '__main__':
    unittest.main()
