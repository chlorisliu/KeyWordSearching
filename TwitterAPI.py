import time
import pycurl
import urllib.parse
import json
import oauth2 as oauth

API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
USER_AGENT = 'TwitterStream 1.0'  # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {
    'consumer_key': "ZALFDuQvGz68wgtomKq0vGY5M",
'consumer_secret':"srNGGiCFxpmU1ui7TryguIJqSpQWGl3QZpRaTxj1sIv2ddZ6DQ",
'access_token' :"1534150777593536512-u6Ie5E531PsiEDc9LHsUBcGX4VcYOu",
'access_token_secret' : "4Dm58ZukdVFTS03nddVWHpnoVM2abx1suViN9WrD1uwCL"}

# These values are posted when setting up the connection
POST_PARAMS = {
    'include_entities': 0,
    'stall_warning': 'true',
    'track': 'iphone,ipad,ipod'
}


class TwitterStream:
    def __init__(self, timeout=False):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        """ Create a persistent HTTP connection to the Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.parse.urlencode(POST_PARAMS).encode('utf-8'))
        self.conn.setopt(pycurl.HTTPHEADER, [
            'Host: stream.twitter.com',
            'Authorization: %s' % self.get_oauth_header().decode('utf-8')
        ])
        # self.handle_tweet is the method that is called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

    def get_oauth_header(self):
        """ Create and return the OAuth header.
        """
        params = {
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time())
        }
        req = oauth.Request(method='POST', parameters=params,
                            url='%s?%s' % (API_ENDPOINT_URL, urllib.parse.urlencode(POST_PARAMS)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to the Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except Exception as e:
                # Network error, use linear back off up to 16 seconds
                print('Network error:', str(e))
                print('Waiting', backoff_network_error, 'seconds before trying again')
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print("Rate limit, waiting", backoff_rate_limit, "seconds")
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print('HTTP error', sc, self.conn.errstr())
                print('Waiting', backoff_http_error, 'seconds')
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)

    def handle_tweet(self, data):
        """ This method is called when data is received through the Streaming endpoint.
        """
        self.buffer += data.decode('utf-8')
        if data.endswith(b'\r\n') and self.buffer.strip():
            # Complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            msg = ''
            if message.get('limit'):
                print('Rate limiting caused us to miss', message['limit'].get('track'), 'tweets')
            elif message.get('disconnect'):
                raise Exception('Got disconnect:', message['disconnect'].get('reason'))
            elif message.get('warning'):
                print('Got warning:', message['warning'].get('message'))
            else:
                print('Got tweet with text:', message.get('text'))


if __name__ == '__main__':
    ts = TwitterStream()
    ts.setup_connection()
    ts.start()