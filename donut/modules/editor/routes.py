import flask
import json
import os
import re
from donut.modules.editor import blueprint, helpers


@blueprint.route('/editor', methods=['GET', 'POST'])
def editor():
    '''
    Returns the editor page where users can create and edit
    existing pages
    '''
    input_text = "Hello world"
    title = "TITLE"
    inputt = flask.request.args.get('title')
    if inputt != None:
        input_text = helpers.read_markdown(inputt)
        title = flask.request.args.get('title')
        load_default = False
    if inputt == None:
        load_default = True
    if not helpers.is_locked(
            title, load_default) and helpers.check_edit_page_permission():
        helpers.change_lock_status(title, True, load_default)
        return flask.render_template(
            'editor_page.html', input_text=input_text, title=title)
    else:
        return flask.abort(403)


@blueprint.route('/pages/_close_page', methods=['POST'])
def close_page():
    """
    Call to change the status of the locks when one exits a page
    """
    title = flask.request.form['title']
    helpers.change_lock_status(title, False)
    return ""


@blueprint.route('/pages/_keep_alive_page', methods=['POST'])
def keep_alive_page():
    """
    Call to update the last access time for a page
    """
    title = flask.request.form['title']
    if helpers.check_edit_page_permission():
        helpers.change_lock_status(title, True)
    return ""


@blueprint.route('/pages/_change_title', methods=['POST'])
def change_title():
    '''
    Allows one to change a file/page title.
    '''
    title = flask.request.form['title']
    old_title = flask.request.form['old_title']
    input_text = flask.request.form['input_text']
    if helpers.check_title(title) and helpers.check_edit_page_permission():
        helpers.rename_title(old_title, title)
        return flask.render_template('editor_page.html', input_text=input_text)
    return flask.abort(403)


@blueprint.route('/pages/_save', methods=['POST'])
def save():
    '''
    Actually saves the data from the forms as markdown
    '''
    markdown = flask.request.form['markdown']
    title = flask.request.form['title']
    markdown = markdown.replace('<', '&lt;')
    markdown = markdown.replace('>', '&gt;')
    if helpers.check_edit_page_permission():
        helpers.write_markdown(markdown, title)
        return flask.jsonify({
            'url': flask.url_for('uploads.display', url=title)
        })
    else:
        flask.abort(403)


@blueprint.route('/pages/_check_errors', methods=['POST'])
def check_errors():
    """
    Checks for any errors with the title
    """
    title = flask.request.form['title']
    if helpers.check_duplicate(title):
        return flask.jsonify({'error': "Duplicate title"})
    if not helpers.check_title(title):
        return flask.jsonify({'error': "Invalid Title"})
    return flask.jsonify({'error': ""})


@blueprint.route('/pages/_delete')
def delete_page():
    """
    End point for page deletion
    """
    filename = flask.request.args.get('filename')
    if filename != None and helpers.check_edit_page_permission():
        helpers.remove_link(filename)

    return flask.redirect(flask.url_for('editor.created_list'))


@blueprint.route('/pages/list_of_pages')
def created_list():
    '''
    Returns a list of all created pages
    '''

    links = helpers.get_links()
    return flask.render_template(
        'created_list.html',
        links=links,
        permissions=helpers.check_edit_page_permission())
