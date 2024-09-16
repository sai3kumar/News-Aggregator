from flask import Flask,render_template
from routes import filter_routes, category_routes, date_routes, headline_routes

app = Flask(__name__,static_folder='static')

# Register routes
app.register_blueprint(filter_routes.bp)
app.register_blueprint(category_routes.bp)
app.register_blueprint(date_routes.bp)
app.register_blueprint(headline_routes.bp)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

