from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'narskinz'
app.config['MYSQL_PASSWORD'] = 'Bobbym123!'
app.config['MYSQL_DB'] = 'food_ordering_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Retrieve form data
        food_item = request.form['food_item']
        quantity = request.form['quantity']

        # Store data in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO orders (food_item, quantity) VALUES (%s, %s)", (food_item, quantity))
        mysql.connection.commit()
        cur.close()

        return redirect('/orders')

    return render_template('order.html')

@app.route('/orders')
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()

    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
