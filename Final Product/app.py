from flask import Flask, render_template, request, redirect
import random
from datetime import datetime


product = ''
price = 0.0
uniqueNumber = 0
totalPrice = 0.0
value = []
values = []
isOrderReady = False
orderStatus = False
orderNumber = 0




def name_a_product(name):
    product = name


app = Flask(__name__)

orders = []


def time():
    now = datetime.now()
    return now

@app.route('/')
def show_menu():
    return render_template('menu.html', values=values)


@app.route('/orders')
def show_orders():
    return render_template('order.html', orders=orders)





@app.route('/receive_order', methods=['POST'])
def receive_order():
    global orderIDs
    global randomID
    global orderNumber
    data = request.get_json()
    orderNumber += 1
    
    
    order = {
        'order_id': orderNumber,  # Generate a unique order ID
        'pizza': data['orderList'],  # Assuming you want to store the list of ordered items
        'timestamp': datetime.now(),
        'status': 'Pending'  # Implement a timestamp function
    }
    orders.insert(0, order)
    return redirect('/')



@app.route('/remove_order/<int:order_id>', methods=['GET'])
def remove_order(order_id):
    global orders
    orders = [order for order in orders if order['order_id'] != order_id]
    return redirect('/orders')


@app.route('/order_ready', methods=['POST'])
def order_ready():
    global isOrderReady
    global currentElemnt

    data = request.get_json()
    isOrderReady = data['orderReady']
    first_order = [x for x in orders if x['status'] == 'Pending'][0]
    if first_order:
        first_order['status'] = 'Finished'

    print(isOrderReady)    

    return redirect('/orders')
















#@app.route('/update_order_status', methods=['POST'])
#def update_order_status():
#    data = request.get_json()
#    order_status = data.get("Order status")
#    if order_status:
#        order_status = "green"
    