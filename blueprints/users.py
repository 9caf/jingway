from sqlite3 import dbapi2 as sqlite3
from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app


# create our blueprint :)
bp = Blueprint('jingway', __name__)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(current_app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@bp.route('/')
def show_users():
    db = get_db()
    cur = db.execute('select username, role, password from users order by id desc')
    users = cur.fetchall()
    return render_template('show_users.html', users=users)


@bp.route('/add', methods=['POST'])
def add_user():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into users (username, role, password) values (?, ?, ?)',
               [request.form['username'], request.form['role'], request.form['password']])
    db.commit()
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
