class OrderItemsManager:
    def __init__(self):
        # دیکشنری برای نگهداری آیتم‌های سفارش
        self.orderitems = {}

    def add_item(self, order_id, product_id, quantity, value):
        # افزودن یا بروزرسانی یک آیتم سفارش
        self.orderitems[(order_id, product_id)] = {
            'quantity': quantity,
            'value': value
        }

    def get_item(self, order_id, product_id):
        # دریافت یک آیتم خاص از روی شناسه سفارش و کالا
        return self.orderitems.get((order_id, product_id))

    def remove_item(self, order_id, product_id):
        # حذف یک آیتم از سفارش
        key = (order_id, product_id)
        if key in self.orderitems:
            del self.orderitems[key]

    def get_all_items(self):
        # گرفتن همه آیتم‌ها
        return self.orderitems

    def get_total_price(self, order_id):
        # محاسبه مجموع قیمت یک سفارش خاص
        total = 0
        for (oid, _), item in self.orderitems.items():
            if oid == order_id:
                total += item['quantity'] * item['value']
        return total
