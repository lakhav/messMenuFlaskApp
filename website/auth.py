from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User ,Year,Department,Subgroup
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Password!", category='error')
        else:
            flash("email does not exist!", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        year_id = request.form['year']  # Assuming you have a form field for selecting year_id
        department_id = request.form['department']  # Assuming you have a form field for selecting department_id
        subgroup_id = request.form['subgroup']  # Assuming you have a form field for selecting subgroup_id

        # Fetch instances of Year, Department, and Subgroup based on the selected IDs
        year = Year.query.get(year_id)
        department = Department.query.get(department_id)
        subgroup = Subgroup.query.get(subgroup_id)
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists!', category='error')
            return redirect(url_for('auth.sign_up'))

        # Validate form inputs
        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('password must be greater than 7 characters.', category='error')
        else:
            # add user to database
            new_user = User(email=email,
                            first_name=firstName,
                            password=generate_password_hash(
                                password1, method='pbkdf2:sha256', salt_length=8),
                            year=year,
                            department=department,
                            subgroup=subgroup
                            )

            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email=email).first()

            if user:
                login_user(user, remember=True)
                flash('Account Created Successfully', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Failed to create account. Please try again.',
                      category='error')

    years = Year.query.all()
    departments = Department.query.all()
    subgroups = Subgroup.query.all()

    print("Years:", years)
    print("Departments:", departments)
    print("Subgroups:", subgroups)

    return render_template("signup.html", user=current_user, years=years, departments=departments, subgroups=subgroups)
