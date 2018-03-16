import flask
import json

from donut.modules.uploads import blueprint, helpers


blueprint.route('/<path:url>')
def display(url):
    (title, page) = helpers.readPage(url)
    return render_template('page.html', page = page, title = url)
