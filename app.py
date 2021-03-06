# -*- encoding: utf-8 -*-
from datetime import datetime

from esipy import App
from esipy import EsiClient
from esipy import EsiSecurity
from esipy.exceptions import APIException

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

import json
#from OpenSSL import SSL
#context = SSL.Context(SSL.SLLv23_METHOD)
#context.useprivatekey

import config
import logging
import time
from fittings import process_resp, add_to_cargo, rename_fit
from evepraisal import parse_evepraisal, find_short_item_list
from requests.exceptions import ConnectionError, MissingSchema

# logger stuff
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logger.addHandler(console)

print config.ESI_CALLBACK

# init app and load conf
app = Flask(__name__)
app.config.from_object(config)

# init db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# init flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# -----------------------------------------------------------------------
# Database models
# -----------------------------------------------------------------------
class User(db.Model, UserMixin):
    # our ID is the character ID from EVE API
    character_id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=False
    )
    character_owner_hash = db.Column(db.String(255))
    character_name = db.Column(db.String(200))

    # SSO Token stuff
    access_token = db.Column(db.String(100))
    access_token_expires = db.Column(db.DateTime())
    refresh_token = db.Column(db.String(100))

    def get_id(self):
        """ Required for flask-login """
        return self.character_id

    def get_sso_data(self):
        """ Little "helper" function to get formated data for esipy security
        """
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_in': (
                self.access_token_expires - datetime.utcnow()
            ).total_seconds()
        }

    def update_token(self, token_response):
        """ helper function to update token data from SSO response """
        self.access_token = token_response['access_token']
        self.access_token_expires = datetime.fromtimestamp(
            time.time() + token_response['expires_in'],
        )
        if 'refresh_token' in token_response:
            self.refresh_token = token_response['refresh_token']


# -----------------------------------------------------------------------
# Flask Login requirements
# -----------------------------------------------------------------------
@login_manager.user_loader
def load_user(character_id):
    """ Required user loader for Flask-Login """
    return User.query.get(character_id)


# -----------------------------------------------------------------------
# ESIPY Init
# -----------------------------------------------------------------------
# create the app
esiapp = App.create(config.ESI_SWAGGER_JSON)

# init the security object
esisecurity = EsiSecurity(
    app=esiapp,
    redirect_uri=config.ESI_CALLBACK,
    client_id=config.ESI_CLIENT_ID,
    secret_key=config.ESI_SECRET_KEY,
)

# init the client
esiclient = EsiClient(
    security=esisecurity,
    cache=None,
    headers={'User-Agent': config.ESI_USER_AGENT}
)


# -----------------------------------------------------------------------
# Login / Logout Routes
# -----------------------------------------------------------------------
@app.route('/sso/login')
def login():
    """ this redirects the user to the EVE SSO login """
    return redirect(esisecurity.get_auth_uri(
        scopes=['esi-fittings.read_fittings.v1', 'esi-fittings.write_fittings.v1']
    ))


@app.route('/sso/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/sso/callback')
def callback():
    """ This is where the user comes after he logged in SSO """
    # get the code from the login process
    code = request.args.get('code')

    # now we try to get tokens
    try:
        auth_response = esisecurity.auth(code)
    except APIException as e:
        return 'Login EVE Online SSO failed: %s' % e, 403

    # we get the character informations
    cdata = esisecurity.verify()

    # if the user is already authed, we log him out
    if current_user.is_authenticated:
        logout_user()

    # now we check in database, if the user exists
    # actually we'd have to also check with character_owner_hash, to be
    # sure the owner is still the same, but that's an example only...
    try:
        user = User.query.filter(
            User.character_id == cdata['CharacterID'],
        ).one()

    except NoResultFound:
        user = User()
        user.character_id = cdata['CharacterID']

    user.character_owner_hash = cdata['CharacterOwnerHash']
    user.character_name = cdata['CharacterName']
    user.update_token(auth_response)

    # now the user is ready, so update/create it and log the user
    try:
        db.session.merge(user)
        db.session.commit()

        login_user(user)
        session.permanent = True

    except:
        logger.exception("Cannot login the user - uid: %d" % user.character_id)
        db.session.rollback()
        logout_user()

    return redirect(url_for("index"))

@app.route('/gen_fit', methods=['POST'])
@login_required
def gen_fit():
    dict = request.get_json()
    if dict is None:
        return ('No data', 400)
    if not 'fit' in dict:
        return ('No fit', 400)
    if not 'evep_url' in dict:
        return ('No url', 400)
    if not 'cargo_size' in dict:
        return ('No size', 400)
    url = dict['evep_url']
    if not url.endswith('.json'):
        url += '.json'
    fit = dict['fit']
    try:
        size = float(dict['cargo_size'])
    except:
        out = { 'msg' : 'Invalid size "' + dict['cargo_size'] + '" supplied.'  }
        return (json.dumps(out), 400)
        
    try:
        parsed_items = parse_evepraisal(url)
    except (MissingSchema, ConnectionError):
        out = { 'msg' : 'Invalid URL "' + dict['evep_url'] + '" supplied.'  }
        return (json.dumps(out), 400)

    (optimal_items, size, val) = find_short_item_list(parsed_items, size, maxitems=255 - len(fit['items']))
    expanded_fit = add_to_cargo(fit, optimal_items)
    expanded_fit = rename_fit(fit, dict['evep_url'])
    esisecurity.update_token(current_user.get_sso_data())
    op = esiapp.op['post_characters_character_id_fittings'](
        character_id = current_user.character_id,
        fitting = expanded_fit
    )
    resp = esiclient.request(op)
    if resp.status != 201:
        print resp.status
        return render_template('error.html', **{
            'error_code': resp.status
        })

    out = {
        'msg' : '"' + expanded_fit['name'] + '" created!',
        'count' : len(optimal_items),
        'size' : size,
        'val' : val
    }
    return (json.dumps(out), 201)

# -----------------------------------------------------------------------
# Index Routes
# -----------------------------------------------------------------------
@app.route('/')
def index():
    wallet = None

    # if the user is authed, get the wallet content !
    if current_user.is_authenticated:
        # give the token data to esisecurity, it will check alone
        # if the access token need some update
        esisecurity.update_token(current_user.get_sso_data())

        op = esiapp.op['get_characters_character_id_fittings'](
            character_id=current_user.character_id
        )
        resp = esiclient.request(op)
        if resp.status != 200:
            print resp
            return render_template('error.html', **{
                'error_code': resp.status
            })
        #Should return list of ships, each ship contains name & list of resp for that ship
        fits = process_resp(esiapp, esiclient, resp)
        return render_template('info.html', **{
            'fittings': fits
            })
#        print json.dumps(resp.data, sort_keys=True, indent=4, separators=(',',': '))


    return render_template('base.html')

if __name__ == '__main__':
    app.run(port=config.PORT, host=config.HOST)
