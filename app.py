# Name: Abdulmoez Akbar(20258267), Ovil Miranda(20284057), Ava Salas(20280689)
# Group number: 3
# This is the main running file for the app. To run it, Python Flask needs to be installed. Once done, you can type
# "Python app.py" on the terminal to open the website.
'''
Instructions on how to run the program: 
	Requirements: HTML, CSS, Python, Flask, MySQL 
	In the files that are already sent, there is a database given but you have to make your own MySQL connection/server in order to connect the database. In the app.py program, you must change your host, user, password, and database name to what you setup the connection to be (This can be found near the very top of the program).  

'''
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# MySQL database connection setup
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="12345678",
    database="delivery"
)
 
cursor = db.cursor()
    

class User:
    '''
    An object that represents the typical customer for the application
    '''
   
    def __init__(self, UserID, email, password, name, address):
        """
        Constructs all the necessary attributes for the user object.

        Parameters
        ----------
            UserID : int 
                Customer's unique identifier
            email : string
                Customer's email address for account 
            password : string
                Customer's password for account
            name : string 
                Customer's name
            address : string 
                Customer's address to deliver order
            paymentDetails : dictionary
                Customer's payment details for orders
            cart : array 
                Customer's shopping cart
        """
        
        self.UserID = UserID
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.paymentDetails = {} 
        self.cart = []

    @app.route('/register_page', methods=['GET', 'POST'])
    def register():
        '''
            Registers a new user account.
            Renders the registration page for the application. 
            Once user is registered, it redirects user to the user homepage.
        '''

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            address = request.form.get('address')
            card_number = request.form.get('card_number')
            expiration_date = request.form.get('expiration_date')
            cvv = request.form.get('cvv')

            try:
                cursor.execute("INSERT INTO user (email, name, address, card_number, expiration_date, cvv, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",(email, name, address, card_number, expiration_date, cvv, password))
                db.commit()  # Commit the changes to the database
                return redirect(url_for('user_homepage'))
            except mysql.connector.Error as err:
                db.rollback()
                return f"Database connection error: {err}"
            
        return render_template('register_page.html')

    @app.route('/', methods=['GET', 'POST'])
    def login():
        '''
            Allows users to log into their accounts. 
            Renders the login page for the application. 
            Once user is logged in, it redirects user to the frontpage 
        '''
    
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if request.form.get('businessPortal'):
                
                cursor.execute("SELECT * FROM restaurant_owner WHERE email = %s AND password = %s", (email, password))
                restaurant_owner = cursor.fetchone()

                if restaurant_owner:
                    # If checked, redirect to the restaurant owner page
                    return redirect(url_for('restaurant_owner_pov', restaurantowner_id=restaurant_owner[0]))
                else:
                    # User doesn't exist or invalid credentials, show an error message
                    error_message = "Invalid email or password"
                    return render_template('front_page.html', error_message=error_message)

            else:
                # Query the database to check if the user exists
                cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()

                if user:
                    # Redirect to the user homepage or any other page
                    return redirect(url_for('user_homepage'))
                else:
                    # User doesn't exist or invalid credentials, show an error message
                    error_message = "Invalid email or password"
                    return render_template('front_page.html', error_message=error_message)


        return render_template('front_page.html')
    
    @app.route('/user_homepage')
    def user_homepage(): 
        '''
        Renders and displays the user homepage. 
        '''
        cursor = db.cursor(dictionary=True)
        # Execute a query to fetch restaurant data
        cursor.execute("SELECT * FROM restaurant")

        # Fetch all the restaurant records
        restaurants = cursor.fetchall()
        cursor.close()
        
        return render_template('user_homepage.html', restaurants=restaurants)
    
    @app.route('/add_item',methods=['GET','POST'])
    def add_item(): 
        '''
        Renders and displays the adding item page. 
        '''
        if request.method == 'POST':
            return redirect(url_for('restaurant_owner_pov'))
        return render_template('add_item.html')


    @app.route('/manage_account',methods=['GET','POST'])
    def manageAccount():
        '''
        Enables users to modify their account details.
        '''
        success = False  # Initialize success flag

        if request.method == 'POST':
            success = True

        return render_template('manage_account.html', success=success)

    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        '''
        Adds to cart list
        '''
        item_id = request.form.get('item_id')
        restaurant_id = request.form.get('restaurant_id')

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fooditem WHERE fooditem_id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()

        if item:
            # Check if a cart exists in the session, create one if not
            if 'cart' not in session:
                session['cart'] = []

            # Add the item to the user's cart in the session
            session['cart'].append(item.name)

        return redirect(url_for('restaurant_details', restaurant_id=restaurant_id))


    
    @app.route('/shopping_cart')
    def viewShoppingCart():
        '''
        Provides users with their shopping cart
        '''
        return render_template('shopping_cart.html')

    def placeOrder():
        '''
        Allows users to place new orders for food. 
        '''
        pass

    def cancelOrder():
        '''
        Permits users to cancel their placed orders.        
        '''
        pass

    def reportWrongOrder():
        '''
        Enables users to report issues with their orders. 
        '''
        pass

