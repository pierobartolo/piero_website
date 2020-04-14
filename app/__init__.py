from flask import Flask
from config import Config
from flask_talisman import Talisman
from flask_bootstrap import Bootstrap

app = Flask(__name__)
talisman = Talisman(app, content_security_policy=Config.csp, content_security_policy_nonce_in=['script-src-elem', 'script-src'])
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes
