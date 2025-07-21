class Product:
    def __init__(self, id, name, price, stock, category):
        # سازنده: مشخصات یک محصول را هنگام ایجاد آن تنظیم می‌کند.
        self.id = id
        # شناسه‌ی منحصر به فرد محصول.
        self.name = name
        # نام محصول.
        self.price = price
        # قیمت واحد محصول.
        self.stock = stock
        # تعداد موجودی فعلی محصول در انبار.
        self.category = category
        # دسته‌بندی محصول (مثلاً الکترونیک، لباس و غیره).

    def updatePrice(self, newPrice):
      # متدی برای به‌روزرسانی قیمت محصول.
      if newPrice > 0:
        self.price = newPrice
        # قیمت محصول را با قیمت جدید به‌روز می‌کند.
      else:
        raise ValueError("Price is not positive.")
        # اگر قیمت جدید مثبت نباشد، خطا می‌دهد.

    def getPrice(self):
      # متدی برای دریافت قیمت فعلی محصول.
      return self.price
      # قیمت محصول را برمی‌گرداند.

    def getId(self):
      # متدی برای دریافت شناسه‌ی محصول.
      return self.id
      # شناسه‌ی محصول را برمی‌گرداند.

    def addStock(self, quantity):
      # متدی برای اضافه کردن موجودی به انبار.
      if 0 < quantity:
        self.stock += quantity
        # تعداد مشخص شده را به موجودی اضافه می‌کند.
      else:
        raise ValueError("Stock is not positive.")
        # اگر تعداد اضافه شده مثبت نباشد، خطا می‌دهد.

    def buy(self, quantity):
      # متدی برای خرید محصول و کسر از موجودی.
      if self.stock >= quantity:
        self.stock -= quantity
        # اگر موجودی کافی باشد، تعداد خریداری شده را از آن کم می‌کند.
      else:
        raise ValueError("Stock is not enough.")
        # اگر موجودی کافی نباشد، خطا می‌دهد.

    def getCategory(self):
      # متدی برای دریافت دسته‌بندی محصول.
      return self.category
      # دسته‌بندی محصول را برمی‌گرداند.

    def getName(self):
      # متدی برای دریافت نام محصول.
      return self.name
      # نام محصول را برمی‌گرداند.

    def __str__(self): # Changed from str to __str__ for correct Python magic method
        # متدی که نمایانگر رشته‌ای از شیء محصول است.
        # این متد هنگام پرینت کردن شیء به صورت مستقیم فراخوانی می‌شود.
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock}, category='{self.category}')"