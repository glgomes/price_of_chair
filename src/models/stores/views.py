from flask import Blueprint
from flask import json
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from src.models.stores.store import Store
import src.models.users.decorators as user_decorators

__author__ = 'glgs'

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.html', store=Store.get_by_id(store_id))


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store.name = request.form['name']
        store.url_prefix = request.form['url_prefix']
        store.tag_name = request.form['tag_name']
        store.query = json.loads(request.form['query'])

        store.update_to_db()
        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@user_decorators.requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_db()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_admin
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_db()

        return redirect(url_for('.index'))
    return render_template('stores/create_store.html')