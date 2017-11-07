import flask

from donut.tests.fixtures import client
from donut import app

def testHome(client):
  rv = client.get(flask.url_for('scheduler.home'))

  assert rv.status_code == 200
  assert "Example page" in rv.data
