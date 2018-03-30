
from flask import render_template, request, flash,redirect, url_for,session

from src.app import app
from src.models.users.user import User
from src.models.otp.otp import OTP
from src.common.Utility.utils import Utils


@app.route('/', methods=['POST', 'GET'])
def home():
    otp_status = False
    if request.method == 'POST':
        aadhaar_number = request.form['aadhaar_no']
        user = User.get_by_aadhaar(aadhaar_number)
        mobile_no = user.mobile_no
        otp = OTP(user._id)
        if Utils.send_otp(otp.otp,mobile_no):
            otp.save_to_db()
            flash('One time password has been successfully Sent To Your Device', 'success')
            otp_status = True
        else:
            flash('There is some error', 'error')

        return render_template('home.html', otp_id=otp._id, otp_status=otp_status)
    return render_template('home.html')


@app.route('/authenticate-user/<otp_id>',methods= ["POST", "GET"])
def authenticate_user(otp_id):
    if request.method == "POST":
        user_otp = request.form['otp']
        otp_sent = OTP.get_recent_otp(otp_id)
        user = User.get_by_id(otp_sent.user_id)
        if int(user_otp)==int(otp_sent.otp):
            session['uid'] = user._id
            return redirect(url_for('.redirect_to_dash'))
        else:
            raise ValueError("Incorrect OTP")

@app.route('/to-dash/redirecting')
def redirect_to_dash():
    if 'uid' in session.keys() and session['uid']==None:
        return redirect(url_for('.home'))
    else:
        user_id = session['uid']
        return redirect(url_for('users.view_dashboard', user_id = user_id ))

@app.route('/logout')
def logout():
    session['uid']=None
    return redirect(url_for('.home'))



