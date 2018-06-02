import flask
import json
import os

import glob
from donut.modules.editor import blueprint, helpers
from flask import current_app, redirect, url_for


@blueprint.route('/editor', methods=['GET', 'POST'])
def editor(input_text='Hello World!!!', title="TITLE"):
    input = flask.request.args.get('input_text')
    print(input)
    if input != None:
        input_text = helpers.read_markdown(input)
        title = flask.request.args.get('title')
    return flask.render_template(
        'editor_page.html', input_text=input_text, title=title)


@blueprint.route('/redirecting')
def redirecting(title='uploads.aaa'):
    return flask.render_template('redirecting.html', input_text=url_for(title))


@blueprint.route('/_save', methods=['POST'])
def save():
    markdown = flask.request.form['markdown']
    title = flask.request.form['title']
    if title == 'BoC':
        return flask.jsonify({'url': url_for('committee_sites.boc')})
    elif title == 'ASCIT_Bylaws':
        return flask.jsonify({'url': url_for('committee_sites.ascit_bylaws')})
    elif title == 'BoC_Bylaws':
        return flask.jsonify({'url': url_for('committee_sites.bylaws')})
    elif title == 'BoC_Defendants' :
        return flask.jsonify({'url': url_for('committee_sites.defendants')})
    elif title ==  'BoC_FAQ' :
        return flask.jsonify({'url': url_for('committee_sites.FAQ')})
    elif title == 'BoC_Reporters' :
        return flask.jsonify({'url': url_for('committee_sites.reporters')})
    elif title == 'BoC_Witness' :
        return flask.jsonify({'url': url_for('committee_sites.winesses')})
    elif title == 'CRC':
        return flask.jsonify({'url': url_for('committee_sites.CRC')})
    if (helpers.write_markdown(markdown, title) == 0):
        return flask.jsonify({'url': url_for('uploads.display', url=title)})
    else:
        return flask.jsonify({'url': url_for('uploads.display', url=title)})


@blueprint.route('/created_list')
def created_list():
    filename = flask.request.form['filename']
    if filename != None:
        helper.remove_link(filename)

    links = helpers.get_links()
    return flask.render_template('created_list.html', links=links)
