from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================
# 1. 用户表
# ==========================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar = db.Column(db.String(200), default='default_avatar.png')
    created_at = db.Column(db.DateTime, default=datetime.now)

    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'avatar': self.avatar
        }


# ==========================================
# 2. 商品主表
# ==========================================
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    scene = db.Column(db.String(50), nullable=False, default='home')
    main_image = db.Column(db.String(120), nullable=False)

    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'scene': self.scene,
            'mainImage': f"/images/products/{self.main_image}",
            'variants': [v.to_dict() for v in self.variants]
        }


# ==========================================
# 3. 商品款式表
# ==========================================
class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=100)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }


# ==========================================
# 4. 购物车表
# ==========================================
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variants.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    variant = db.relationship('ProductVariant')

    def to_dict(self):
        return {
            'id': self.id,
            'productId': self.variant.product.id,
            'productName': self.variant.product.name,
            'variantId': self.variant.id,
            'variantName': self.variant.name,
            'price': self.variant.price,
            'quantity': self.quantity,
            'image': f"/images/products/{self.variant.product.main_image}"
        }


# ==========================================
# 5. 订单主表
# ==========================================
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now)

    receiver_name = db.Column(db.String(50))
    receiver_phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    trade_no = db.Column(db.String(64))
    pay_time = db.Column(db.DateTime)
    delivery_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'totalPrice': self.total_price,
            'status': self.status,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': [i.to_dict() for i in self.items]
        }


# ==========================================
# 6. 订单详情表
# ==========================================
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_name = db.Column(db.String(120), nullable=False)
    variant_name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'productName': self.product_name,
            'variantName': self.variant_name,
            'quantity': self.quantity,
            'price': self.price
        }


# ==========================================
# 7. 其他表 (留言, 文物)
# ==========================================
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class DailyArtifact(db.Model):
    __tablename__ = 'daily_artifacts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    era = db.Column(db.String(50))
    specs = db.Column(db.String(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_name = db.Column(db.String(100))
    publish_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'era': self.era,
            'specs': self.specs,
            'location': self.location,
            'description': self.description,
            'image_name': self.image_name
        }


# ==========================================
# 8. 趣味问答表
# ==========================================
class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'options': [
                {'key': 'A', 'text': self.option_a},
                {'key': 'B', 'text': self.option_b},
                {'key': 'C', 'text': self.option_c}
            ],
            'correct': self.correct_option,
            'explanation': self.explanation
        }


# ==========================================
# 9. 定制订单表 (注意缩进：它必须在最外层，不能在 Quiz 里面)
# ==========================================
class CustomOrder(db.Model):
    __tablename__ = 'custom_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=True)
    contact = db.Column(db.String(100), nullable=False)
    pattern_name = db.Column(db.String(100), nullable=False)
    pattern_img = db.Column(db.String(255), nullable=True)
    artifact_type = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=True)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'userName': self.user_name,
            'contact': self.contact,
            'pattern': self.pattern_name,
            'artifact': self.artifact_type,
            'position': self.position,
            'note': self.note,
            'status': self.status,
            'createTime': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }