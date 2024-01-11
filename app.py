from flask import Flask,render_template,request,redirect, url_for,session,jsonify
import sqlite3
import base64
app=Flask(__name__)
app.secret_key = 'cupcake'


@app.route("/")

def index():
    username = request.args.get('username', '')  # Retrieve the username from the URL parameters
    conn=sqlite3.connect('capcake.db')
    cursor = conn.execute("SELECT * FROM CAKE")
    products = cursor.fetchall()  # Fetch all products from the database
    return render_template('index.html',products=products, username=username,convert_to_stars=convert_to_stars,cart=session.get('cart', []))

def convert_to_stars(rate):
    if rate is not None:
        rounded_rate = round(rate)  # Round the rate to the nearest integer
        stars = '★' * rounded_rate + '☆' * (5 - rounded_rate)
        return stars
    return ''


@app.route('/register',methods=['POST','GET'])
def register():
    # register=registerForm()
    con=sqlite3.connect('capcake.db')
    c=con.cursor()
    if request.method=='POST':
        if(request.form['name']!="" and request.form['email']!="" and request.form['password']!=""):
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            mobile=request.form['mobile']
            statement=f"select * from user where name='{name}' and password='{password}';"
            c.execute(statement)
            data=c.fetchone()
            if data:
                return render_template('error.html')
            else:
                if not data:
                    c.execute("INSERT INTO USER(name,email, password,mobile_number) values(?,?,?,?)",(name, email, password,mobile))
                    con.commit()
                    con.close()
                    return render_template('login.html')


    elif request.method=='GET':
        return render_template('register.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Retrieve user input from the form
        name = request.form.get('name')
        password = request.form.get('password')

        # Perform login logic by checking the database
        con = sqlite3.connect('capcake.db')
        c = con.cursor()

        # Example: Query the database for a user with the given username and password
        c.execute("SELECT * FROM USER WHERE name=? AND password=?", (name, password))
        user = c.fetchone()

        con.close()

        if user:
            # If the user exists, redirect to the index page with the username as a parameter
            return redirect(url_for('index', username=name))
        else:
            # If the user doesn't exist or the password is incorrect, render an error message
            return render_template('error.html')

    # If the request method is GET or the login failed, render the login page
    return render_template('login.html')


@app.route("/add_product", methods=["GET", "POST"])  # Accept both GET and POST methods
def add_product():
    conn=sqlite3.connect('capcake.db')
    if request.method == "POST":  # Handle form submission if request method is POST
        name = request.form["name"]
        price = int(request.form["price"])
        image = request.files["image"].read()  # Assuming image is a file input
        image_data = base64.b64encode(image).decode("utf-8")  # Encode the bytes directly
    
        try:
            # Execute the INSERT statement with placeholders for security
            rate = float(request.form.get("rate", 0))  # Get the rate value, default to 0
            conn.execute(
                "INSERT INTO CAKE (NAME, PRICE, rate, image) VALUES (?, ?, ?, ?)",
                (name, price, rate, image_data),
            )
            conn.commit()
            return redirect(url_for("index"))  # Redirect to home page after success
        except sqlite3.Error as e:
            print("Error adding product:", e)
            return "Error adding product", 500  # Return error message and status code
    else:  # Render the template if request method is GET
        return render_template('add_product.html')

# this code to add product to cart
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    try:
        conn = sqlite3.connect('capcake.db')
        cursor = conn.cursor()
        print(f"id: {product_id}")
        # Get product information (including price)
        cursor.execute("SELECT * FROM CAKE WHERE Id = ?", (product_id,))
        product_info = cursor.fetchone()

        # Check for existing items with the same product_id
        cursor.execute("SELECT * FROM cart WHERE product_id = ?", (product_id,))
        existing_cart_item = cursor.fetchone()

        if existing_cart_item:
            # Update quantity for existing item
            cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE product_id = ?", (product_id,))
            # Recalculate total price for the item
            cursor.execute("UPDATE cart SET total_price = ? * quantity WHERE product_id = ?", (product_info[2], product_id))  # Assuming price is in column 2
        else:
            # Insert new item with quantity 1 and total price
            cursor.execute("INSERT INTO cart (product_id, quantity, total_price) VALUES (?, 1, ?)", (product_id, product_info[2]))

        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except sqlite3.Error as e:
        print("Error adding to cart:", e)
        return jsonify({'success': False, 'error': str(e)})





# get cart count
@app.route('/get_cart_count')
def get_cart_count():
    count = get_cart_item_count()  # Function to count cart items from database
    return jsonify({'count': count})

def get_cart_item_count():
    try:
        conn = sqlite3.connect('capcake.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cart")
        count = cursor.fetchone()[0]  # Retrieve the first column (count)
        print(count)
        conn.close()
        return count

    except sqlite3.Error as e:
        print("Error retrieving cart count:", e)
        return 0  # Or return a suitable error message

@app.route('/view_cart')
def view_cart():
    # Fetch cart contents and payment information
    # cart = session.get('cart', [])
    conn = sqlite3.connect('capcake.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart")
    cart = cursor.fetchall()
    total_price = sum(item[3] for item in cart)
    print("Cart:", cart)
    print("Total Price:", total_price)

    payment_info = "Your payment information goes here."
    return render_template('view_cart.html', cart=cart, total_price=total_price, payment_info=payment_info)

# to get payment details
@app.route('/get_cart_details')
def get_cart_details():
    cart = session.get('cart', [])

    # Render the cart details template and return the HTML
    cart_details_html = render_template('cart_details.html', cart=cart)
    return jsonify({'cart_details_html': cart_details_html})


@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    # Handle payment form submission logic here
    # Retrieve data from the form using request.form
    # Perform any necessary validation and processing

    # For simplicity, let's just return a success message
    return jsonify({'message': 'Payment submitted successfully'})

if __name__=='__main__':
    app.run(debug=True)
