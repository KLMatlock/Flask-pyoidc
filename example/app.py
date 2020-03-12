import datetime
import flask
import logging
from flask import Flask, jsonify

from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_pyoidc.user_session import UserSession

app = Flask(__name__)
# See http://flask.pocoo.org/docs/0.12/config/
app.config.update({
    'SECRET_KEY': 'dev_key',  # make sure to change this!!
    'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=7).total_seconds(),
    'PREFERRED_URL_SCHEME': 'https',
    'DEBUG': True})

ISSUER1 = 'http://192.168.1.3:8890/auth/realms/mypatient'
CLIENT1 = 'flask'
PROVIDER_NAME1 = 'provider1'
PROVIDER_CONFIG1 = ProviderConfiguration(issuer=ISSUER1,
                                         client_metadata=ClientMetadata(CLIENT1, '34e4a94c-a4ce-480e-a5b5-a7b2b56e3199'))

auth = OIDCAuthentication({PROVIDER_NAME1: PROVIDER_CONFIG1}, app=app)

@app.route('/')
@auth.oidc_auth(PROVIDER_NAME1)
def login1():
    user_session = UserSession(flask.session)
    return jsonify(access_token=user_session.access_token,
                   id_token=user_session.id_token,
                   userinfo=user_session.userinfo)



@app.route('/logout')
@auth.oidc_logout
def logout():
    return "You've been successfully logged out!"


@auth.error_view
def error(error=None, error_description=None):
    return jsonify({'error': error, 'message': error_description})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    auth.init_app(app)
    app.run(host='0.0.0.0')
