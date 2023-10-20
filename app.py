from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


class User:
    def __init__(self, UserID, email, password, name, address):
        self.UserID = UserID
        self.email = email
        self.password = password
        self.name = name
        self.address = address
        self.paymentDetails = {} 
        self.cart = []

    @app.route('/register_page')
    def register():
        return render_template('register_page.html')

    @app.route('/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            return redirect(url_for('user_homepage'))
        return render_template('front_page.html')
    
    @app.route('/user_homepage')
    def user_homepage():
        return render_template('user_homepage.html')

    def manageAccount():
        pass

    def viewPastOrders():
        pass

    def placeOrder():
        pass

    def cancelOrder():
        pass

    def reportWrongOrder():
        pass

class Restaurant:
    def __init__(self, restaurantID, name, category, address):
        self.restaurantID = restaurantID
        self.name = name
        self.category = category
        self.address = address
        self.foodItems = []

    @app.route('/restaurant_details')
    def restaurant_details():
        return render_template('restaurant_details.html')

    def addItem(self, food_item):
        pass

    def editItem(self, food_item_id, updated_item):
        pass

    def deleteItem(self, food_item_id):
        pass
 


if __name__ == '__main__':
    app.run(debug=True)


