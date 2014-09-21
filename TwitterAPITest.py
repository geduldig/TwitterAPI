import unittest
from mock import Mock
import requests
from TwitterAPI.TwitterAPI import RestIterator, StreamingIterator, TwitterResponse

class TwitterAPITest(unittest.TestCase):

    def test_restiterator_next_old_way(self):
        mock_response = Mock()
        mock_response.json.return_value = {"statuses": [{"tweet":"foo"}, {"tweet":"bar"}, {"tweet":"baz"}]} #actual data structure is different
        
        rest_iterator = RestIterator(mock_response)
        actual_iterator = iter(rest_iterator)

        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(actual_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(actual_iterator)
    
    def test_restiterator_next_new_way(self):
        mock_response = Mock()
        mock_response.json.return_value = {"statuses": [{"tweet":"foo"}, {"tweet":"bar"}, {"tweet":"baz"}]} 
        
        rest_iterator = RestIterator(mock_response)

        next_thing = next(rest_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(rest_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(rest_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(rest_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(rest_iterator)

    def test_streamingiterator_next_old_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        streaming_iterator = StreamingIterator(mock_response)
        actual_iterator = iter(streaming_iterator)

        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(actual_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(actual_iterator)
    
    def test_streamingiterator_next_new_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        streaming_iterator = StreamingIterator(mock_response)

        next_thing = next(streaming_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(streaming_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(streaming_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(streaming_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(streaming_iterator)
  
    def test_twitterresponse_next_old_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        twitter_response = TwitterResponse(mock_response, True)
        actual_iterator = iter(twitter_response.get_iterator())

        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(actual_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(actual_iterator)

    def test_twitterresponse_next_new_way(self):
        mock_response = Mock()
        mock_data = []
        mock_data.append('{"tweet":"foo"}'.encode('utf-8'))
        mock_data.append('{"tweet":"bar"}'.encode('utf-8'))
        mock_data.append('{"tweet":"baz"}'.encode('utf-8'))
        mock_response.iter_lines.return_value = mock_data
        twitter_response = TwitterResponse(mock_response, True)
        actual_iterator = iter(twitter_response)

        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"foo"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"bar"})
        next_thing = next(actual_iterator)
        self.assertEqual(next_thing, {"tweet":"baz"})
        with self.assertRaises(StopIteration):
            next_thing = next(actual_iterator)
        #must continue to raise error, not reset
        with self.assertRaises(StopIteration): 
            next_thing = next(actual_iterator)
     
if __name__ == "__main__":
    unittest.main()
