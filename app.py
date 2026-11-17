from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///canteen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------------------------------------------------------
# Database Models
# -------------------------------------------------------------------------
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cuisine = db.Column(db.String(50), nullable=False)  # Chinese, South Indian, North Indian, Snacks, Beverages

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), nullable=False)
    pickup_slot = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Preparing, Ready, Picked Up
    payment_method = db.Column(db.String(50), default='Pay at Counter')  # Pay at Counter or UPI QR Code
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    item = db.relationship('MenuItem')

# -------------------------------------------------------------------------
# Database Initialization & Multi-Cuisine Seed Data
# -------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    if not MenuItem.query.first():
        sample_items = [
            # Chinese Counter
            MenuItem(name='Veg Hakka Noodles', price=80.0, cuisine='Chinese'),
            MenuItem(name='Chilli Chicken (4 pcs)', price=120.0, cuisine='Chinese'),
            MenuItem(name='Steam Veg Momos (6 pcs)', price=60.0, cuisine='Chinese'),
            
            # South Indian Counter
            MenuItem(name='Masala Dosa', price=70.0, cuisine='South Indian'),
            MenuItem(name='Idli Sambhar (2 pcs)', price=40.0, cuisine='South Indian'),
            
            # North Indian & Snacks Counter
            MenuItem(name='Paneer Butter Masala & Paratha', price=110.0, cuisine='North Indian'),
            MenuItem(name='Samosa (2 pcs)', price=20.0, cuisine='Snacks'),
            MenuItem(name='Veg Club Sandwich', price=50.0, cuisine='Snacks'),
            
            # Beverages Counter
            MenuItem(name='Cold Coffee', price=45.0, cuisine='Beverages'),
            MenuItem(name='Masala Chai', price=15.0, cuisine='Beverages')
        ]
        db.session.add_all(sample_items)
        db.session.commit()

# -------------------------------------------------------------------------
# Application Routes
# -------------------------------------------------------------------------

@app.route('/')
def index():
    items = MenuItem.query.all()
    # Group items by cuisine category for the frontend view
    grouped_menu = {}
    for item in items:
        if item.cuisine not in grouped_menu:
            grouped_menu[item.cuisine] = []
        grouped_menu[item.cuisine].append(item)
    return render_template('index.html', grouped_menu=grouped_menu)


@app.route('/place_order', methods=['POST'])
def place_order():
    student_name = request.form.get('student_name')
    roll_number = request.form.get('roll_number')
    pickup_slot = request.form.get('pickup_slot')
    payment_method = request.form.get('payment_method')
    
    items = MenuItem.query.all()
    total_price = 0.0
    order_items_to_create = []

    # Calculate bill and filter out selected quantities
    for item in items:
        qty = int(request.form.get(f'quantity_{item.id}', 0))
        if qty > 0:
            total_price += item.price * qty
            order_items_to_create.append((item.id, qty))

    if total_price == 0:
        return "Please select at least one item before placing an order.", 400

    # Create new master order record
    new_order = Order(
        student_name=student_name,
        roll_number=roll_number,
        pickup_slot=pickup_slot,
        total_price=total_price,
        payment_method=payment_method
    )
    db.session.add(new_order)
    db.session.commit()

    # Create relational order line items
    for item_id, qty in order_items_to_create:
        order_item = OrderItem(order_id=new_order.id, menu_item_id=item_id, quantity=qty)
        db.session.add(order_item)
    
    db.session.commit()
    return redirect(url_for('order_status', order_id=new_order.id))


@app.route('/order_status/<int:order_id>')
def order_status(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_status.html', order=order)


@app.route('/vendor/dashboard')
def vendor_dashboard():
    # Retrieve all orders sorted by newest first
    orders = Order.query.order_by(Order.id.desc()).all()
    return render_template('vendor.html', orders=orders)


@app.route('/vendor/update_status', methods=['POST'])
def update_status():
    order_id = request.form.get('order_id')
    new_status = request.form.get('status')
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
    return redirect(url_for('vendor_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)