from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as user_decorators

__author__ = 'glgs'


alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == 'POST':
        alert.price_limit = float(request.form['price_limit'])
        alert.update_to_db()

        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_db()

        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()

    return render_template('alerts/create_alert.html')


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def remove_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.item.remove_from_db()
    alert.remove_from_db()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html', alert=alert)


@alert_blueprint.route('/check_alert_price/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert._id))