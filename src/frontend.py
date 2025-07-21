import tkinter as tk
from tkinter import ttk, messagebox
from User import User
from Product import Product
from orderitems import OrderItemsManager
from Order import Order
from app import StoreApp

# ایجاد یک نمونه از StoreApp
storeapp = StoreApp()


# ---------- GUI START ----------
class StoreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("فروشگاه آنلاین")  # عنوان پنجره به فارسی
        self.current_user = None
        self.cart = {}  # سبد خرید: {'product_id': quantity}

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")  # رنگ پس‌زمینه فریم‌ها
        self.style.configure("TLabel", font=("B Nazanin", 12))  # فونت برای لیبل‌ها
        self.style.configure("TButton", font=("B Nazanin", 12, "bold"))  # فونت برای دکمه‌ها
        self.style.configure("Treeview.Heading", font=("B Nazanin", 12, "bold"))  # فونت برای سربرگ Treeview
        self.style.configure("Treeview", font=("B Nazanin", 10))  # فونت برای محتوای Treeview

        self.build_login_ui()

    def build_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("400x300")
        self.root.resizable(False, False)  # غیرفعال کردن تغییر اندازه پنجره ورود

        # استفاده از Frame برای چیدمان بهتر
        login_frame = ttk.Frame(self.root, padding="20 20 20 20")
        login_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(login_frame, text="به فروشگاه آنلاین خوش آمدید!").pack(pady=(10, 20))

        ttk.Label(login_frame, text="نام کاربری:").pack(pady=2)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=2)

        ttk.Label(login_frame, text="رمز عبور:").pack(pady=2)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.pack(pady=2)

        ttk.Button(login_frame, text="ورود", command=self.handle_login).pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = storeapp.login(username, password)  #

        if user:
            self.current_user = user
            self.cart = {}  # سبد خرید را هنگام ورود کاربر جدید پاک می‌کنیم
            if user.is_admin():  #
                self.build_admin_ui()
            else:
                self.build_customer_ui()
        else:
            messagebox.showerror("خطا در ورود", "نام کاربری یا رمز عبور اشتباه است.")  # پیام فارسی

    def build_customer_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("850x650")  # اندازه بزرگتر برای نمایش محصولات و سبد خرید
        self.root.resizable(True, True)  # فعال کردن تغییر اندازه برای صفحه مشتری

        customer_frame = ttk.Frame(self.root, padding="15 15 15 15")
        customer_frame.pack(expand=True, fill=tk.BOTH)

        # اطلاعات کاربر و موجودی
        user_info_frame = ttk.Frame(customer_frame)
        user_info_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(user_info_frame, text=f"خوش آمدید، {self.current_user.username}!").pack(side=tk.RIGHT, padx=10)

        # به‌روزرسانی موجودی کاربر از آخرین وضعیت
        updated_user = storeapp.users.get(self.current_user.username)
        if updated_user:
            self.current_user.balance = updated_user.balance
        self.balance_label = ttk.Label(user_info_frame, text=f"موجودی شما: {self.current_user.balance} تومان")
        self.balance_label.pack(side=tk.LEFT, padx=10)

        # فریم برای لیست محصولات و سبد خرید
        main_content_frame = ttk.Frame(customer_frame)
        main_content_frame.pack(fill=tk.BOTH, expand=True)
        main_content_frame.columnconfigure(0, weight=3)  # وزن بیشتر برای لیست محصولات
        main_content_frame.columnconfigure(1, weight=1)  # وزن کمتر برای سبد خرید
        main_content_frame.rowconfigure(0, weight=1)

        # لیست محصولات
        products_panel = ttk.Frame(main_content_frame, padding="5")
        products_panel.grid(row=0, column=0, sticky=tk.NSEW)

        ttk.Label(products_panel, text="لیست محصولات موجود:").pack(pady=(0, 5))

        # بخش فیلتر و جستجو
        filter_search_frame = ttk.Frame(products_panel)
        filter_search_frame.pack(fill=tk.X, pady=(0, 5))

        # فیلتر دسته‌بندی
        ttk.Label(filter_search_frame, text="فیلتر بر اساس دسته‌بندی:").pack(side=tk.RIGHT, padx=(10, 5))
        self.category_filter_combobox = ttk.Combobox(filter_search_frame, state="readonly", width=20)
        self.category_filter_combobox.pack(side=tk.RIGHT, padx=(0, 10))
        self.category_filter_combobox.bind("<<ComboboxSelected>>", self.apply_category_filter)
        self.populate_category_filter()  # پر کردن گزینه‌های دسته‌بندی

        # بخش جستجو
        self.search_entry = ttk.Entry(filter_search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(filter_search_frame, text="جستجو", command=self.apply_search_and_filter).pack(side=tk.LEFT,
                                                                                                 padx=(0, 5))
        ttk.Button(filter_search_frame, text="پاک کردن جستجو", command=self.clear_search).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(products_panel, columns=("ID", "Name", "Price", "Stock"), show="headings")
        self.tree.heading("ID", text="شناسه محصول", anchor=tk.W)
        self.tree.heading("Name", text="نام محصول", anchor=tk.W)
        self.tree.heading("Price", text="قیمت (تومان)", anchor=tk.W)
        self.tree.heading("Stock", text="موجودی", anchor=tk.W)

        # تنظیم عرض ستون‌ها و قابلیت تغییر اندازه
        self.tree.column("ID", width=100, minwidth=80, stretch=tk.NO)
        self.tree.column("Name", width=200, minwidth=150, stretch=tk.YES)
        self.tree.column("Price", width=150, minwidth=100, stretch=tk.NO)
        self.tree.column("Stock", width=80, minwidth=60, stretch=tk.NO)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.load_products_into_treeview()  # بارگذاری اولیه محصولات

        # بخش افزودن به سبد خرید
        add_to_cart_frame = ttk.LabelFrame(products_panel, text="افزودن به سبد خرید", padding="10 10 10 10")
        add_to_cart_frame.pack(fill=tk.X, pady=10)

        add_to_cart_frame.columnconfigure(0, weight=1)
        add_to_cart_frame.columnconfigure(1, weight=3)

        ttk.Label(add_to_cart_frame, text="شناسه محصول:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.product_id_entry = ttk.Entry(add_to_cart_frame, width=20)
        self.product_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(add_to_cart_frame, text="تعداد:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantity_entry = ttk.Entry(add_to_cart_frame, width=20)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Button(add_to_cart_frame, text="افزودن به سبد خرید", command=self.add_to_cart).grid(row=2, column=0,
                                                                                                columnspan=2, pady=10)

        # سبد خرید
        cart_panel = ttk.Frame(main_content_frame, padding="5", relief=tk.GROOVE, borderwidth=2)
        cart_panel.grid(row=0, column=1, sticky=tk.NSEW, padx=(15, 0))  # اضافه کردن padx برای فاصله

        ttk.Label(cart_panel, text="سبد خرید شما:").pack(pady=(0, 5))

        self.cart_tree = ttk.Treeview(cart_panel, columns=("Name", "Quantity", "Price"), show="headings")
        self.cart_tree.heading("Name", text="نام محصول", anchor=tk.W)
        self.cart_tree.heading("Quantity", text="تعداد", anchor=tk.W)
        self.cart_tree.heading("Price", text="قیمت واحد", anchor=tk.W)

        self.cart_tree.column("Name", width=100, minwidth=80, stretch=tk.YES)
        self.cart_tree.column("Quantity", width=50, minwidth=40, stretch=tk.NO)
        self.cart_tree.column("Price", width=80, minwidth=60, stretch=tk.NO)
        self.cart_tree.pack(pady=5, fill=tk.BOTH, expand=True)

        self.cart_total_label = ttk.Label(cart_panel, text="جمع کل: 0 تومان", font=("B Nazanin", 12, "bold"))
        self.cart_total_label.pack(pady=(10, 5))

        ttk.Button(cart_panel, text="تکمیل خرید", command=self.checkout).pack(pady=5)
        self.update_cart_display()  # نمایش اولیه سبد خرید

        # دکمه خروج
        ttk.Button(customer_frame, text="خروج", command=self.build_login_ui).pack(pady=10)

    def populate_category_filter(self):
        categories = sorted(list(set(p.category for p in storeapp.products.values())))
        categories.insert(0, "همه دسته‌بندی‌ها")  # اضافه کردن گزینه "همه" به ابتدای لیست
        self.category_filter_combobox['values'] = categories
        self.category_filter_combobox.set("همه دسته‌بندی‌ها")  # تنظیم مقدار پیش‌فرض

    def apply_category_filter(self, event=None):
        self.apply_search_and_filter()

    def apply_search_and_filter(self):
        selected_category = self.category_filter_combobox.get()
        search_query = self.search_entry.get().strip().lower()
        self.load_products_into_treeview(category_filter=selected_category, search_query=search_query)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.apply_search_and_filter()

    def load_products_into_treeview(self, category_filter=None, search_query=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        products_to_display = []
        for product_id, product in storeapp.products.items():
            # اعمال فیلتر دسته‌بندی
            if category_filter and category_filter != "همه دسته‌بندی‌ها" and product.category != category_filter:
                continue

            # اعمال فیلتر جستجو
            if search_query:
                if not (search_query in product.id.lower() or
                        search_query in product.name.lower() or
                        search_query in product.category.lower()):
                    continue

            products_to_display.append(product)

        for product in products_to_display:
            self.tree.insert("", "end", iid=product.id, values=(product.id, product.name, product.price, product.stock))

    def add_to_cart(self):
        pid = self.product_id_entry.get().strip()
        try:
            qty = int(self.quantity_entry.get())
            if qty <= 0:
                raise ValueError("تعداد باید مثبت باشد.")
        except ValueError as e:
            messagebox.showerror("خطا در ورودی", f"تعداد نامعتبر است: {e}")
            return

        product = storeapp.products.get(pid)
        if not product:
            messagebox.showerror("خطا", f"محصول با شناسه {pid} یافت نشد.")
            return

        # بررسی موجودی کافی (شامل مقادیر موجود در سبد خرید)
        current_cart_qty = self.cart.get(pid, 0)
        if product.stock < (current_cart_qty + qty):
            messagebox.showerror("خطا", f"موجودی کافی برای {product.name} (موجود: {product.stock}) وجود ندارد.")
            return

        self.cart[pid] = self.cart.get(pid, 0) + qty
        messagebox.showinfo("سبد خرید", f"{qty} عدد از {product.name} به سبد خرید اضافه شد.")

        self.product_id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.update_cart_display()
        # Refresh product list based on current filters
        self.load_products_into_treeview(category_filter=self.category_filter_combobox.get(),
                                         search_query=self.search_entry.get().strip().lower())

    def update_cart_display(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total_cart_price = 0
        for pid, qty in self.cart.items():
            product = storeapp.products.get(pid)
            if product:
                item_price = product.price * qty
                self.cart_tree.insert("", "end", values=(product.name, qty, product.price))
                total_cart_price += item_price

        self.cart_total_label.config(text=f"جمع کل: {total_cart_price} تومان")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("سبد خرید خالی", "سبد خرید شما خالی است. لطفا محصولی را اضافه کنید.")
            return

        # تبدیل سبد خرید به فرمت مورد نیاز place_order در app.py
        cart_items_for_order = []
        for pid, qty in self.cart.items():
            product = storeapp.products.get(pid)
            if product:
                cart_items_for_order.append({
                    'product_id': pid,
                    'quantity': qty,
                    'price': product.price  # قیمت فعلی محصول
                })

        result_message = storeapp.place_order(self.current_user.username, cart_items_for_order)
        messagebox.showinfo("نتیجه سفارش", result_message)

        # پس از موفقیت آمیز بودن سفارش
        if "با موفقیت ثبت شد" in result_message:
            self.cart.clear()  # سبد خرید را پاک می‌کنیم
            self.update_cart_display()  # نمایش سبد خرید خالی

            # رفرش کردن موجودی کاربر و لیست محصولات
            self.current_user = storeapp.users.get(self.current_user.username)
            if self.current_user:
                self.balance_label.config(text=f"موجودی شما: {self.current_user.balance} تومان")

            # Refresh product list based on current filters
            self.load_products_into_treeview(category_filter=self.category_filter_combobox.get(),
                                             search_query=self.search_entry.get().strip().lower())

    def build_admin_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("800x700")  # اندازه بزرگتر برای پنل مدیریت با تب‌ها
        self.root.resizable(True, True)

        admin_frame = ttk.Frame(self.root, padding="15 15 15 15")
        admin_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(admin_frame, text=f"پنل مدیریت، خوش آمدید {self.current_user.username}").pack(pady=(10, 10))

        # ایجاد Notebook (سیستم تب)
        self.admin_notebook = ttk.Notebook(admin_frame)
        self.admin_notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # تب مدیریت محصولات
        product_management_frame = ttk.Frame(self.admin_notebook, padding="10")
        self.admin_notebook.add(product_management_frame, text="مدیریت محصولات")

        # محتوای تب مدیریت محصولات
        ttk.Label(product_management_frame, text="لیست محصولات موجود:").pack(pady=(10, 5))
        self.admin_tree = ttk.Treeview(product_management_frame, columns=("ID", "Name", "Price", "Stock", "Category"),
                                       show="headings")
        self.admin_tree.heading("ID", text="شناسه", anchor=tk.W)
        self.admin_tree.heading("Name", text="نام", anchor=tk.W)
        self.admin_tree.heading("Price", text="قیمت", anchor=tk.W)
        self.admin_tree.heading("Stock", text="موجودی", anchor=tk.W)
        self.admin_tree.heading("Category", text="دسته‌بندی", anchor=tk.W)

        self.admin_tree.column("ID", width=80, minwidth=60, stretch=tk.NO)
        self.admin_tree.column("Name", width=150, minwidth=100, stretch=tk.YES)
        self.admin_tree.column("Price", width=100, minwidth=80, stretch=tk.NO)
        self.admin_tree.column("Stock", width=70, minwidth=50, stretch=tk.NO)
        self.admin_tree.column("Category", width=120, minwidth=90, stretch=tk.YES)
        self.admin_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.load_admin_products_into_treeview()

        add_product_frame = ttk.LabelFrame(product_management_frame, text="افزودن محصول جدید", padding="10 10 10 10")
        add_product_frame.pack(fill=tk.X, pady=10)
        add_product_frame.columnconfigure(0, weight=1)
        add_product_frame.columnconfigure(1, weight=3)

        ttk.Label(add_product_frame, text="نام محصول:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.name_entry = ttk.Entry(add_product_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(add_product_frame, text="قیمت:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.price_entry = ttk.Entry(add_product_frame, width=40)
        self.price_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(add_product_frame, text="موجودی:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.stock_entry = ttk.Entry(add_product_frame, width=40)
        self.stock_entry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(add_product_frame, text="دسته‌بندی:").grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        self.cat_entry = ttk.Entry(add_product_frame, width=40)
        self.cat_entry.grid(row=3, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Button(add_product_frame, text="افزودن محصول", command=self.add_product).grid(row=4, column=0, columnspan=2,
                                                                                          pady=15)

        # تب مشاهده سفارشات
        order_management_frame = ttk.Frame(self.admin_notebook, padding="10")
        self.admin_notebook.add(order_management_frame, text="مشاهده سفارشات")
        self.build_order_management_tab(order_management_frame)  # ایجاد محتوای تب مدیریت سفارش

        # دکمه خروج
        ttk.Button(admin_frame, text="خروج", command=self.build_login_ui).pack(pady=10)

    def load_admin_products_into_treeview(self):
        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)
        for product_id, product in storeapp.products.items():
            self.admin_tree.insert("", "end", iid=product.id,
                                   values=(product.id, product.name, product.price, product.stock, product.category))  #

    def add_product(self):
        try:
            name = self.name_entry.get().strip()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
            category = self.cat_entry.get().strip()

            if not name or price <= 0 or stock <= 0 or not category:
                raise ValueError("لطفا تمام فیلدها را به درستی پر کنید (مقادیر مثبت برای قیمت و موجودی).")
        except ValueError as e:
            messagebox.showerror("خطا در ورودی", f"ورودی نامعتبر: {e}")
            return

        # تولید Product ID ساده (در یک سیستم واقعی ممکن است قوی‌تر باشد)
        # مطمئن می‌شویم که ID تکراری نباشد
        new_product_id_num = len(storeapp.products) + 1
        new_product_id = f"P{new_product_id_num}"
        while new_product_id in storeapp.products:
            new_product_id_num += 1
            new_product_id = f"P{new_product_id_num}"

        new_product = Product(new_product_id, name, price, stock, category)  #
        if storeapp.add_product(new_product):
            messagebox.showinfo("موفقیت", f"محصول {name} با موفقیت اضافه شد.")
            # پاک کردن فیلدها
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.stock_entry.delete(0, tk.END)
            self.cat_entry.delete(0, tk.END)
            self.load_admin_products_into_treeview()  # به‌روزرسانی لیست محصولات مدیر
        else:
            messagebox.showerror("خطا", f"افزودن محصول {name} با مشکل مواجه شد.")

    def build_order_management_tab(self, parent_frame):
        ttk.Label(parent_frame, text="لیست سفارشات:").pack(pady=(10, 5))
        self.orders_tree = ttk.Treeview(parent_frame, columns=("OrderID", "Username", "TotalPrice", "OrderDate"),
                                        show="headings")
        self.orders_tree.heading("OrderID", text="شناسه سفارش", anchor=tk.W)
        self.orders_tree.heading("Username", text="نام کاربری خریدار", anchor=tk.W)
        self.orders_tree.heading("TotalPrice", text="مبلغ کل (تومان)", anchor=tk.W)
        self.orders_tree.heading("OrderDate", text="تاریخ سفارش", anchor=tk.W)

        self.orders_tree.column("OrderID", width=120, minwidth=100, stretch=tk.NO)
        self.orders_tree.column("Username", width=120, minwidth=100, stretch=tk.NO)
        self.orders_tree.column("TotalPrice", width=150, minwidth=100, stretch=tk.NO)
        self.orders_tree.column("OrderDate", width=120, minwidth=100, stretch=tk.NO)

        self.orders_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.orders_tree.bind("<<TreeviewSelect>>", self.on_order_select)

        ttk.Label(parent_frame, text="جزئیات آیتم‌های سفارش:").pack(pady=(10, 5))
        self.order_items_tree = ttk.Treeview(parent_frame,
                                             columns=("ProductID", "ProductName", "Quantity", "PriceAtOrder"),
                                             show="headings")
        self.order_items_tree.heading("ProductID", text="شناسه محصول", anchor=tk.W)
        self.order_items_tree.heading("ProductName", text="نام محصول", anchor=tk.W)
        self.order_items_tree.heading("Quantity", text="تعداد", anchor=tk.W)
        self.order_items_tree.heading("PriceAtOrder", text="قیمت واحد در زمان سفارش", anchor=tk.W)

        self.order_items_tree.column("ProductID", width=100, minwidth=80, stretch=tk.NO)
        self.order_items_tree.column("ProductName", width=200, minwidth=150, stretch=tk.YES)
        self.order_items_tree.column("Quantity", width=80, minwidth=60, stretch=tk.NO)
        self.order_items_tree.column("PriceAtOrder", width=150, minwidth=100, stretch=tk.NO)

        self.order_items_tree.pack(pady=5, fill=tk.BOTH, expand=True)

        self.load_orders_into_orders_treeview()  # بارگذاری سفارشات هنگام ساخت تب

    def load_orders_into_orders_treeview(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        # مطمئن شوید که storeapp.orders قبل از بارگذاری به روز است (هرچند با ذخیره خودکار اینطور است)
        storeapp.load_orders_from_csv('orders.csv.txt', 'order_items.csv.txt')
        for order in storeapp.orders:
            self.orders_tree.insert("", "end", iid=order.get_order_id(),
                                    values=(order.get_order_id(), order.get_username(),
                                            order.get_total_price(), order.get_order_date()))

    def on_order_select(self, event):
        for item in self.order_items_tree.get_children():
            self.order_items_tree.delete(item)

        selected_item = self.orders_tree.focus()
        if not selected_item:
            return

        order_id = self.orders_tree.item(selected_item, "iid")

        # آیتم‌های سفارش را از OrderItemsManager بارگذاری کنید
        # order_items_manager = storeapp.order_items # این قبلا به عنوان self.order_items در storeapp ایجاد شده است

        items_for_selected_order = []
        for (oid, pid), item_data in storeapp.order_items.get_all_items().items():
            if oid == order_id:
                items_for_selected_order.append({
                    'product_id': pid,
                    'quantity': item_data['quantity'],
                    'price_at_order': item_data['value']
                })

        for item in items_for_selected_order:
            product_id = item['product_id']
            quantity = item['quantity']
            price_at_order = item['price_at_order']

            product_name = "ناشناخته"
            product = storeapp.products.get(product_id)
            if product:
                product_name = product.name

            self.order_items_tree.insert("", "end", values=(product_id, product_name, quantity, price_at_order))


if __name__ == "__main__":
    root = tk.Tk()
    gui = StoreGUI(root)
    root.mainloop()