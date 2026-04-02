from flask import Blueprint, request, jsonify
from . import db
from .models import Message, DailyArtifact, User, Product, ProductVariant, CartItem, Order, OrderItem
from zhipuai import ZhipuAI
from sqlalchemy import or_
import random
import datetime
import time
# 确保导入了 Quiz 和 func
from .models import Message, DailyArtifact, User, Product, ProductVariant, CartItem, Order, OrderItem, Quiz
from sqlalchemy.sql.expression import func
from .models import Message, DailyArtifact, User, Product, ProductVariant, CartItem, Order, OrderItem, Quiz, CustomOrder

bp = Blueprint('api', __name__, url_prefix='/api')
client = ZhipuAI(api_key="69c729c061af4cf590f6079d0ea1c1cb.J7RQE5IslWO6rnzT")


# ==========================================
# 1. 认证模块 (注册/登录/头像)
# ==========================================

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json();
    username = data.get('username');
    password = data.get('password')
    if not username or not password: return jsonify({'error': '用户名和密码不能为空'}), 400
    if User.query.filter_by(username=username).first(): return jsonify({'error': '用户名已存在'}), 400
    try:
        new_user = User(username=username);
        new_user.set_password(password)
        db.session.add(new_user);
        db.session.commit()
        return jsonify({'message': '注册成功', 'user': new_user.to_dict()}), 201
    except Exception as e:
        db.session.rollback(); return jsonify({'error': str(e)}), 500


@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json();
    username = data.get('username');
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': '登录成功', 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': '用户名或密码错误'}), 401


@bp.route('/auth/avatar', methods=['POST'])
def update_avatar():
    data = request.get_json();
    user = User.query.get(data.get('userId'))
    if user: user.avatar = data.get('avatarUrl'); db.session.commit(); return jsonify(
        {'message': '成功', 'avatar': user.avatar}), 200
    return jsonify({'error': '用户不存在'}), 404


# ==========================================
# 2. 商城核心业务 (商品/购物车/订单)
# ==========================================

# --- 商品查询 ---
@bp.route('/shop/products', methods=['GET'])
def get_products():
    category = request.args.get('category');
    scene = request.args.get('scene');
    search_query = request.args.get('q')
    page = request.args.get('page', 1, type=int);
    per_page = request.args.get('per_page', 12, type=int)
    query = Product.query
    if category and category != 'all': query = query.filter_by(category=category)
    if scene and scene != 'all': query = query.filter_by(scene=scene)
    if search_query: query = query.filter(Product.name.like(f'%{search_query}%'))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(
        {'products': [p.to_dict() for p in pagination.items], 'total': pagination.total, 'pages': pagination.pages,
         'current_page': page}), 200


