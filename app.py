from flask import Flask


app = Flask(__name__)

# 1. points analysis
from views.points import points
app.register_blueprint(points, url_prefix='/v1/points')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
