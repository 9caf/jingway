from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
	return 'Hello, 刘经纬.'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8509, debug=True)