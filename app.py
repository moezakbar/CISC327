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

# Global variable to store the shopping cart
shopping_cart = []

def clear_shopping_cart():
    global shopping_cart
    shopping_cart = []

    

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

        # Clear the shopping cart when the user visits the home page
        clear_shopping_cart()

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            address = request.form.get('address')
            card_number = request.form.get('card_number')
            expiration_date = request.form.get('expiration_date')
            cvv = request.form.get('cvv')

            try:
                if (password == None) or (password == ""):
                    raise mysql.connector.Error
                cursor.execute("INSERT INTO user (email, name, address, card_number, expiration_date, cvv, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",(email, name, address, card_number, expiration_date, cvv, password))
                db.commit()  # Commit the changes to the database
                cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
                return redirect(url_for('user_homepage', user_id=user[0]))
            except mysql.connector.Error as err:
                db.rollback()
                error_message = "Invalid registration information"
                return render_template('register_page.html', error_message=error_message)
            
        return render_template('register_page.html')

    @app.route('/', methods=['GET', 'POST'])
    def login():
        '''
            Allows users to log into their accounts. 
            Renders the login page for the application. 
            Once user is logged in, it redirects user to the frontpage.
	    If the person logging in is a restaurant owner, it will redirect to their restaurant page.
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
                    return redirect(url_for('user_homepage', user_id=user[0]))
                else:
                    # User doesn't exist or invalid credentials, show an error message
                    error_message = "Invalid email or password"
                    return render_template('front_page.html', error_message=error_message)


        return render_template('front_page.html')
    
    @app.route('/user_homepage/<int:user_id>')
    def user_homepage(user_id): 
        '''
        Renders and displays the user homepage. 
	The user can pick a restaurant they want to order at.
        '''
        cursor = db.cursor(dictionary=True)
        # Execute a query to fetch restaurant data
        cursor.execute("SELECT * FROM restaurant")

        # Fetch all the restaurant records
        restaurants = cursor.fetchall()
        cursor.close()
        
        return render_template('user_homepage.html', restaurants=restaurants, user_id=user_id)
    
    @app.route('/add_item',methods=['GET','POST'])
    def add_item(): 
        '''
        Renders and displays the adding item page. 
        '''
        if request.method == 'POST':
            return redirect(url_for('restaurant_owner_pov'))
        return render_template('add_item.html')


    @app.route('/manage_account/<int:user_id>',methods=['GET','POST'])
    def manageAccount(user_id):
        '''
        Enables users to modify their account details.
	    Renders and displays the manage_account.html
        '''
        

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.execute("SELECT password FROM user WHERE user_id = %s", (user_id,))
        current_password = cursor.fetchone()["password"]

        success = False
        if request.method == 'POST':
            oldpassword = request.form.get('oldpassword')
            newpassword = request.form.get('newpassword')
            address = request.form.get('address')
            card_number = request.form.get('card_number')
            expiration_date = request.form.get('expiration_date')
            cvv = request.form.get('cvv')

            try:
                if oldpassword == current_password:
                    cursor.execute("UPDATE user SET address = %s, password = %s, card_number = %s, expiration_date = %s, cvv = %s WHERE user_id = %s", (address, newpassword, card_number, expiration_date,cvv,user_id))
                    db.commit()
                    success = True
                    return redirect(url_for('user_homepage', user_id=user_id))
                else:
                    raise mysql.connector.Error
            except mysql.connector.Error as err:
                    db.rollback()
                    error_message = "Invalid account information"
                    return render_template('manage_account.html', user_id=user_id, error_message=error_message)
            
        cursor.close()
        return render_template('manage_account.html', success=success, user_id=user_id, user_name=user['name'])

    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        '''
        Adds to cart list
        '''
        item_id = request.form.get('item_id')
        restaurant_id = request.form.get('restaurant_id')
        user_id = request.form.get('user_id')

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fooditem WHERE fooditem_id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()

        if item:
            shopping_cart.append(item)

        print(f"Redirecting to restaurant_details with restaurant_id: {restaurant_id}, user_id: {user_id}")
        return redirect(url_for('restaurant_details', restaurant_id=restaurant_id, user_id=user_id))


    
    @app.route('/shopping_cart/<int:user_id>')
    def viewShoppingCart(user_id):
        '''
        Provides users with their shopping cart
        '''
        cart = shopping_cart

        totalprice = sum(item['price'] for item in cart)
        total_price = float(totalprice)
        subtotal = round(total_price + 0.99, 2)


        return render_template('shopping_cart.html', cart=cart, total_price=total_price, subtotal=subtotal, user_id=user_id)

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

    @app.route('/restaurant_details/<int:restaurant_id>/<int:user_id>')
    def restaurant_details(restaurant_id, user_id):
        '''
            Renders and displays the specific restaurant page based on its ID to the users.
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
        
        return render_template('restaurant_details.html', restaurant_info=restaurant_info, items=items, user_id=user_id)
        

    @app.route('/restaurant_owner/<int:restaurantowner_id>')
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
        
        return render_template('restaurant_owner.html', restaurantowner_info=restaurantowner_info, restaurant_info=restaurant_info, items=items, restaurantowner_id=restaurantowner_id)

    @app.route('/addItem/<int:restaurantowner_id>', methods=['GET','POST'])
    def addItem(restaurantowner_id):
        '''
            Enables a restaurant to add a new menu item.
	    Renders and displays add_item.html
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
	    Renders and displays edit_restaurant_info.html
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

    @app.route('/deleteItem', methods=['POST'])
    def deleteItem():
        '''
            Enables a restaurant to delete a menu item. 
        '''
        restaurantowner_id = request.form['restaurantowner_id']
        food_item_id = request.form['food_item_id']
        cursor.execute("DELETE FROM fooditem WHERE fooditem_id = %s", (food_item_id,))
        db.commit()
        return redirect(url_for('restaurant_owner_pov', restaurantowner_id=restaurantowner_id))



if __name__ == '__main__':
    app.run(debug=True)

@app.teardown_appcontext
def close_db(error):
    if hasattr(cursor, 'close'):
        cursor.close()
    if hasattr(db, 'close'):
        db.close()
