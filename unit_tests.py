import unittest
from bot import Monitoring

monitor = Monitoring()

class BotCompareTesting(unittest.TestCase):

    def test_no_argumets_passed(self):
        with self.assertRaises(SystemExit) as cm:
            (isStringCorrect) = Monitoring.compare_string(monitor)

        the_exception = cm.exception
        self.assertEqual(the_exception.code, 3)

    def test_one_argumet_passed(self):
        (isStringCorrect) = Monitoring.compare_string(monitor, "12")
        self.assertAlmostEqual (isStringCorrect, (False), (True))

    def test_not_string_arguments_passed(self):
        with self.assertRaises(SystemExit) as cm:
            (isStringCorrect) = Monitoring.compare_string(monitor)

        the_exception = cm.exception
        self.assertEqual(the_exception.code, 3)


    def test_equilas_strings(self):
        (isStringCorrect) = Monitoring.compare_string(monitor, "hello", "hello")
        self.assertAlmostEqual (isStringCorrect, True)
       

    def test_not_equilas_string(self):
        (isStringCorrect) = Monitoring.compare_string(monitor, "hello", "bye")
        self.assertAlmostEqual (isStringCorrect, False)


class BotGetBodyTesting(unittest.TestCase):
    
    def test_no_argumets_passed(self):
        (responseBody) = Monitoring.get_body(monitor)
        assert type(responseBody) is str

    def test_one_argumet_passed(self):
        (responseBody) = Monitoring.get_body(monitor, "mail.ru")
        assert type(responseBody) is str

    def test_all_argumet_passed(self):
         (responseBody) = Monitoring.get_body(monitor, "www.mocky.io", "/")
         assert type(responseBody) is str
 
    def test_dont_exist_context(self):
         (responseBody) = Monitoring.get_body(monitor, "www.mocky.io", "/123")
         assert type(responseBody) is str
    
    def test_dont_exist_url(self):
        with self.assertRaises(SystemExit) as cm:
            (responseBody) = Monitoring.get_body(monitor, "www.mo.com", "/123")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)
 
    def test_not_string_arguments_passed(self):
        with self.assertRaises(SystemExit) as cm:
            (responseBody) = Monitoring.get_body(monitor, 123)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 2)


