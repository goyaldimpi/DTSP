import requests
from flask import render_template, request, redirect, url_for, session
from flask.blueprints import Blueprint
from src.models.retailers.retailer import Retailer
from src.models.users.user import User

retailers_blueprint = Blueprint('retailer', __name__)


@retailers_blueprint.route('/dashboard/<user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    retailer = Retailer.get_by_id(user_id)
    return render_template('Dashboard.html', retailer=retailer)


@retailers_blueprint.route('/user_verify', methods=['GET', 'POST'])
def user_verify():
    if request.method == 'POST':
        aadhaar = request.form['aadhaar']
        if Retailer.is_authenticated(aadhaar):
            user = Retailer.get_user_by_adhaar(aadhaar)
            return redirect(url_for('.user_details', user_id=user._id))
        else:
            return render_template('user-verify.html')
    else:
        return render_template('user-verify.html')


@retailers_blueprint.route('/user_details/<user_id>', methods=['GET', 'POST'])
def user_details(user_id):
    user = User.get_by_id(user_id)
    data = requests.post("https://beast-cdb.herokuapp.com/api/tsp/sim",data={'aadhaar_no':user.aadhaar_no, 'tsp':'Airtel'}).json()
    sims = data['data']['sim']
    sim_count = data['data']['sim_by_other_tsp']
    keys = sim_count.keys()
    return render_template('user_details.html', user=user, sims=sims, sim_count =sim_count, keys = keys)


@retailers_blueprint.route('/register/<user_id>', methods=['GET', 'POST'])
def register(aadhaar):
    user = User.get_by_aadhaar(aadhaar)
    return render_template('Register.html', user=user)


@staticmethod
def logout():
  session['username'] = None
