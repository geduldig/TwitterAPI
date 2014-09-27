import unittest
from mock import Mock
import requests
import warnings
from TwitterAPI.TwitterAPI import (
    RestIterator, 
    StreamingIterator, 
    TwitterResponse, 
    _RestIterable, 
    _StreamingIterable
)


MOCK_RESPONSE = {"statuses": [{"tweet":"foo"}, {"tweet":"bar"}, {"tweet":"baz"}]}

MOCK_RESPONSE_LINES = [
    '{"tweet":"foo"}'.encode('utf-8'),
    '{"tweet":"bar"}'.encode('utf-8'),
    '{"tweet":"baz"}'.encode('utf-8')
]


class TwitterAPITest(unittest.TestCase):

    def test_restiterator_deprecation(self):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_RESPONSE

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            rest_iterator = RestIterator(mock_response)
            actual_iterator = iter(rest_iterator)
            self.run_standard_tests(actual_iterator)
            self.assertIs(w[-1].category, DeprecationWarning)

    def test_restiterable(self):
        mock_response = Mock()
        mock_response.json.return_value = MOCK_RESPONSE

        rest_iterable = _RestIterable(mock_response)
        actual_iterator = iter(rest_iterable)
        self.run_standard_tests(actual_iterator)
           
    def test_twitterresponse_old_way(self):
        mock_response = Mock()
        mock_response.iter_lines.return_value = MOCK_RESPONSE_LINES
        twitter_response = TwitterResponse(mock_response, True)
        actual_iterator = iter(twitter_response.get_iterator())
        self.run_standard_tests(actual_iterator)

    def test_twitterresponse_new_way(self):
        mock_response = Mock()
        mock_response.iter_lines.return_value = MOCK_RESPONSE_LINES
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