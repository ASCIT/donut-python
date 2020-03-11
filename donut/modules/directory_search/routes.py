import flask
import json
import mimetypes
from flask import jsonify, redirect

from donut.auth_utils import get_user_id, is_caltech_user, login_redirect
from donut.modules.directory_search import blueprint, helpers


@blueprint.route('/directory')
def directory_search():
    if not is_caltech_user():
        return login_redirect()

    return flask.render_template(
        'directory_search.html',
        houses=helpers.get_houses(),
        options=helpers.get_options(),
        residences=helpers.get_residences(),
        grad_years=helpers.get_grad_years())


@blueprint.route('/1/users/<int:user_id>')
def view_user(user_id):
    if not is_caltech_user():
        return login_redirect()

    user = helpers.get_user(user_id)
    is_me = 'username' in flask.session and get_user_id(
        flask.session['username']) == user_id
    hidden_fields = helpers.get_hidden_fields(
        flask.session.get('username'), user_id)
    return flask.render_template(
        'view_user.html',
        user=user,
        is_me=is_me,
        user_id=user_id,
        hidden_fields=hidden_fields)


@blueprint.route('/1/users/<int:user_id>/image')
def get_image(user_id):
    if not is_caltech_user():
        flask.abort(401)

    extension, image = helpers.get_image(user_id)
    response = flask.make_response(image)
    response.headers.set('Content-Type',
                         mimetypes.guess_type('img.' + extension)[0])
    return response


@blueprint.route('/1/users/search/<name_query>')
def search_by_name(name_query):
    if not is_caltech_user():
        flask.abort(401)

    return jsonify(helpers.get_users_by_name_query(name_query))


@blueprint.route('/1/users', methods=['GET', 'POST'])
def search():
    if not is_caltech_user():
        flask.abort(401)

    if flask.request.method == 'POST':
        form = flask.request.form
        page = 1
        per_page = 10
    else:
        form = flask.request.args
        page = int(form['page'])
        total = int(form['total'])
        per_page = int(form['per_page'])
    name = form['name']
    if name.strip() == '':
        name = None
    house_id = form['house_id']
    if house_id:
        house_id = int(house_id)
    else:
        house_id = None
    option_id = form['option_id']
    if option_id:
        option_id = int(option_id)
    else:
        option_id = None
    building_id = form['building_id']
    if building_id:
        building_id = int(building_id)
    else:
        building_id = None
    grad_year = form['grad_year']
    if grad_year:
        grad_year = int(grad_year)
    else:
        grad_year = None
    offset = (page - 1) * per_page
    args = dict(
        name=name,
        house_id=house_id,
        option_id=option_id,
        building_id=building_id,
        grad_year=grad_year,
        username=form['username'],
        email=form['email'])
    if flask.request.method == 'POST':
        total = helpers.execute_search(**args)
    offset = (page - 1) * per_page
    users = helpers.execute_search(**args, offset=offset, per_page=per_page)
    if total == 1:  #1 result
        return redirect(
            flask.url_for(
                'directory_search.view_user', user_id=users[0]['user_id']))
    show_images = 'show_images' in form
    query_info = {k: ('' if v is None else v) for k, v in args.items()}
    return flask.render_template(
        'search_results.html',
        users=users,
        show_images=show_images,
        total=total,
        per_page=per_page,
        page=page,
        query_info=query_info)
