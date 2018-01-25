from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app
from models import db, Users


# create our blueprint :)
bp = Blueprint('jingway', __name__)


@bp.route('/')
def show_users():
    users = Users.query.order_by(Users.id).all()
    return render_template('show_users.html', users=users)


@bp.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    user = Users(
        username = request.form['username'],
        role = request.form['role'],
        password = request.form['password']
        )
    db.session.add(user)
    db.session.commit()
    flash('您已成功新建用户。')
    return redirect(url_for('jingway.show_users'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['admin'] != current_app.config['USERNAME']:
            error = '对不起，不存在该管理员。'
        elif request.form['passwd'] != current_app.config['PASSWORD']:
            error = '对不起，您的密码错误。'
        else:
            session['logged_in'] = True
            flash('恭喜！您已登陆。')
            return redirect(url_for('jingway.show_users'))
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('您已成功登出。')
    return redirect(url_for('jingway.show_users'))
