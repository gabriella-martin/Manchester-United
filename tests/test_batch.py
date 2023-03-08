import sys 
import unittest
sys.path.insert(1, '/Users/gabriellamartin/Manchester-United' )
from bs4 import BeautifulSoup 
from pipelines.batch_pipeline import FBrefParser, SalaryParser, MarketValueParser, PlayerNumberParser, DataProcessing
from unittest.mock import patch, mock_open



class TestFBrefParser(unittest.TestCase):
    def setUp(self):
        self.mock_path = 'tests/mock_html/Mock'
        self.parser = FBrefParser(club=self.mock_path)
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake html')
    @patch.object(BeautifulSoup, '__init__', return_value=None)
    def test_init(self, mock_soup_init, mock_open):
        parser = FBrefParser(self.mock_path)
        self.assertEqual(parser.club, self.mock_path)
        mock_open.assert_called_once_with(f'{self.mock_path}-Football-Data', 'rb')
        mock_soup_init.assert_called_once_with(b'fake html', 'html.parser')

    def test_standard_stats_table(self):

        actual_output = (self.parser.standard_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', '0', '0', '0']
        self.assertEqual(actual_output, expected_ouput)

    def test_goalkeeper_stats_table(self):

        actual_output = (self.parser.goalkeeper_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', '0', 
                          '0', '0', '35', '100', '66', '10']
        self.assertEqual(actual_output, expected_ouput)

    def test_shooting_stats_table(self):

        actual_output = (self.parser.shooting_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0']
        self.assertEqual(actual_output, expected_ouput)

    def test_passing_stats_table(self):

        actual_output = (self.parser.passing_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', '1', '2', '1']

        self.assertEqual(actual_output, expected_ouput)

    def test_posession_stats_table(self):

        actual_output = (self.parser.possession_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', 
                          '1', '2', '1', '832', '695', '828', '4', '0', '0', '']

        self.assertEqual(actual_output, expected_ouput)

    def test_misc_stats_table(self):

        actual_output = (self.parser.misc_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0', 
                          '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', '43.2', 
                          '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', '2']

        self.assertEqual(actual_output, expected_ouput)

    def test_defender_stats_table(self):

        actual_output = (self.parser.defending_stats_table())[0]
        expected_ouput = ['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0',
                           '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', 
                           '43.2', '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', 
                           '2', '0', '0', '', '0', '0', '0', '10']

        self.assertEqual(actual_output, expected_ouput)

    def tearDown(self):
        del self.parser



class TestSalaryParser(unittest.TestCase):
    def setUp(self):
        list_of_player_stats = [['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0',
                           '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', 
                           '43.2', '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', 
                           '2', '0', '0', '', '0', '0', '0', '10']]
        self.mock_path = 'tests/mock_html/Mock'
        self.parser = SalaryParser(club=self.mock_path, list_of_player_stats=list_of_player_stats)
        self.list_of_player_stats = self.parser.list_of_player_stats
        
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake html')
    @patch.object(BeautifulSoup, '__init__', return_value=None)
    def test_init(self, mock_soup_init, mock_open):
        parser = SalaryParser(club=self.mock_path, list_of_player_stats=self.list_of_player_stats)
        self.assertEqual(parser.club, self.mock_path)
        mock_open.assert_called_once_with(f'{self.mock_path}-Salary', 'rb')
        mock_soup_init.assert_called_once_with(b'fake html', 'html.parser')

    def test_get_salary(self):
        expected_output = self.list_of_player_stats[0] + [19500000]
        actual_output = (self.parser.get_salary())[0]
        self.assertEqual(actual_output, expected_output)
        
    def tearDown(self):
        del self.parser



class TestMarketValueParser(unittest.TestCase):

    def setUp(self):
        self.mock_path = 'tests/mock_html/Mock'
        list_of_player_stats = [['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0',
                           '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', 
                           '43.2', '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', 
                           '2', '0', '0', '', '0', '0', '0', '10', 19500000]]
        self.parser = MarketValueParser(club=self.mock_path, list_of_player_stats=list_of_player_stats)
        self.list_of_player_stats = self.parser.list_of_player_stats
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake html')
    @patch.object(BeautifulSoup, '__init__', return_value=None)
    def test_init(self, mock_soup_init, mock_open):
        parser = MarketValueParser(club=self.mock_path, list_of_player_stats=self.list_of_player_stats)
        self.assertEqual(parser.club, self.mock_path)
        mock_open.assert_called_once_with(f'{self.mock_path}-Market-Value', 'rb')
        mock_soup_init.assert_called_once_with(b'fake html', 'html.parser')

    def test_get_market_worth(self):
        expected_output = self.list_of_player_stats[0] + [5192000.0]
        actual_output = (self.parser.get_market_worth())[0]
        self.assertEqual(actual_output, expected_output)
        
    def tearDown(self):
        del self.parser

    


class TestPlayerNumberParser(unittest.TestCase):

    def setUp(self):
        self.mock_path = 'tests/mock_html/Mock'
        list_of_player_stats = [['David de Gea', 'ESP', 'GK', '32', '25', '25', 2250, '25.0', '0', '0', '0',
                           '0', '0', '0', '35', '100', '66', '10', '0', '0', '72.0', '100.0', '98.4', 
                           '43.2', '1', '2', '1', '832', '695', '828', '4', '0', '0', '', '100.0', '0', 
                           '2', '0', '0', '', '0', '0', '0', '10', 19500000, 5192000.0]]    
        self.parser = PlayerNumberParser(club=self.mock_path, list_of_player_stats=list_of_player_stats)
        self.list_of_player_stats = self.parser.list_of_player_stats
    
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake html')
    @patch.object(BeautifulSoup, '__init__', return_value=None)
    def test_init(self, mock_soup_init, mock_open):
        parser = PlayerNumberParser(club=self.mock_path, list_of_player_stats=self.list_of_player_stats)
        self.assertEqual(parser.club, self.mock_path)
        mock_open.assert_called_once_with(f'{self.mock_path}-Number', 'rb')
        mock_soup_init.assert_called_once_with(b'fake html', 'html.parser')

    def test_get_market_worth(self):
        expected_output = self.list_of_player_stats[0] + ['1']
        actual_output = (self.parser.get_player_number())[0]
        self.assertEqual(actual_output, expected_output)
        
    def tearDown(self):
        del self.parser

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.club = 'Mock Club'
        list_of_player_stats = [
            ['Cristiano Ronaldo', 'Portugal', 'FW', '36', '20', '19', '1710', '19.0', '12', '2', '1', '0', '100', '67', '', '', '', '', '51', '25', '36', '9', '5', '20', '6', '29', '24', '200', '6', '90', '21', '33', '30', '3', '2', '17', '1', '8', '18', '10', '11', '1', '0', '0', '0', '0', '€100.00m', '7'],
            ['Bruno Fernandes', 'Portugal', 'MF', '27', '25', '24', '2151', '23.9', '10', '7', '3', '0', '73', '40', '', '', '', '-', '82', '57', '15', '5', '1', '14', '4', '45', '15', '144', '2', '77', '18', '43', '42', '23', '11', '49', '4', '20', '29', '27', '12', '1', '0', '0', '0', '0', '€100.00m', '18'],
            ['Marcus Rashford', 'England', 'FW', '24', '19', '16', '1360', '15.1', '7', '7', '3', '0', '50', '30', '', '', '', '', '46', '26', '19', '3', '3', '11', '2', '28', '11', '173', '6', '53', '14', '18', '16', '19', '8', '39', '4', '11', '16', '11', '12', '0', '0', '0', '0', '0', '€100.00m', '10']
        ]
        self.processor = DataProcessing(self.club, list_of_player_stats=list_of_player_stats)

    def test_remove_ronaldo(self):
        actual_output = self.processor.remove_ronaldo()

        
        expected_output = [
            ['Bruno Fernandes', 'Portugal', 'MF', '27', '25', '24', '2151', '23.9', '10', '7', '3', '0', '73', '40', '', '', '', '-', '82', '57', '15', '5', '1', '14', '4', '45', '15', '144', '2', '77', '18', '43', '42', '23', '11', '49', '4', '20', '29', '27', '12', '1', '0', '0', '0', '0', '€100.00m', '18'],
            ['Marcus Rashford', 'England', 'FW', '24', '19', '16', '1360', '15.1', '7', '7', '3', '0', '50', '30', '', '', '', '', '46', '26', '19', '3', '3', '11', '2', '28', '11', '173', '6', '53', '14', '18', '16', '19', '8', '39', '4', '11', '16', '11', '12', '0', '0', '0', '0', '0', '€100.00m', '10']]

        self.assertEqual(actual_output, expected_output)

    def test_empty_values_to_null(self):
        actual_output = self.processor.empty_values_to_null()
        expected_output = [
            ['Bruno Fernandes', 'Portugal', 'MF', '27', '25', '24', '2151', '23.9', '10', '7', '3', '0', '73', '40', 'NULL', 'NULL', 'NULL', 'NULL', '82', '57', '15', '5', '1', '14', '4', '45', '15', '144', '2', '77', '18', '43', '42', '23', '11', '49', '4', '20', '29', '27', '12', '1', '0', '0', '0', '0', '€100.00m', '18'],
            ['Marcus Rashford', 'England', 'FW', '24', '19', '16', '1360', '15.1', '7', '7', '3', '0', '50', '30', 'NULL', 'NULL', 'NULL', 'NULL', '46', '26', '19', '3', '3', '11', '2', '28', '11', '173', '6', '53', '14', '18', '16', '19', '8', '39', '4', '11', '16', '11', '12', '0', '0', '0', '0', '0', '€100.00m', '10']]
        self.assertEqual(actual_output, expected_output)
        
    def test_add_club(self):
        actual_output = self.processor.add_club()
        expected_output = [
            ['Bruno Fernandes', 'Portugal', 'MF', '27', '25', '24', '2151', '23.9', '10', '7', '3', '0', '73', '40', 'NULL', 'NULL', 'NULL', 'NULL', '82', '57', '15', '5', '1', '14', '4', '45', '15', '144', '2', '77', '18', '43', '42', '23', '11', '49', '4', '20', '29', '27', '12', '1', '0', '0', '0', '0', '€100.00m', '18', 'Mock Club'],
            ['Marcus Rashford', 'England', 'FW', '24', '19', '16', '1360', '15.1', '7', '7', '3', '0', '50', '30', 'NULL', 'NULL', 'NULL', 'NULL', '46', '26', '19', '3', '3', '11', '2', '28', '11', '173', '6', '53', '14', '18', '16', '19', '8', '39', '4', '11', '16', '11', '12', '0', '0', '0', '0', '0', '€100.00m', '10', 'Mock Club']]
        self.assertEqual(actual_output, expected_output)

    def tearDown(self):
        del self.processor


if __name__ == '__main__':
    unittest.main()
