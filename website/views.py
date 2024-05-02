from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . models import Post
from . import db
from . models import Menu, MenuItem, Day, Hostel


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/timetable")
@login_required
def view_timetable():
    return render_template('timetable.html', user=current_user)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)


@views.route('/selection', methods=['GET', 'POST'])
@login_required
def select_hostel_day():
    if request.method == 'POST':
        hostel = request.form.get('hostel')
        day = request.form.get('day')

        return redirect(url_for('views.display_mess_menu', hostel=hostel, day=day))

    hostels = Hostel.query.all()  # Query all hostels from the database
    days = Day.query.all()  # Query all days from the database

    return render_template('selection.html', user=current_user, hostels=hostels, days=days)


@views.route('/displaymessmenu', methods=['GET', 'POST'])
@login_required
def display_mess_menu():
    hostel_name = request.form.get('hostel')
    day_name = request.form.get('day')
    meal = request.form.get('meal')

    hostel = Hostel.query.filter_by(name=hostel_name).first()
    day = Day.query.filter_by(name=day_name).first()

    print("Hostel name:", hostel_name)
    print("Day name:", day_name)

    if not hostel or not day:
        return render_template('error.html', message='Invalid hostel or day', user=current_user)

    menu = Menu.query.filter_by(hostel_id=hostel.id, day_id=day.id).first()

    if not menu:
        return render_template('error.html', message='Menu not found for selected hostel and day', user=current_user)

    menu_items = MenuItem.query.filter_by(menu_id=menu.id, meal=meal).all()

    if not menu_items:
        return render_template('error.html', message='Menu items not found for selected meal', user=current_user)

    return render_template('display_mess_menu.html', hostel=hostel_name, day=day_name, meal=meal, menu_items=menu_items, user=current_user)


@views.route('/add_menu_item', methods=['GET', 'POST'])
@login_required
def add_menu_item():
    # Retrieve hostel and day from the request parameters

    hostel_name = request.form.get('hostel')
    day_name = request.form.get('day')
    meal = request.form.get('meal')

    # Query the database to find the corresponding Hostel and Day objects
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    day = Day.query.filter_by(name=day_name).first()

    # Check if the Hostel and Day exist
    if hostel and day:
        # Query the database to find the Menu object based on the Hostel and Day
        menu = Menu.query.filter_by(hostel_id=hostel.id, day_id=day.id).first()

        # Check if the Menu object exists
        if menu:
            # Create a new MenuItem associated with the found Menu
            meal = request.form.get('meal')
            name = request.form.get('name')
            category = request.form.get('category')

            # Create the new MenuItem
            new_menu_item = MenuItem(
                menu=menu, meal=meal, name=name, category=category)

            # Add the new MenuItem to the database session and commit the transaction
            db.session.add(new_menu_item)
            db.session.commit()

            flash('Menu item added successfully!', category='success')
        else:
            flash('Menu not found for the selected hostel and day.', category='error')
    else:
        flash('Invalid hostel or day.', category='error')

    hostel = Hostel.query.filter_by(name=hostel_name).first()
    day = Day.query.filter_by(name=day_name).first()
    menu = Menu.query.filter_by(hostel_id=hostel.id, day_id=day.id).first()
    menu_items = MenuItem.query.filter_by(menu_id=menu.id, meal=meal).all()

    return render_template('display_mess_menu.html', hostel=hostel_name, day=day_name, meal=meal, menu_items=menu_items, user=current_user)


@views.route('/delete_menu_item', methods=['POST'])
@login_required
def delete_menu_item():
    item_id = request.form.get('item_id')
    hostel_name = request.form.get('hostel')
    day_name = request.form.get('day')
    meal = request.form.get('meal')

    # Check if the hostel and day values are received correctly
    print("Hostel name:", hostel_name)
    print("Day name:", day_name)
    item_to_delete = MenuItem.query.get(item_id)
    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('Item deleted from the menu!', category='success')

    else:
        flash('Item not found or you do not have permission to delete it.',
              category='error')

    hostel = Hostel.query.filter_by(name=hostel_name).first()
    day = Day.query.filter_by(name=day_name).first()
    menu = Menu.query.filter_by(hostel_id=hostel.id, day_id=day.id).first()
    menu_items = MenuItem.query.filter_by(menu_id=menu.id, meal=meal).all()

    return render_template('display_mess_menu.html', hostel=hostel_name, day=day_name, meal=meal, menu_items=menu_items, user=current_user)
