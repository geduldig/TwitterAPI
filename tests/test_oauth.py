from TwitterAPI import TwitterAPI, TwitterOAuth
import unittest


class OAuthTest(unittest.TestCase):

    """Test user and application authentication."""

    def setUp(self):
        """Read credentials from TwitterAPI/credentials.txt. You
        must copy your credentials into this text file.
        """
        self.oa = TwitterOAuth.read_file()

    def test_oauth_1(self):
        """Test user authentication."""
        api = TwitterAPI(self.oa.consumer_key, self.oa.consumer_secret,
                         self.oa.access_token_key, self.oa.access_token_secret)
        status_code = self.verify_credentials(api)
        # 200 means success
        self.assertEqual(status_code, 200)

    def test_oauth_2(self):
        """Test application authentication."""
        api = TwitterAPI(self.oa.consumer_key, self.oa.consumer_secret,
                         auth_type='oAuth2')
        status_code = self.verify_credentials(api)
        # 403 means no access, which is correct since no user credentials
        # provided
        self.assertEqual(status_code, 403)

    def verify_credentials(self, api):
        r = api.request('account/verify_credentials')
        return r.status_code


if __name__ == '__main__':
    unittest.main()