# --- 购物车 ---
@bp.route('/shop/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('userId')
    return jsonify([i.to_dict() for i in CartItem.query.filter_by(user_id=user_id).all()] if user_id else []), 200


@bp.route('/shop/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json();
    user_id = data.get('userId');
    variant_id = data.get('variantId');
    quantity = int(data.get('quantity', 1))
    cart_item = CartItem.query.filter_by(user_id=user_id, variant_id=variant_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        db.session.add(CartItem(user_id=user_id, variant_id=variant_id, quantity=quantity))
    db.session.commit();
    return jsonify({'message': '成功'}), 200


# --- 下单 (带地址) ---
@bp.route('/shop/orders/create', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data.get('userId');
    discount = data.get('discount', 0)
    addr = data.get('addressInfo', {})

    if not all([addr.get('name'), addr.get('phone'), addr.get('address')]):
        return jsonify({'error': '收货信息不完整'}), 400

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items: return jsonify({'error': '购物车为空'}), 400

    try:
        # 创建订单
        new_order = Order(
            user_id=user_id, total_price=0, status='Pending',
            receiver_name=addr.get('name'), receiver_phone=addr.get('phone'), address=addr.get('address')
        )
        db.session.add(new_order);
        db.session.flush()

        total_price = 0
        for item in cart_items:
            variant = item.variant
            variant.stock -= item.quantity  # 简单扣库存
            price = variant.price
            total_price += price * item.quantity
            db.session.add(
                OrderItem(order_id=new_order.id, product_name=variant.product.name, variant_name=variant.name,
                          quantity=item.quantity, price=price))
            db.session.delete(item)  # 清空购物车

        new_order.total_price = max(0, total_price - discount)
        db.session.commit()
        return jsonify({'message': '下单成功', 'orderId': new_order.id, 'totalPrice': new_order.total_price}), 200
    except Exception as e:
        db.session.rollback();
        return jsonify({'error': str(e)}), 500


# --- 模拟支付 ---
@bp.route('/shop/pay', methods=['POST'])
def pay_order():
    order = Order.query.get(request.get_json().get('orderId'))
    if order and order.status == 'Pending':
        order.status = 'Paid'
        order.pay_time = datetime.datetime.now()
        order.trade_no = f"ALIPAY_{int(time.time())}_{random.randint(1000, 9999)}"
        db.session.commit()
        return jsonify({'message': '支付成功', 'tradeNo': order.trade_no}), 200
    return jsonify({'error': '订单状态异常'}), 400


# --- 订单列表 ---
@bp.route('/shop/orders', methods=['GET'])
def get_orders():
    orders = Order.query.filter_by(user_id=request.args.get('userId')).order_by(Order.created_at.desc()).all()
    res = []
    for o in orders:
        d = o.to_dict()
        d.update({'receiverName': o.receiver_name, 'receiverPhone': o.receiver_phone, 'address': o.address})
        res.append(d)
    return jsonify(res), 200


# --- 确认收货 ---
@bp.route('/shop/orders/receive', methods=['POST'])
def confirm_receive():
    order = Order.query.get(request.get_json().get('orderId'))
    if order and order.status == 'Shipped':
        order.status = 'Completed';
        order.finish_time = datetime.datetime.now()
        db.session.commit();
        return jsonify({'message': '交易完成'}), 200
    return jsonify({'error': '操作失败'}), 400


# --- 商家发货 (测试用) ---
@bp.route('/shop/orders/ship', methods=['POST'])
def ship_order():
    order = Order.query.get(request.get_json().get('orderId'))
    if order and order.status == 'Paid':
        order.status = 'Shipped';
        order.delivery_time = datetime.datetime.now()
        db.session.commit();
        return jsonify({'message': '发货成功'}), 200
    return jsonify({'error': '失败'}), 400


# ==========================================
# 3. 辅助接口 (轮播/优惠券/新闻/AI/DIY)
# ==========================================

@bp.route('/shop/hot_products', methods=['GET'])
def get_hot_products():
    all_p = Product.query.all()
    return jsonify([p.to_dict() for p in (random.sample(all_p, 5) if len(all_p) > 5 else all_p)]), 200


@bp.route('/shop/coupons', methods=['GET'])
def get_coupons():
    return jsonify([
        {'id': 1, 'amount': 100, 'threshold': 1000, 'name': '非遗大额券', 'desc': '满1000减100'},
        {'id': 2, 'amount': 50, 'threshold': 500, 'name': '吉州窑专享', 'desc': '满500减50'},
        {'id': 3, 'amount': 20, 'threshold': 0, 'name': '无门槛体验', 'desc': '下单即减'},
    ]), 200


@bp.route('/shop/news', methods=['GET'])
def get_news():
    return jsonify([
        {'id': 1, 'title': '吉州窑木叶盏：千年窑火中的树叶重生', 'date': '2025-01-04', 'tag': '文化'},
        {'id': 2, 'title': '鄂州剪纸传承人新作亮相国际艺术展', 'date': '2025-01-02', 'tag': '资讯'},
        {'id': 3, 'title': '如何鉴别手工剪纸与机器剪纸？专家教你三招', 'date': '2024-12-28', 'tag': '科普'},
        {'id': 4, 'title': '新中式家居搭配指南：当瓷器遇上剪纸', 'date': '2024-12-25', 'tag': '生活'}
    ]), 200


@bp.route('/shop/news/<int:id>', methods=['GET'])
def get_news_detail(id):
    news_db = {
        1: {'title': '吉州窑木叶盏：千年窑火中的树叶重生',
            'content': '木叶盏是吉州窑独步宋代的 “窑火魔术”，也是中国陶瓷史上 “以自然入器” 的极致代表。\n\n取秋日菩提叶或桑叶，经浸蜡、描纹、覆于黑釉瓷胎之上，入窑经 1300℃高温焙烧，树叶肌理与窑变釉色相融 —— 叶片脉络如描金般浮于黑釉之上，边缘晕染出 “窑变天目” 的虹彩光泽，最终成就 “一叶一器，无有同者” 的孤品。\n\n它不止是茶器：宋代文人以木叶盏盛茶，观叶影浮沉，暗合禅宗 “一叶一菩提” 的哲思；如今，吉州窑传承人在传统工艺基础上，融入鄂州剪纸的 “游丝纹” 叶脉装饰，让木叶盏成为 “窑纸共生” 的新非遗载体。',
            'date': '2025-01-04'},
        2: {'title': '鄂州剪纸传承人新作亮相国际艺术展',
            'content': '近日，巴黎卢浮宫 “东方非遗展” 现场，一幅宽 5 米、高 2.8 米的鄂州剪纸作品《长江万里图》，让欧洲观众驻足惊叹。\n\n这幅作品由鄂州剪纸省级传承人耗时 3 个月完成：以 “千刻不落、万剪不断” 的技法，将长江三峡、黄鹤楼、武汉长江大桥等景观，与鄂州剪纸经典的 “龙凤纹”“缠枝莲纹” 交织，甚至在船帆纹样中藏入吉州窑 “木叶纹” 细节，暗合 “窑纸同源” 的非遗融合主题。展方评价：“它不止是剪纸，更是用东方线条写就的长江史诗。”',
            'date': '2025-01-02'},
        3: {'title': '鉴别手工剪纸秘籍',
            'content': '市场上机器剪纸泛滥，如何锁定真正的鄂州手工剪纸？\n3 个细节帮你鉴别：\n\n1.刀口：手工剪刻的线条边缘有细微 “毛刺感”（是剪刀 / 刻刀与纸张摩擦的自然痕迹），机器冲压则边缘过于平滑、无手工温度；\n\n2.看纸张：正宗鄂州剪纸用 “万年红” 宣纸，薄而韧，透光可见纤维纹理；机器剪纸多用水印纸，手感偏硬、易脆裂；\n\n3.看构图：手工剪纸的 “游丝纹”“月牙纹” 会随匠人手法有细微弧度变化，构图灵动自然；机器剪纸的纹样是复刻模板，线条僵硬、无变化。',
            'date': '2024-12-28'},
        4: {'title': '新中式家居指南',
            'content': '想让现代家居透出东方韵味？试试 “吉州窑 + 鄂州剪纸” 的搭配公式：\n\n1、客厅 C 位：\n摆一件吉州窑黑釉木叶梅瓶，瓶身插一支干莲蓬，旁挂一幅鄂州剪纸 “缠枝莲纹” 装饰画，黑釉的沉静与剪纸的红韵形成视觉呼应；\n\n2、茶桌点睛：\n用吉州窑剪纸贴花盏承茶，搭配同纹样的剪纸杯垫，喝茶时指尖触到的既是窑火温度，也是剪纸的细腻；\n\n3、角落氛围：\n在玄关柜上放一盏 “窑纸融合” 小夜灯（吉州窑瓷座 + 剪纸灯罩），灯光透过剪纸纹样，在墙面投出细碎光影，氛围感拉满。',
            'date': '2024-12-25'}
    }
    return jsonify(news_db.get(id, {'title': '资讯不存在', 'content': ''})), 200


@bp.route('/shop/diy/patterns', methods=['GET'])
def get_diy_patterns():
    return jsonify([{'id': 1, 'name': '连年有余', 'img': 'paper_fish_knot.png'},
                    {'id': 2, 'name': '百鸟朝凤', 'img': 'paper_phoenix.png'},
                    {'id': 3, 'name': '喜上眉梢', 'img': 'paper_wedding.png'},
                    {'id': 4, 'name': '荷塘月色', 'img': 'paper_lotus.png'}]), 200


@bp.route('/messages/submit', methods=['POST'])
def submit_message():
    data = request.get_json()
    # 打印一下，看看后台有没有收到请求
    print(f">>> 收到留言: {data}")

    new_message = Message(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        subject=data.get('subject'),
        content=data.get('message')
    )

    try:
        db.session.add(new_message)
        db.session.commit()  # 🔥 这一行最重要，没有它就不会写入数据库
        return jsonify({'message': '留言提交成功！'}), 201
    except Exception as e:
        db.session.rollback()
        print(f">>> 留言失败: {e}")
        return jsonify({'message': str(e)}), 500


@bp.route('/artifacts', methods=['GET'])
def get_artifacts(): return jsonify([a.to_dict() for a in DailyArtifact.query.all()]), 200


@bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    # 1. 获取前端传来的 JSON 数据
    data = request.get_json()
    user_input = data.get('message', '')

    if not user_input:
        return jsonify({"answer": "你想了解哪方面的非遗知识呢？"}), 400

    try:
        # 2. 调用智谱 AI (GLM-4) 接口
        # 这里的 client 是你在 routes.py 开头定义的那个 ZhipuAI 实例
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位精通中国非物质文化遗产的专家，特别擅长吉州窑陶瓷制作（木叶天目）和鄂州雕花剪纸艺术。请用亲切、活泼、充满文化底蕴的语气回答用户。回复中可以使用 HTML 标签加粗重点。"
                },
                {"role": "user", "content": user_input}
            ],
            top_p=0.7,
            temperature=0.9,
        )

        # 3. 解析 AI 回复并返回
        ai_answer = response.choices[0].message.content
        return jsonify({"answer": ai_answer}), 200

    except Exception as e:
        print(f">>> AI 接口调用失败: {e}")
        return jsonify({"answer": "抱歉，守艺人由于由于功力（网络）不足，暂时无法回答您。"}), 500# 占位


# --- 接口: 随机获取一道题目 ---
@bp.route('/shop/quiz/random', methods=['GET'])
def get_random_quiz():
    try:
        # 使用 func.random() 从数据库随机取一条
        quiz = Quiz.query.order_by(func.random()).first()

        if not quiz:
            return jsonify({'error': '题库为空'}), 404

        return jsonify(quiz.to_dict()), 200
    except Exception as e:
        print(f"Quiz Error: {e}")
        return jsonify({'error': str(e)}), 500


# --- 接口: 提交定制需求 (真实入库) ---
@bp.route('/custom/create', methods=['POST'])
def create_custom_order():
    data = request.get_json()

    # 必填校验
    if not data.get('contact') or not data.get('artifact') or not data.get('pattern'):
        return jsonify({'error': '请填写完整信息（联系方式、器具、纹样必填）'}), 400

    try:
        new_custom = CustomOrder(
            user_name=data.get('userName', '匿名客户'),
            contact=data.get('contact'),
            pattern_name=data.get('pattern'),
            pattern_img=data.get('patternImg'),
            artifact_type=data.get('artifact'),
            position=data.get('position', '默认位置'),
            note=data.get('note', '')
        )

        db.session.add(new_custom)
        db.session.commit()

        return jsonify({'message': '定制需求提交成功！', 'id': new_custom.id}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Custom Order Error: {e}")
        return jsonify({'error': '提交失败，请联系客服'}), 500