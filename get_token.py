import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from utils.config import Config as cfg

# Replace these with your client ID and client secret
CLIENT_ID=cfg.GOOGLE_CLIENT_ID
CLIENT_SECRET=cfg.GOOGLE_CLIENT_SECRET
REDIRECT_URI = 'http://localhost:8080/'  # Make sure this matches the one in Google Cloud Console

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if 'code' in query_components:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Authorization code received. You can close this window.")
            
            authorization_code = query_components['code'][0]
            data = {
                'code': authorization_code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            response = requests.post('https://oauth2.googleapis.com/token', data=data)
            print(response.json())
            self.server.auth_code_received = True

def get_auth_code():
    auth_url = (
        'https://accounts.google.com/o/oauth2/auth'
        '?response_type=code'
        '&client_id={client_id}'
        '&redirect_uri={redirect_uri}'
        '&scope={scope}'
        '&access_type=offline'
        '&prompt=consent'
    ).format(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope='https://mail.google.com/'
    )
    webbrowser.open(auth_url)

def main():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, OAuthHandler)
    print('Starting server at http://localhost:8080/')
    
    get_auth_code()
    
    while not hasattr(httpd, 'auth_code_received') or not httpd.auth_code_received:
        httpd.handle_request()

if __name__ == '__main__':
    main()