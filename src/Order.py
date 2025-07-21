import datetime  # برای استفاده از تاریخ


class Order:
    def __init__(self, username, products_in_order, order_id=None):  # order_id اضافه شد
        # سازنده: مشخصات یک سفارش را هنگام ایجاد آن تنظیم می‌کند.
        # یک سفارش می‌تواند شامل چندین محصول باشد.

        self.username = username
        # نام کاربری خریدار این سفارش.

        self.products_in_order = products_in_order
        # لیستی از محصولات موجود در این سفارش.
        # هر آیتم در این لیست باید یک دیکشنری باشد شامل 'product_id', 'quantity' و 'price'.
        # مثال: [{'product_id': 'P001', 'quantity': 2, 'price': 50000}, ...]

        self.total_price = self._calculate_total_price()
        # قیمت کل سفارش که به صورت خودکار محاسبه می‌شود.

        self.order_date = datetime.date.today()
        # تاریخ ثبت سفارش (به صورت خودکار تاریخ امروز را قرار می‌دهد).

        self.order_id = order_id if order_id is not None else self._generate_unique_order_id()  # اختصاص یا تولید

    def _calculate_total_price(self):
        # متد داخلی برای محاسبه قیمت کل سفارش.
        # این متد تمام اقلام سفارش را جمع می‌کند.
        calculated_total = 0
        for item in self.products_in_order:
            # انتظار داریم هر 'item' یک دیکشنری با کلیدهای 'quantity' و 'price' باشد.
            quantity = item.get('quantity', 0)  # اگر 'quantity' نباشد، 0 در نظر گرفته می‌شود.
            price = item.get('price', 0)  # اگر 'price' نباشد، 0 در نظر گرفته می‌شود.
            calculated_total += quantity * price
        return calculated_total

    def _generate_unique_order_id(self):
        # در یک برنامه واقعی، این از یک روش قوی‌تر برای تولید ID استفاده می‌کند
        # مانند UUID یا یک شمارنده پایدار. برای سادگی، فعلاً از رویکرد مبتنی بر زمان استفاده می‌کنیم.
        return f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    def get_username(self):
        # متدی برای دریافت نام کاربری خریدار سفارش.
        return self.username

    def get_products_in_order(self):
        # متدی برای دریافت لیست محصولات و اطلاعاتشان در این سفارش.
        return self.products_in_order

    def get_total_price(self):
        # متدی برای دریافت قیمت کل سفارش.
        return self.total_price

    def get_order_date(self):
        # متدی برای دریافت تاریخ ثبت سفارش.
        return self.order_date

    def get_order_id(self):  # متد جدید برای دریافت order_id
        return self.order_id

    def display_order_info(self):
        # نمایش جزئیات کامل سفارش.
        print(f"سفارش ID: {self.order_id}")  # نمایش ID سفارش
        print(f"سفارش برای کاربر: {self.username}")
        print(f"تاریخ سفارش: {self.order_date}")
        print("محصولات سفارش داده شده:")
        for item in self.products_in_order:
            product_id = item.get('product_id', 'نامشخص')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            print(f"  - ID: {product_id}, تعداد: {quantity}, قیمت واحد: {price} تومان")
        print(f"قیمت کل سفارش: {self.total_price} تومان")

    def __str__(self):
        return f"Order(id='{self.order_id}', username='{self.username}', total_price={self.total_price}, date={self.order_date})"