class Restaurant:
    '''
    An object that represents how restaurant owners can interact with the application
    '''
    def __init__(self, restaurantID, name, category, address):
        """
        Constructs all the necessary attributes for the restaurant object.

        Parameters
        ----------
            restaurantID : int 
                Restaurant's unique identifier
            name : string 
                Restaurant's name
            category : string 
                Restaurant's category of food they make
            address : string 
                Restaurant's address 
            foodItems : array 
                Array of possible food items to buy at the restaurant

        """
        self.restaurantID = restaurantID
        self.name = name
        self.category = category
        self.address = address
        self.foodItems = []

    @app.route('/restaurant_details/<int:restaurant_id>')
    def restaurant_details(restaurant_id):
        '''
            Renders and displays the specific restaurant page based on its ID.
        '''
        '''
        Renders and displays the user homepage. 
        '''
        cursor = db.cursor(dictionary=True)
        # Fetch restaurant information based on restaurant_id
        cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurant_id,))
        restaurant_info = cursor.fetchone()

        # Execute a query to fetch restaurant data
        cursor.execute("SELECT * FROM fooditem WHERE restaurant_id_fk = %s",(restaurant_id,))

        # Fetch all the restaurant records
        items = cursor.fetchall()
        cursor.close()
        
        return render_template('restaurant_details.html', restaurant_info=restaurant_info, items=items)
        

    @app.route('/restaurant_owners/<int:restaurantowner_id>')
    def restaurant_owner_pov(restaurantowner_id): 
        '''
            Renders and displays the specific restaurant page FROM THE OWNER PERSPECTIVE.
        '''
        cursor = db.cursor(dictionary=True)
        # Fetch restaurant information based on restaurant_id
        cursor.execute("SELECT * FROM restaurant_owner WHERE restaurantowner_id = %s", (restaurantowner_id,))
        restaurantowner_info = cursor.fetchone()

        cursor.execute("SELECT * FROM restaurant WHERE restaurant_id = %s", (restaurantowner_id,))
        restaurant_info = cursor.fetchone()

        # Execute a query to fetch restaurant data
        cursor.execute("SELECT * FROM fooditem WHERE restaurant_id_fk = %s",(restaurantowner_id,))

        # Fetch all the restaurant records
        items = cursor.fetchall()
        cursor.close()
        
        return render_template('restaurant_owner.html', restaurantowner_info=restaurantowner_info, restaurant_info=restaurant_info, items=items)

    @app.route('/addItem/<int:restaurantowner_id>', methods=['GET','POST'])
    def addItem(restaurantowner_id):
        '''
            Enables a restaurant to add a new menu item. 
        '''
        success = False
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            image_url = request.form.get('image_url')

            try:
                
                cursor.execute("INSERT INTO fooditem (name, price, image_url, restaurant_id_fk) VALUES (%s, %s, %s, %s)", (name, price, image_url, restaurantowner_id))
                db.commit()
                success = True
            except mysql.connector.Error as err:
                db.rollback()
            


        return render_template('add_item.html', success=success, restaurantowner_id=restaurantowner_id)
    
    @app.route('/edit_restaurant_info/<int:restaurantowner_id>', methods=['GET','POST'])
    def editRestaurant(restaurantowner_id):
        '''
            Enables a restaurant to make edits to a menu item. 
        '''
        success = False

        if request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')
            delivery_fee = request.form.get('delivery_fee')
            
            # Update the restaurant's information in the database
            cursor.execute("UPDATE restaurant SET name = %s, category = %s, delivery_fee = %s WHERE restaurantowner_id = %s", (name, category, delivery_fee, restaurantowner_id))
            db.commit()

            success = True

        return render_template('edit_restaurant_info.html', success=success, restaurantowner_id=restaurantowner_id)

    def deleteItem(self, food_item_id):
        '''
            Enables a restaurant to delete a menu item. 
        '''
        pass

class Order:
    '''
    An object for the order placed by user
    '''
    def __init__(self, orderID, orderStatus, totalPrice, deliveryAddress):
        self.orderID = orderID
        self.orderStatus = orderStatus
        self.totalPrice = totalPrice
        self.deliveryAddress = deliveryAddress

    def calculateprice():
        '''
        A function to calculate the total price
        '''
        pass


if __name__ == '__main__':
    app.run(debug=True)

@app.teardown_appcontext
def close_db(error):
    if hasattr(cursor, 'close'):
        cursor.close()
    if hasattr(db, 'close'):
        db.close()