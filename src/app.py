import csv  # برای خواندن و نوشتن فایل‌های CSV
from datetime import date  # برای گرفتن تاریخ امروز

from User import User  # وارد کردن کلاس کاربر
from Product import Product  # وارد کردن کلاس محصول
from orderitems import OrderItemsManager  # کلاس مدیریت آیتم‌های سفارش
from Order import Order  # کلاس سفارش


# تعریف کلاس اصلی اپلیکیشن فروشگاه
class StoreApp:
    def __init__(self):
        self.users = {}  # دیکشنری کاربران، کلید: username، مقدار: شی User
        self.products = {}  # دیکشنری محصولات، کلید: product_id، مقدار: شی Product
        self.orders = []  # لیست سفارش‌ها
        self.order_items = OrderItemsManager()  # شی برای مدیریت آیتم‌های هر سفارش

        # بارگذاری داده‌ها هنگام راه‌اندازی برنامه
        self.load_users_from_csv('users.txt')
        self.load_products_from_csv('products.txt')
        # بارگذاری سفارشات و آیتم‌های سفارش (فایل جدید order_items.txt اضافه شده است)
        self.load_orders_from_csv('orders.txt', 'order_items.txt')

    # ------------------------- مدیریت کاربران ----------------------------
    def load_users_from_csv(self, filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if not row:
                        continue  # رد کردن ردیف‌های خالی

                    # فرمت مورد انتظار: username,password,balance,role
                    if len(row) == 4:
                        try:
                            username, password, balance_str, role = row
                            balance = float(balance_str)
                            user = User(username, password, balance, role)
                            self.users[username] = user
                        except ValueError as e:
                            print(f"⚠️ خطای تجزیه داده‌های کاربر در ردیف {i + 1}: {row}. خطا: {e}")
                        except Exception as e:
                            print(f"⚠️ خطای غیرمنتظره در بارگذاری کاربر در ردیف {i + 1}: {e}")
                    else:
                        print(f"⚠️ فرمت خط نامعتبر در users.csv.txt (ردیف {i + 1} رد شد): {row}")
            print("✅ کاربران با موفقیت بارگذاری شدند!")
        except FileNotFoundError:
            print(f"❌ فایل کاربران '{filename}' یافت نشد. بدون کاربر شروع می‌شود.")
        except Exception as e:
            print(f"❌ خطای بارگذاری کاربران: {e}")

    def save_users_to_csv(self, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for user in self.users.values():
                    writer.writerow([user.username, user.password, user.balance, user.role])
            print("✅ کاربران با موفقیت ذخیره شدند!")
        except Exception as e:
            print(f"❌ خطای ذخیره کاربران: {e}")

    # ------------------------- مدیریت محصولات ----------------------------
    def load_products_from_csv(self, filename):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if not row:
                        continue  # رد کردن ردیف‌های خالی
                    # P101,Laptop,25000000,5,Electronics
                    if len(row) == 5:
                        try:
                            product_id, name, price_str, stock_str, category = row
                            price = float(price_str)
                            stock = int(stock_str)
                            product = Product(product_id, name, price, stock, category)
                            self.products[product.id] = product  # استفاده از product.id
                        except ValueError as e:
                            print(f"⚠️ خطای تجزیه داده‌های محصول در ردیف {i + 1}: {row}. خطا: {e}")
                        except Exception as e:
                            print(f"⚠️ خطای غیرمنتظره در بارگذاری محصول در ردیف {i + 1}: {e}")
                    else:
                        print(f"⚠️ فرمت خط نامعتبر در products.csv.txt (ردیف {i + 1} رد شد): {row}")
            print("✅ محصولات با موفقیت بارگذاری شدند!")
        except FileNotFoundError:
            print(f"❌ فایل محصولات '{filename}' یافت نشد. بدون محصول شروع می‌شود.")
        except Exception as e:
            print(f"❌ خطای بارگذاری محصولات: {e}")

    def save_products_to_csv(self, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # بدون سطر هدر فعلا برای مطابقت با فرمت اولیه، اما برای خوانایی توصیه می‌شود
                # writer.writerow(['product_id', 'name', 'price', 'stock', 'category'])
                for product in self.products.values():
                    writer.writerow([product.id, product.name, product.price, product.stock, product.category])
            print("✅ محصولات با موفقیت ذخیره شدند!")
        except Exception as e:
            print(f"❌ خطای ذخیره محصولات: {e}")

    def add_product(self, product_id, name, price, stock, category):
        """
        Adds a new product or updates an existing one.
        Returns True if added/updated, False otherwise (e.g., validation error).
        """
        if product_id in self.products:
            # Update existing product
            existing_product = self.products[product_id]
            existing_product.name = name
            existing_product.price = price
            existing_product.stock = stock
            existing_product.category = category
            self.save_products_to_csv('products.csv.txt')
            return True, "updated"
        else:
            # Add new product
            new_product = Product(product_id, name, price, stock, category)
            self.products[product_id] = new_product
            self.save_products_to_csv('products.csv.txt')
            return True, "added"

    # ------------------------- مدیریت سفارشات ----------------------------
    def load_orders_from_csv(self, orders_filename, order_items_filename):
        # بارگذاری اطلاعات اصلی سفارش
        try:
            with open(orders_filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if not row:
                        continue
                    # فرمت: order_id,username,total_price,order_date
                    if len(row) == 4:
                        try:
                            order_id, username, total_price_str, order_date_str = row
                            total_price = float(total_price_str)
                            # لیست محصولات در سفارش، فعلا به عنوان جایگزین قرار داده می‌شود، پس از بارگذاری آیتم‌های سفارش پر می‌شود
                            order = Order(username, [], order_id=order_id)
                            order.total_price = total_price  # قیمت کل را به صورت دستی برای سفارش بارگذاری شده تنظیم می‌کند
                            order.order_date = date.fromisoformat(order_date_str)
                            self.orders.append(order)
                        except ValueError as e:
                            print(f"⚠️ خطای تجزیه داده‌های سفارش در ردیف {i + 1}: {row}. خطا: {e}")
                        except Exception as e:
                            print(f"⚠️ خطای غیرمنتظره در بارگذاری سفارش در ردیف {i + 1}: {e}")
                    else:
                        print(f"⚠️ فرمت خط نامعتبر در {orders_filename} (ردیف {i + 1} رد شد): {row}")
            print(f"✅ سفارشات با موفقیت از {orders_filename} بارگذاری شدند!")
        except FileNotFoundError:
            print(f"❌ فایل سفارشات '{orders_filename}' یافت نشد. بدون سفارش شروع می‌شود.")
        except Exception as e:
            print(f"❌ خطای بارگذاری سفارشات: {e}")

        # بارگذاری آیتم‌های سفارش و اتصال آنها به سفارشات
        try:
            with open(order_items_filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if not row:
                        continue
                    # فرمت: order_id,product_id,quantity,price_at_time_of_order
                    if len(row) == 4:
                        try:
                            order_id, product_id, quantity_str, price_at_time_of_order_str = row
                            quantity = int(quantity_str)
                            price_at_time_of_order = float(price_at_time_of_order_str)
                            self.order_items.add_item(order_id, product_id, quantity, price_at_time_of_order)
                        except ValueError as e:
                            print(f"⚠️ خطای تجزیه داده‌های آیتم سفارش در ردیف {i + 1}: {row}. خطا: {e}")
                        except Exception as e:
                            print(f"⚠️ خطای غیرمنتظره در بارگذاری آیتم سفارش در ردیف {i + 1}: {e}")
                    else:
                        print(f"⚠️ فرمت خط نامعتبر در {order_items_filename} (ردیف {i + 1} رد شد): {row}")
            print(f"✅ آیتم‌های سفارش با موفقیت از {order_items_filename} بارگذاری شدند!")

            # اکنون، محصولات_در_سفارش را برای هر شیء سفارش پر می‌کند
            for order in self.orders:
                order_id = order.get_order_id()
                items_for_this_order = []
                for (oid, pid), item_data in self.order_items.get_all_items().items():
                    if oid == order_id:
                        items_for_this_order.append({
                            'product_id': pid,
                            'quantity': item_data['quantity'],
                            'price': item_data['value']  # 'value' از orderitems قیمت در زمان سفارش است
                        })
                order.products_in_order = items_for_this_order  # لیست محصولات شیء سفارش را به روز می‌کند

        except FileNotFoundError:
            print(f"❌ فایل آیتم‌های سفارش '{order_items_filename}' یافت نشد. هیچ آیتمی برای سفارشات بارگذاری نشد.")
        except Exception as e:
            print(f"❌ خطای بارگذاری آیتم‌های سفارش: {e}")

    def save_orders_to_csv(self, orders_filename, order_items_filename):
        try:
            with open(orders_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for order in self.orders:
                    writer.writerow(
                        [order.get_order_id(), order.get_username(), order.get_total_price(), order.get_order_date()])
            print(f"✅ سفارشات با موفقیت در {orders_filename} ذخیره شدند!")

            with open(order_items_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for (order_id, product_id), item_data in self.order_items.get_all_items().items():
                    writer.writerow([order_id, product_id, item_data['quantity'], item_data['value']])
            print(f"✅ آیتم‌های سفارش با موفقیت در {order_items_filename} ذخیره شدند!")

        except Exception as e:
            print(f"❌ خطای ذخیره سفارشات یا آیتم‌های سفارش: {e}")

    # ------------------------- منطق اصلی ----------------------------
    def login(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            print(f"✅ ورود موفقیت‌آمیز برای {username}")
            return user
        print("❌ نام کاربری یا رمز عبور نامعتبر است")
        return None

    def place_order(self, username, cart_items, order_id=None):
        user = self.users.get(username)
        if not user:
            return "خطا: کاربر یافت نشد."

        if not cart_items:
            return "خطا: سبد خرید خالی است."

        products_for_order = []
        total_order_price = 0

        # اعتبارسنجی محصولات و تعداد، و محاسبه قیمت کل
        for item in cart_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')

            if not product_id or not quantity or quantity <= 0:
                return "خطا: محصول یا تعداد نامعتبر در سبد خرید."

            product = self.products.get(product_id)
            if not product:
                return f"خطا: محصول با ID {product_id} یافت نشد."

            if product.stock < quantity:
                return f"خطا: موجودی کافی برای {product.name} (ID: {product_id}) وجود ندارد. موجود: {product.stock}"

            products_for_order.append({
                'product_id': product.id,
                'quantity': quantity,
                'price': product.price  # استفاده از قیمت فعلی محصول
            })
            total_order_price += quantity * product.price

        if user.balance < total_order_price:
            return f"خطا: موجودی ناکافی. موجودی شما: {user.balance}، مجموع سفارش: {total_order_price}"

        # کسر موجودی و به روز رسانی موجودی کاربر
        for item in products_for_order:
            product = self.products.get(item['product_id'])
            try:
                product.buy(item['quantity'])
            except ValueError as e:
                # این حالت نباید رخ دهد اگر بررسی موجودی موفق باشد، اما برای پایداری خوب است
                return f"خطا در پردازش سفارش: {e}"

        user.buying(total_order_price)

        # تولید ID سفارش اگر ارائه نشده باشد (برای سفارشات جدید)
        if order_id is None:
            # تولید ID ساده و منحصر به فرد؛ در برنامه‌های واقعی UUID برای پایداری توصیه می‌شود
            new_order_id_num = len(self.orders) + 1
            generated_order_id = f"ORD{new_order_id_num}"
            # Ensure uniqueness
            while any(o.get_order_id() == generated_order_id for o in self.orders):
                new_order_id_num += 1
                generated_order_id = f"ORD{new_order_id_num}"
            order_id = generated_order_id

        # ایجاد شیء سفارش
        new_order = Order(username, products_for_order, order_id)
        self.orders.append(new_order)

        # افزودن آیتم‌ها به OrderItemsManager
        for item in products_for_order:
            self.order_items.add_item(order_id, item['product_id'], item['quantity'], item['price'])

        # ذخیره تمام تغییرات
        self.save_products_to_csv('products.txt')
        self.save_users_to_csv('users.txt')
        self.save_orders_to_csv('orders.txt', 'order_items.txt')

        return f"سفارش {order_id} با موفقیت ثبت شد! مجموع: {total_order_price}. موجودی جدید شما: {user.balance}"