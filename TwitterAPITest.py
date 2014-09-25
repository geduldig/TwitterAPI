import unittest
from mock import Mock
import requests
import warnings
#import TwitterAPI
from TwitterAPI.TwitterAPI import RestIterator, StreamingIterator, TwitterResponse, RestIterable, StreamingIterable

class TwitterAPITest(unittest.TestCase):


    def test_restiterator_deprecation(self):
        mock_response = Mock()
        mock_response.json.return_value = {"statuses": [{"tweet":"foo"}, {"tweet":"bar"}, {"tweet":"baz"}]} #actual data structure is different

        with warnings.catch_warnings(record=True) as w:
            rest_iterator = RestIterator(mock_response)
            actual_iterator = iter(rest_iterator)
            self.run_standard_tests(actual_iterator)
            self.assertIs(w[-1].category, DeprecationWarning)

    def test_restiterable(self):
        mock_response = Mock()
        mock_response.json.return_value = {"statuses": [{"tweet":"foo"}, {"tweet":"bar"}, {"tweet":"baz"}]} 

        rest_iterable = RestIterable(mock_response)
        actual_iterator = iter(rest_iterable)
        self.run_standard_tests(actual_iterator)
           
    def test_twitterresponse_old_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        twitter_response = TwitterResponse(mock_response, True)
        actual_iterator = iter(twitter_response.get_iterator())
        self.run_standard_tests(actual_iterator)

    def test_twitterresponse_new_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        twitter_response = TwitterResponse(mock_response, True)
        actual_iterator = iter(twitter_response)
        self.run_standard_tests(actual_iterator)

    def run_standard_tests(self, actual_iterator):
        self.assertEqual(next(actual_iterator), {"tweet":"foo"})
        self.assertEqual(next(actual_iterator), {"tweet":"bar"})
        self.assertEqual(next(actual_iterator), {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(actual_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(actual_iterator)



if __name__ == "__main__":
    unittest.main()

