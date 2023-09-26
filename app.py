from myproyect import app, db, google
from flask_login import login_required, logout_user, login_user
from flask import render_template, url_for, redirect, request, flash
from myproyect.forms import LoginForm, RegisterForm, LoginGoogleForm
from myproyect.models import Users

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    google_form = LoginGoogleForm()
    next = request.args.get('next')
    if not next or next[0] != '/':
        next = url_for('welcome')
    if google_form.validate_on_submit():
        if not google.authorized:
            return render_template(url_for('google.login'))
        resp = google.get('/oauth2/v2/userinfo')
        assert resp.ok and resp.text
        user = Users.query.filter_by(email=resp.json()['email']).first()
        if not user:
            flash("Couldn't find your account. There's no account for that email. Try logging in with a different email.")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(next)
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(next)
    for e in form.errors.values():
        flash(e[0])
    return render_template('login.html', form=form, google_form=google_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    for e in form.errors.values():
        flash(e[0])
    return render_template('register.html', form=form)

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
