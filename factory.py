from flask import Flask, g
from werkzeug.utils import find_modules, import_string
from blueprints.users import bp


def create_app(config=None):
    app = Flask('jingway')
    app.config.from_pyfile('config.cfg')
    register_db(app)
    register_blueprints(app)
#    login_manager = LoginManager()
    return app


def register_db(app):
    import sys
    sys.path.append(app.root_path)
    from models import db
    db.init_app(app)


def init_db():
    app = Flask('jingway')
    app.config.from_pyfile('config.cfg')

    import sys
    sys.path.append(app.root_path)
    from models import db
    db.init_app(app)

    db.create_all(app=app)
    print('数据库创建成功！')



def register_blueprints(app):
    """蓝图注册"""
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8509)
