# Name: Abdulmoez Akbar(20258267), Ovil Miranda(20284057), Ava Salas(20280689)
# Group number: 3
# This is the main running file for the app. To run it, Python Flask needs to be installed. Once done, you can type
# "Python app.py" on the terminal to open the website.
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
            return redirect(url_for('user_homepage'))
        return render_template('register_page.html')

    @app.route('/', methods=['GET', 'POST'])
    def login():
        '''
            Allows users to log into their accounts. 
            Renders the login page for the application. 
            Once user is logged in, it redirects user to the frontpage 
        '''
        if request.method == 'POST':
            if request.form.get('businessPortal'):
                # If checked, redirect to the restaurant owner page
                return redirect(url_for('restaurant_owner_pov'))
            else:
                # If not checked, redirect to the user homepage
                return redirect(url_for('user_homepage'))
            
        return render_template('front_page.html')
    
    @app.route('/user_homepage')
    def user_homepage(): 
        '''
        Renders and displays the user homepage. 
        '''
        return render_template('user_homepage.html')
    
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

    def viewPastOrders():
        '''
        Provides users with a history of their past orders. 
        '''
        pass
    
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

    @app.route('/restaurant_details')
    def restaurant_details():
        '''
            Renders and displays the specific restaurant page based on its ID.
        '''
        return render_template('restaurant_details.html')
    
    @app.route('/restaurant_owners')
    def restaurant_owner_pov(): 
        '''
            Renders and displays the specific restaurant page FROM THE OWNER PERSPECTIVE.
        '''
        return render_template('restaurant_owner.html')

    def addItem(self, food_item):
        '''
            Enables a restaurant to add a new menu item. 
        '''
        pass
    
    @app.route('/edit_restaurant_info')
    def editRestaurant():
        '''
            Enables a restaurant to make edits to a menu item. 
        '''
        return render_template('edit_restaurant_info.html')

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


