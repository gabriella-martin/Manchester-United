import unittest
import sys 
sys.path.insert(1, '/Users/gabriellamartin/Manchester-United' )
from pipelines.batch_pipeline import FBrefParser
from unittest.mock import patch, mock_open, MagicMock
from bs4 import BeautifulSoup 


class TestFBrefParser(unittest.TestCase):
    def setUp(self):
        self.mock_path = 'mock_html/Mock'
        self.parser = FBrefParser(club=self.mock_path)
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake html')
    @patch.object(BeautifulSoup, '__init__', return_value=None)
    def test_init(self, mock_soup_init, mock_open):
        parser = FBrefParser(self.mock_path)
        self.assertEqual(parser.club, self.mock_path)
        mock_open.assert_called_once_with(f'{self.mock_path}-Football-Data', 'rb')
        mock_soup_init.assert_called_once_with(b'fake html', 'html.parser')

    def test_standard_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.standard_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(actual_output, expected_ouput)

    def test_goalkeeper_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.goalkeeper_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', '0', 
                          '0', '0', '35', '100', '66', '10']
        self.assertEqual(actual_output, expected_ouput)

    def test_shooting_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.shooting_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0']
        self.assertEqual(actual_output, expected_ouput)

    def test_passing_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.passing_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', '1', '2', '1']

        self.assertEqual(actual_output, expected_ouput)

    def test_posession_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.possession_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', 
                          '1', '2', '1', '832', '695', '828', '4', '0', '0', '']

        self.assertEqual(actual_output, expected_ouput)

    def test_misc_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.misc_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', 
                          '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', '2']

        self.assertEqual(actual_output, expected_ouput)

    def test_defender_stats_table(self):
        #focus on first item of result 
        actual_output = (self.parser.defending_stats_table())[0]
        #I know what the mock HTML should return if this function works properly
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0',
                           '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', 
                           '43.2', '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', 
                           '2', '0', '0', '', '0', '0', '0', '10']

        self.assertEqual(actual_output, expected_ouput)

    def tearDown(self):
        del self.parser

class TestSalaryParser(unittest.TestCase):

    

if __name__ == '__main__':
    unittest.main()
