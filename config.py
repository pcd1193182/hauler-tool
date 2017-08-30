# -*- encoding: utf-8 -*-
import datetime
import os

# -----------------------------------------------------
# Application configurations
# ------------------------------------------------------
DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
PORT = int(os.environ['APP_PORT'])
HOST = os.environ['APP_HOST']

# -----------------------------------------------------
# SQL Alchemy configs
# -----------------------------------------------------
SQLALCHEMY_DATABASE_URI =  os.environ['DATABASE_URL']

# -----------------------------------------------------
# ESI Configs
# -----------------------------------------------------
ESI_DATASOURCE = 'tranquility'  # Change it to 'singularity' to use the test server
ESI_SWAGGER_JSON = 'https://esi.tech.ccp.is/latest/swagger.json?datasource=%s' % ESI_DATASOURCE
ESI_SECRET_KEY = os.environ['ESI_SECRET_KEY']  # your secret key
ESI_CLIENT_ID = os.environ['ESI_CLIENT_ID']  # your client ID
ESI_CALLBACK = 'https://%s/sso/callback' % (HOST)  # the callback URI you gave CCP
ESI_USER_AGENT = 'hauler-packing-tool'


# ------------------------------------------------------
# Session settings for flask login
# ------------------------------------------------------
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

# ------------------------------------------------------
# DO NOT EDIT
# Fix warnings from flask-sqlalchemy / others
# ------------------------------------------------------
SQLALCHEMY_TRACK_MODIFICATIONS = True
