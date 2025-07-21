class User:
    def __init__(self, username, password, balance, role):
        self.username = username        # نام کاربری
        self.password = password        # رمز عبور
        self.balance = float(balance)   # موجودی حساب به صورت عدد اعشاری
        self.role = role                # نقش کاربر (customer یا admin)

    def check_password(self, password):
        # بررسی درستی رمز عبور وارد شده
        return self.password == password

    def is_customer(self):
        # بررسی اینکه آیا نقش کاربر "مشتری" است
        return self.role == 'customer'

    def is_admin(self):
        # بررسی اینکه آیا نقش کاربر "مدیر" است
        return self.role == 'admin'

    def buying(self, total):
        # کم کردن مبلغ خرید از موجودی کاربر
        self.balance -= total
