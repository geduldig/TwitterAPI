import unittest
import TwitterAPI


class IteratorTest(unittest.TestCase):

    """Test REST API and Streaming API iterators."""

    def setUp(self):
        """Read credentials from TwitterAPI/credentials.txt. You
        must copy your credentials into this text file.
        """
        oa = TwitterAPI.TwitterOAuth.read_file()
        self.api = TwitterAPI.TwitterAPI(oa.consumer_key,
                                         oa.consumer_secret,
                                         oa.access_token_key,
                                         oa.access_token_secret)

    def test_rest_iterator(self):
        r = self.api.request('search/tweets', {'q': 'pizza'})
        self.assertIsInstance(r, TwitterAPI.TwitterResponse)
        # 200 means success
        self.assertEqual(r.status_code, 200)
        it = r.get_iterator()
        self.use_iterator(it)

    def test_streaming_iterator(self):
        r = self.api.request('statuses/filter', {'track': 'pizza'})
        self.assertIsInstance(r, TwitterAPI.TwitterResponse)
        # 200 means success
        # 420 means too many simultaneous connections, ok
        self.assertIn(r.status_code, [200, 420])
        if r.status_code == 200:
            it = r.get_iterator()
            self.use_iterator(it)

    def test_paging_iterator(self):
        pager = TwitterAPI.TwitterRestPager(self.api,
                                            'search/tweets',
                                            {'q': 'pizza'})
        self.assertIsInstance(pager, TwitterAPI.TwitterRestPager)
        it = pager.get_iterator()
        self.use_iterator(it)

    def use_iterator(self, it):
        """Checks the first item for a tweet id."""
        self.assertTrue(hasattr(it, '__iter__'))
        item = next(it)
        self.assertIn('id', item)


if __name__ == '__main__':
    unittest.main()
