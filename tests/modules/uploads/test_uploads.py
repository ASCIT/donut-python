"""
Tests donut/modules/editor/
"""
from datetime import date
import flask
import pytest
from donut.testing.fixtures import client
from donut import app
import donut.modules.core.helpers as core_helpers
from donut.modules.uploads import helpers
from donut.modules.uploads import routes
from donut.modules.editor import helpers as editor_helpers
import os


def test_routes(client):
    assert client.get(flask.url_for('uploads.uploads')).status_code == 200
    assert client.get(
        flask.url_for('uploads.uploaded_list')).status_code == 200


def test_get_links(client):
   
    helpers.remove_link("SOME_TITLE")
    links = helpers.get_links()
    titles= []
    for (discard, title) in links:
        titles.append(title)
    assert "SOME_TITLE" not in ''.join(titles)

    root = os.path.join(flask.current_app.root_path,
                        flask.current_app.config["UPLOAD_FOLDER"])
    path = os.path.join(root, "SOME_TITLE"+ ".jpg")

    f = open(path, "w+")
    f.write("")
    f.close()
    links = helpers.get_links()
    titles= []
    for (discard, title) in links:
        titles.append(title)
    assert "SOME_TITLE" in ''.join(titles)

    editor_helpers.write_markdown("BLEH", "ANOTHER_TITLE")
    assert "BLEH" == helpers.readPage("ANOTHER_TITLE")

    helpers.remove_link("SOME_TITLE")
    links = helpers.get_links()
    titles= []
    for (discard, title) in links:
        titles.append(title)
    assert "SOME_TITLE" not in ''.join(titles)


def test_allowed_file(client):
    assert helpers.allowed_file("bleh.bleh") == False
    assert helpers.allowed_file("bleh.JPg") == True
    assert helpers.allowed_file("bleh.GiF") == True
    assert helpers.allowed_file("bleh.PDF") == True
