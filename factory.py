from flask import Flask, g
from werkzeug.utils import find_modules, import_string
from blueprints.users import bp

def create_app(config=None):
    app = Flask('jingway')

    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='12345678',
        USERNAME='admin',
        PASSWORD='admin'
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    import sys
    sys.path.append(app.root_path) 
    from models import db

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///var/services/homes/jingwei/jingway/jingway.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    register_blueprints(app)
    register_cli(app)
    register_teardowns(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def register_cli(app):
    @app.cli.command('initdb')
    def initdb_command():
        """Creates the database tables."""
        db.create_all(app=create_app())
        print('Initialized the database.')


def register_teardowns(app):
    @app.teardown_appcontext
    def close_db(error):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8509)