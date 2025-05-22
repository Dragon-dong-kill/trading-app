import tkinter as tk  
from tkinter import ttk, messagebox, scrolledtext  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  
import pandas as pd  
import numpy as np  
from datetime import datetime, timedelta  
import requests  
import threading  
import traceback  
import json  
import os  
from tkcalendar import DateEntry  
import matplotlib.dates as mdates  
from PIL import Image, ImageTk  
import pickle  

# 数据源库 - 名称到URL的映射  
DATA_SOURCES = {  
    "AK47 | 血腥运动": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=553370749&platform=YOUPIN&specialStyle",  
    "蝴蝶刀": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=22779&platform=YOUPIN&specialStyle",  
    "树篱迷宫": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=525873303&platform=YOUPIN&specialStyle",  
    "水栽竹": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=24283&platform=YOUPIN&specialStyle",  
    "怪兽在b": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=1315999843394654208&platform=YOUPIN&specialStyle",  
    "金刚犬": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=1315844312734502912&platform=YOUPIN&specialStyle",  
    "tyloo": "https://sdt-api.ok-skins.com/user/steam/category/v1/kline?timestamp={}&type=2&maxTime={}&typeVal=925497374167523328&platform=YOUPIN&specialStyle",  
}  

# 数据源对应的图片URLs (示例)  
ITEM_IMAGES = {  
    "AK47 | 血腥运动": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot7HxfDhjxszJemkV09-5lpKKqPrxN7LEmyVQ7MEpiLuSrYmnjQO3-UdsZGHyd4_Bd1RvNQ7T_FDrw-_ng5Pu75iY1zI97bhLsvQz/360fx360f",  
    "蝴蝶刀": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpovbSsLQJf0ebcZThQ6tCvq4GGqPP7I6vdk3lu-M1wmeyQyoD8j1yg5Rc5YDz2I4OScwJsZ1-G_wC3lefsjJa4uJXLnSBl7nI8pSGK_UPjcSw/360fx360f",  
    "树篱迷宫": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhnwMzFJTwW09--m5CbkuXLNLPehW5V18l4jeHVu9qg3Ffj-RJtajjzJoKUdQZoN1HS-ge9l7jqjZ-87pnMzHBg7CVw7S3D30vgNL-dAwU/360fx360f",  
    "水栽竹": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhnwMzFJTwW09-vloWZh-zlN7iJlD9V7cAl2eyVpIrz2FKx_RFuYmmmdYfDdAY2YVmC-AO4xb3u1JG-7sinJwOE8GY/360fx360f",  
    "怪兽在b": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgposLuoKhRf0Ob3dzxP7c-JmIWFg_bLP7LWnn9u5MRjjeyPoo333QPs_xBpZj-iIdfBcVA4ZlnRqwW2lb28jcO87ZzNwXNqs3Fw5WGdwULkJ8pNJw/360fx360f",  
    "金刚犬": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpotLu8JAllx8zJfAJG48ymmIWZqOf8MqjUxFRd4cJ5ntbN9J7yjRrhrUFuamD1LICde1Q4YQ2F_wO_xue908K86szJzHZl63Uj-z-DyN2AYCdJ/360fx360f",  
    "tyloo": "https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopamie19f0Ob3Yi5FvISJkJKKkPj6NbLDk1RC68phj9bN_Iv9nGu4qgE7Nnf1I4CcIVA8MF2F_lm-kL3qh8K-vJucm3IxpGB8ss6c2YdO/360fx360f"  
}  

# 从您的代码复制过来的函数  
def get_kline(url, start_date=None, end_date=None):  
    """爬取网站K线数据（保持原始结构，增加时间范围筛选）"""  
    kline_ls = []  
    
    # 处理时间范围  
    end_ts = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp()) if end_date else int(datetime.now().timestamp())  
    start_ts = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp()) if start_date else 0  
    
    while 1:  
        ts = int(datetime.now().timestamp() * 1000)  
        try:  
            data = requests.get(url.format(ts, end_ts)).json()['data']  
            
            if len(data) == 0:  
                break  
                
            kline_ls += data  
            end_ts = int(data[0][0]) - 86400  
            
            if start_date and end_ts < start_ts:  
                break  
        except Exception as e:  
            print(f"Error fetching data: {e}")  
            break  
    
    if not kline_ls:  
        return pd.DataFrame(columns=['close']).set_index('date')  
        
    kline_df = pd.DataFrame(kline_ls)[[0, 2]]  
    kline_df.columns = ['date', 'close']  
    kline_df['date'] = kline_df['date'].apply(lambda x: datetime.fromtimestamp(int(x)))  
    
    if start_date or end_date:  
        mask = True  
        if start_date:  
            mask = mask & (kline_df['date'] >= datetime.strptime(start_date, '%Y-%m-%d'))  
        if end_date:  
            mask = mask & (kline_df['date'] <= datetime.strptime(end_date, '%Y-%m-%d'))  
        kline_df = kline_df[mask]  
    
    return kline_df.set_index('date')[['close']].sort_index()  

# 交易物品类  
class TradingItem:  
    def __init__(self, name, price, quantity=1, purchase_date=None):  
        self.name = name  
        self.purchase_price = price  
        self.quantity = quantity  
        self.purchase_date = purchase_date or datetime.now()  
        self.cooldown_end_date = self.purchase_date + timedelta(days=7)  
    
    def is_tradable(self):  
        return datetime.now() >= self.cooldown_end_date  
    
    def remaining_cooldown_days(self):  
        if self.is_tradable():  
            return 0  
        else:  
            delta = self.cooldown_end_date - datetime.now()  
            return max(0, delta.days + (1 if delta.seconds > 0 else 0))  
    
    def to_dict(self):  
        return {  
            'name': self.name,  
            'purchase_price': self.purchase_price,  
            'quantity': self.quantity,  
            'purchase_date': self.purchase_date.isoformat(),  
            'cooldown_end_date': self.cooldown_end_date.isoformat()  
        }  
    
    @classmethod  
    def from_dict(cls, data):  
        item = cls(  
            name=data['name'],  
            price=data['purchase_price'],  
            quantity=data['quantity'],  
            purchase_date=datetime.fromisoformat(data['purchase_date'])  
        )  
        item.cooldown_end_date = datetime.fromisoformat(data['cooldown_end_date'])  
        return item  

# 用户类  
class User:  
    def __init__(self, username, password, balance=100000.0):  
        self.username = username  
        self.password = password  # 实际应用中应该加密存储  
        self.balance = balance  
        self.inventory = []  # 存储 TradingItem 对象  
        self.transaction_history = []  # 存储交易历史  
    
    def add_to_inventory(self, item):  
        if len(self.inventory) >= 1000:  
            return False, "库存已满，最多只能存储1000个物品"  
        self.inventory.append(item)  
        return True, "成功添加到库存"  
    
    def remove_from_inventory(self, item_index):  
        if 0 <= item_index < len(self.inventory):  
            item = self.inventory.pop(item_index)  
            return True, item  
        return False, "物品不存在"  
    
    def buy_item(self, item_name, current_price, quantity=1):  
        total_cost = current_price * quantity  
        
        if self.balance < total_cost:  
            return False, "余额不足"  
        
        self.balance -= total_cost  
        new_item = TradingItem(item_name, current_price, quantity)  
        success, message = self.add_to_inventory(new_item)  
        
        if success:  
            # 记录交易  
            transaction = {  
                'type': 'buy',  
                'item': item_name,  
                'price': current_price,  
                'quantity': quantity,  
                'date': datetime.now().isoformat(),  
                'total': total_cost  
            }  
            self.transaction_history.append(transaction)  
            return True, f"成功购买 {quantity} 个 {item_name}"  
        else:  
            # 如果添加到库存失败，退还余额  
            self.balance += total_cost  
            return False, message  
    
    def sell_item(self, item_index, current_price):  
        success, result = self.remove_from_inventory(item_index)  
        
        if not success:  
            return False, result  
        
        item = result  
        if not item.is_tradable():  
            # 将物品放回库存  
            self.inventory.insert(item_index, item)  
            return False, f"物品还在交易冷却期，剩余 {item.remaining_cooldown_days()} 天"  
        
        total_gain = current_price * item.quantity  
        self.balance += total_gain  
        
        # 记录交易  
        transaction = {  
            'type': 'sell',  
            'item': item.name,  
            'buy_price': item.purchase_price,  
            'sell_price': current_price,  
            'quantity': item.quantity,  
            'date': datetime.now().isoformat(),  
            'total': total_gain,  
            'profit': total_gain - (item.purchase_price * item.quantity)  
        }  
        self.transaction_history.append(transaction)  
        
        return True, f"成功卖出 {item.name}，获得 {total_gain:.2f}"  
    
    def to_dict(self):  
        return {  
            'username': self.username,  
            'password': self.password,  
            'balance': self.balance,  
            'inventory': [item.to_dict() for item in self.inventory],  
            'transaction_history': self.transaction_history  
        }  
    
    @classmethod  
    def from_dict(cls, data):  
        user = cls(  
            username=data['username'],  
            password=data['password'],  
            balance=data['balance']  
        )  
        user.inventory = [TradingItem.from_dict(item_data) for item_data in data['inventory']]  
        user.transaction_history = data['transaction_history']  
        return user  

# 用户管理类  
class UserManager:  
    def __init__(self, data_file='users.json'):  
        self.data_file = data_file  
        self.users = {}  
        self.current_user = None  
        self.load_users()  
    
    def load_users(self):  
        try:  
            if os.path.exists(self.data_file):  
                with open(self.data_file, 'r', encoding='utf-8') as f:  
                    data = json.load(f)  
                    for username, user_data in data.items():  
                        self.users[username] = User.from_dict(user_data)  
        except Exception as e:  
            print(f"加载用户数据失败: {e}")  
    
    def save_users(self):  
        try:  
            data = {username: user.to_dict() for username, user in self.users.items()}  
            with open(self.data_file, 'w', encoding='utf-8') as f:  
                json.dump(data, f, ensure_ascii=False, indent=2)  
        except Exception as e:  
            print(f"保存用户数据失败: {e}")  
    
    def register(self, username, password):  
        if username in self.users:  
            return False, "用户名已存在"  
        
        self.users[username] = User(username, password)  
        self.save_users()  
        return True, "注册成功"  
    
    def login(self, username, password):  
        if username not in self.users:  
            return False, "用户不存在"  
        
        user = self.users[username]  
        if user.password != password:  
            return False, "密码错误"  
        
        self.current_user = user  
        return True, "登录成功"  
    
    def logout(self):  
        self.current_user = None  
        return True, "已登出"  

# 主应用类  
class CSGOTradingApp:  
    def __init__(self, root):  
        self.root = root  
        self.root.title("CSGO皮肤模拟交易系统")  
        self.root.geometry("1200x800")  
        self.root.minsize(1000, 700)  
        
        # 初始化用户管理  
        self.user_manager = UserManager()  
        
        # 创建菜单栏  
        self.create_menu()  
        
        # 初始化界面  
        self.current_frame = None  
        self.show_login_frame()  
        
        # 初始化数据  
        self.current_item = None  
        self.price_data = None  
        self.current_price = 0.0  
        
        # 初始化图像缓存  
        self.image_cache = {}  
    
    def create_menu(self):  
        menu_bar = tk.Menu(self.root)  
        
        file_menu = tk.Menu(menu_bar, tearoff=0)  
        file_menu.add_command(label="退出", command=self.root.quit)  
        menu_bar.add_cascade(label="文件", menu=file_menu)  
        
        if self.user_manager.current_user:  
            account_menu = tk.Menu(menu_bar, tearoff=0)  
            account_menu.add_command(label="市场", command=self.show_market_frame)  
            account_menu.add_command(label="库存", command=self.show_inventory_frame)  
            account_menu.add_command(label="交易历史", command=self.show_history_frame)  
            account_menu.add_separator()  
            account_menu.add_command(label="登出", command=self.logout)  
            menu_bar.add_cascade(label="账户", menu=account_menu)  
        
        self.root.config(menu=menu_bar)  
    
    def refresh_menu(self):  
        self.create_menu()  
    
    def clear_frame(self):  
        if self.current_frame:  
            self.current_frame.destroy()  
    
    def show_login_frame(self):  
        self.clear_frame()  
        self.current_frame = LoginFrame(self.root, self)  
        self.current_frame.pack(fill=tk.BOTH, expand=True)  
    
    def show_market_frame(self):  
        self.clear_frame()  
        self.current_frame = MarketFrame(self.root, self)  
        self.current_frame.pack(fill=tk.BOTH, expand=True)  
    
    def show_inventory_frame(self):  
        self.clear_frame()  
        self.current_frame = InventoryFrame(self.root, self)  
        self.current_frame.pack(fill=tk.BOTH, expand=True)  
    
    def show_history_frame(self):  
        self.clear_frame()  
        self.current_frame = HistoryFrame(self.root, self)  
        self.current_frame.pack(fill=tk.BOTH, expand=True)  
    
    def show_item_detail(self, item_name):  
        self.current_item = item_name  
        self.clear_frame()  
        self.current_frame = ItemDetailFrame(self.root, self, item_name)  
        self.current_frame.pack(fill=tk.BOTH, expand=True)  
    
    def login(self, username, password):  
        success, message = self.user_manager.login(username, password)  
        if success:  
            self.refresh_menu()  
            self.show_market_frame()  
        return success, message  
    
    def register(self, username, password, confirm_password):  
        if password != confirm_password:  
            return False, "两次输入的密码不一致"  
        
        return self.user_manager.register(username, password)  
    
    def logout(self):  
        self.user_manager.save_users()  # 保存用户数据  
        success, message = self.user_manager.logout()  
        if success:  
            self.refresh_menu()  
            self.show_login_frame()  
        return success, message  
    
    def get_item_image(self, item_name):  
        """获取物品图片"""  
        if item_name in self.image_cache:  
            return self.image_cache[item_name]  
        
        try:  
            if item_name in ITEM_IMAGES:  
                # 实际应用中应该异步下载图片  
                image_url = ITEM_IMAGES[item_name]  
                # 这里简化处理，返回一个占位图片  
                img = tk.PhotoImage(width=100, height=100)  
                self.image_cache[item_name] = img  
                return img  
            else:  
                # 返回默认图片  
                img = tk.PhotoImage(width=100, height=100)  
                self.image_cache[item_name] = img  
                return img  
        except Exception as e:  
            print(f"获取图片失败: {e}")  
            img = tk.PhotoImage(width=100, height=100)  
            self.image_cache[item_name] = img  
            return img  

# 登录注册界面  
class LoginFrame(tk.Frame):  
    def __init__(self, parent, controller):  
        super().__init__(parent, bg="#f5f5f5")  
        self.controller = controller  
        
        # 创建登录框  
        login_frame = tk.Frame(self, bg="white", padx=20, pady=20)  
        login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  
        
        # 标题  
        title_label = tk.Label(login_frame, text="CSGO皮肤模拟交易系统", font=("微软雅黑", 18, "bold"), bg="white")  
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))  
        
        # 用户名  
        username_label = tk.Label(login_frame, text="用户名:", font=("微软雅黑", 12), bg="white")  
        username_label.grid(row=1, column=0, sticky=tk.W, pady=5)  
        self.username_entry = tk.Entry(login_frame, font=("微软雅黑", 12), width=20)  
        self.username_entry.grid(row=1, column=1, pady=5)  
        
        # 密码  
        password_label = tk.Label(login_frame, text="密码:", font=("微软雅黑", 12), bg="white")  
        password_label.grid(row=2, column=0, sticky=tk.W, pady=5)  
        self.password_entry = tk.Entry(login_frame, font=("微软雅黑", 12), width=20, show="*")  
        self.password_entry.grid(row=2, column=1, pady=5)  
        
        # 确认密码（注册用）  
        confirm_label = tk.Label(login_frame, text="确认密码:", font=("微软雅黑", 12), bg="white")  
        confirm_label.grid(row=3, column=0, sticky=tk.W, pady=5)  
        self.confirm_entry = tk.Entry(login_frame, font=("微软雅黑", 12), width=20, show="*")  
        self.confirm_entry.grid(row=3, column=1, pady=5)  
        
        # 按钮容器  
        button_frame = tk.Frame(login_frame, bg="white")  
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)  
        
        # 登录按钮  
        login_button = tk.Button(button_frame, text="登录", font=("微软雅黑", 12),   
                                width=10, bg="#4CAF50", fg="white", command=self.login)  
        login_button.grid(row=0, column=0, padx=5)  
        
        # 注册按钮  
        register_button = tk.Button(button_frame, text="注册", font=("微软雅黑", 12),   
                                  width=10, bg="#2196F3", fg="white", command=self.register)  
        register_button.grid(row=0, column=1, padx=5)  
        
        # 信息标签  
        self.message_label = tk.Label(login_frame, text="", font=("微软雅黑", 10), bg="white", fg="red")  
        self.message_label.grid(row=5, column=0, columnspan=2, pady=10)  
    
    def login(self):  
        username = self.username_entry.get()  
        password = self.password_entry.get()  
        
        if not username or not password:  
            self.message_label.config(text="请输入用户名和密码")  
            return  
        
        success, message = self.controller.login(username, password)  
        if not success:  
            self.message_label.config(text=message)  
    
    def register(self):  
        username = self.username_entry.get()  
        password = self.password_entry.get()  
        confirm = self.confirm_entry.get()  
        
        if not username or not password or not confirm:  
            self.message_label.config(text="请完整填写所有字段")  
            return  
        
        success, message = self.controller.register(username, password, confirm)  
        if success:  
            self.message_label.config(text=message, fg="green")  
        else:  
            self.message_label.config(text=message, fg="red")  

# 市场界面  
class MarketFrame(tk.Frame):  
    def __init__(self, parent, controller):  
        super().__init__(parent)  
        self.controller = controller  
        self.user = controller.user_manager.current_user  
        
        # 创建顶部状态栏  
        self.create_status_bar()  
        
        # 创建皮肤列表  
        self.create_item_list()  
    
    def create_status_bar(self):  
        status_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=5)  
        status_frame.pack(fill=tk.X)  
        
        # 用户名和余额  
        user_label = tk.Label(status_frame, text=f"用户: {self.user.username}", font=("微软雅黑", 10), bg="#f0f0f0")  
        user_label.pack(side=tk.LEFT, padx=5)  
        
        balance_label = tk.Label(status_frame, text=f"余额: ¥{self.user.balance:.2f}", font=("微软雅黑", 10), bg="#f0f0f0")  
        balance_label.pack(side=tk.LEFT, padx=20)  
        
        # 导航按钮  
        market_btn = tk.Button(status_frame, text="市场", width=8, command=self.controller.show_market_frame)  
        market_btn.pack(side=tk.RIGHT, padx=5)  
        
        inventory_btn = tk.Button(status_frame, text="库存", width=8, command=self.controller.show_inventory_frame)  
        inventory_btn.pack(side=tk.RIGHT, padx=5)  
        
        history_btn = tk.Button(status_frame, text="交易历史", width=8, command=self.controller.show_history_frame)  
        history_btn.pack(side=tk.RIGHT, padx=5)  
    
    def create_item_list(self):  
        # 创建滚动区域  
        canvas = tk.Canvas(self, bg="#ffffff")  
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)  
        scrollable_frame = ttk.Frame(canvas)  
        
        scrollable_frame.bind(  
            "<Configure>",  
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))  
        )  
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  
        canvas.configure(yscrollcommand=scrollbar.set)  
        
        canvas.pack(side="left", fill="both", expand=True)  
        scrollbar.pack(side="right", fill="y")  
        
        # 市场标题  
        title_label = tk.Label(scrollable_frame, text="皮肤市场", font=("微软雅黑", 16, "bold"), pady=10)  
        title_label.grid(row=0, column=0, columnspan=4, sticky="w", padx=20)  
        
        # 创建皮肤卡片  
        row = 1  
        col = 0  
        for item_name, url in DATA_SOURCES.items():  
            self.create_item_card(scrollable_frame, item_name, row, col)  
            col += 1  
            if col > 3:  # 每行4个卡片  
                col = 0  
                row += 1  
    
    def create_item_card(self, parent, item_name, row, col):  
        # 加载皮肤当前价格  
        try:  
            # 在实际应用中应该异步加载价格  
            today = datetime.now().strftime('%Y-%m-%d')  
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  
            url = DATA_SOURCES[item_name]  
            df = get_kline(url, yesterday, today)  
            current_price = df['close'].iloc[-1] if not df.empty else 0  
        except Exception as e:  
            print(f"获取价格失败: {e}")  
            current_price = 0  
        
        # 创建卡片容器  
        card = tk.Frame(parent, width=250, height=300, bg="white", bd=1, relief=tk.SOLID)  
        card.grid(row=row, column=col, padx=10, pady=10)  
        card.pack_propagate(False)  # 防止内部组件改变Frame大小  
        
        # 物品图片（使用占位图）  
        img = self.controller.get_item_image(item_name)  
        img_label = tk.Label(card, image=img, bg="white")  
        img_label.image = img  # 保持引用防止垃圾回收  
        img_label.pack(pady=(20, 10))  
        
        # 物品名称  
        name_label = tk.Label(card, text=item_name, font=("微软雅黑", 12, "bold"), bg="white")  
        name_label.pack(pady=5)  
        
        # 物品价格  
        price_label = tk.Label(card, text=f"¥{current_price:.2f}", font=("微软雅黑", 12), bg="white")  
        price_label.pack(pady=5)  
        
        # 查看按钮  
        view_button = tk.Button(card, text="查看详情", width=15, bg="#2196F3", fg="white",  
                               command=lambda name=item_name: self.controller.show_item_detail(name))  
        view_button.pack(pady=10)  

# 物品详情界面  
class ItemDetailFrame(tk.Frame):  
    def __init__(self, parent, controller, item_name):  
        super().__init__(parent)  
        self.controller = controller  
        self.item_name = item_name  
        self.user = controller.user_manager.current_user  
        
        # 获取价格数据  
        self.price_data = None  
        self.current_price = 0  
        self.load_price_data()  
        
        # 创建顶部状态栏  
        self.create_status_bar()  
        
        # 创建主体内容  
        self.create_main_content()  
    
    def create_status_bar(self):  
        status_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=5)  
        status_frame.pack(fill=tk.X)  
        
        # 用户名和余额  
        user_label = tk.Label(status_frame, text=f"用户: {self.user.username}", font=("微软雅黑", 10), bg="#f0f0f0")  
        user_label.pack(side=tk.LEFT, padx=5)  
        
        balance_label = tk.Label(status_frame, text=f"余额: ¥{self.user.balance:.2f}", font=("微软雅黑", 10), bg="#f0f0f0")  
        balance_label.pack(side=tk.LEFT, padx=20)  
        
        # 导航按钮  
        market_btn = tk.Button(status_frame, text="市场", width=8, command=self.controller.show_market_frame)  
        market_btn.pack(side=tk.RIGHT, padx=5)  
        
        inventory_btn = tk.Button(status_frame, text="库存", width=8, command=self.controller.show_inventory_frame)  
        inventory_btn.pack(side=tk.RIGHT, padx=5)  
        
        history_btn = tk.Button(status_frame, text="交易历史", width=8, command=self.controller.show_history_frame)  
        history_btn.pack(side=tk.RIGHT, padx=5)  
    
    def load_price_data(self):  
        # 获取过去30天的价格数据  
        try:  
            end_date = datetime.now().strftime('%Y-%m-%d')  
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')  
            url = DATA_SOURCES.get(self.item_name)  
            
            if url:  
                self.price_data = get_kline(url, start_date, end_date)  
                if not self.price_data.empty:  
                    self.current_price = self.price_data['close'].iloc[-1]  
                    # 计算MA5/10/20  
                    self.price_data['MA5'] = self.price_data['close'].rolling(5).mean()  
                    self.price_data['MA10'] = self.price_data['close'].rolling(10).mean()  
                    self.price_data['MA20'] = self.price_data['close'].rolling(20).mean()  
        except Exception as e:  
            print(f"加载价格数据失败: {e}")  
            traceback.print_exc()  
    
    def create_main_content(self):  
        main_frame = tk.Frame(self)  
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  
        
        # 顶部行：物品图片和基本信息  
        top_frame = tk.Frame(main_frame)  
        top_frame.pack(fill=tk.X, pady=10)  
        
        # 物品图片  
        img_frame = tk.Frame(top_frame, width=150, height=150)  
        img_frame.pack(side=tk.LEFT, padx=20)  
        
        img = self.controller.get_item_image(self.item_name)  
        img_label = tk.Label(img_frame, image=img)  
        img_label.image = img  
        img_label.pack()  
        
        # 物品信息  
        info_frame = tk.Frame(top_frame)  
        info_frame.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)  
        
        name_label = tk.Label(info_frame, text=self.item_name, font=("微软雅黑", 16, "bold"))  
        name_label.pack(anchor=tk.W, pady=5)  
        
        price_label = tk.Label(info_frame, text=f"当前价格: ¥{self.current_price:.2f}", font=("微软雅黑", 14))  
        price_label.pack(anchor=tk.W, pady=5)  
        
        # 价格走势图  
        chart_frame = tk.Frame(main_frame, height=300)  
        chart_frame.pack(fill=tk.X, pady=10)  
        
        if self.price_data is not None and not self.price_data.empty:  
            self.create_price_chart(chart_frame)  
        else:  
            no_data_label = tk.Label(chart_frame, text="无价格数据", font=("微软雅黑", 14))  
            no_data_label.pack(pady=50)  
        
        # 交易操作区  
        trade_frame = tk.Frame(main_frame, bg="#f5f5f5", padx=20, pady=15)  
        trade_frame.pack(fill=tk.X, pady=10)  
        
        # 数量选择  
        quantity_frame = tk.Frame(trade_frame, bg="#f5f5f5")  
        quantity_frame.pack(pady=10)  
        
        quantity_label = tk.Label(quantity_frame, text="购买数量:", font=("微软雅黑", 12), bg="#f5f5f5")  
        quantity_label.pack(side=tk.LEFT, padx=5)  
        
        self.quantity_var = tk.IntVar(value=1)  
        quantity_spinbox = ttk.Spinbox(quantity_frame, from_=1, to=10, textvariable=self.quantity_var, width=10)  
        quantity_spinbox.pack(side=tk.LEFT, padx=5)  
        
        # 总价  
        self.total_label = tk.Label(trade_frame, text=f"总价: ¥{self.current_price:.2f}",   
                                   font=("微软雅黑", 12), bg="#f5f5f5")  
        self.total_label.pack(pady=10)  
        
        # 更新总价的回调  
        def update_total(*args):  
            quantity = self.quantity_var.get()  
            total = quantity * self.current_price  
            self.total_label.config(text=f"总价: ¥{total:.2f}")  
        
        self.quantity_var.trace_add("write", update_total)  
        
        # 买入按钮  
        buy_button = tk.Button(trade_frame, text="买入", font=("微软雅黑", 12, "bold"),   
                              bg="#4CAF50", fg="white", width=15, command=self.buy_item)  
        buy_button.pack(pady=10)  
        
        # 提示信息  
        self.message_label = tk.Label(trade_frame, text="", font=("微软雅黑", 10), bg="#f5f5f5")  
        self.message_label.pack(pady=5)  
    
    def create_price_chart(self, parent):  
        # 创建matplotlib图形  
        fig, ax = plt.subplots(figsize=(10, 5))  
        
        # 绘制收盘价  
        ax.plot(self.price_data.index, self.price_data['close'], label='价格', color='black')  
        
        # 绘制移动平均线  
        ax.plot(self.price_data.index, self.price_data['MA5'], label='MA5', color='red')  
        ax.plot(self.price_data.index, self.price_data['MA10'], label='MA10', color='blue')  
        ax.plot(self.price_data.index, self.price_data['MA20'], label='MA20', color='green')  
        
        # 设置图表格式  
        ax.set_title(f"{self.item_name} 价格走势", fontsize=14, fontproperties="SimHei")  
        ax.set_xlabel('日期', fontproperties="SimHei")  
        ax.set_ylabel('价格 (¥)', fontproperties="SimHei")  
        ax.grid(True, linestyle='--', alpha=0.7)  
        ax.legend(prop={"family": "SimHei"})  
        
        # 格式化x轴日期  
        date_format = mdates.DateFormatter('%m-%d')  
        ax.xaxis.set_major_formatter(date_format)  
        fig.autofmt_xdate()  
        
        # 嵌入到tkinter  
        canvas = FigureCanvasTkAgg(fig, parent)  
        canvas.draw()  
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  
        
        # 添加工具栏  
        toolbar = NavigationToolbar2Tk(canvas, parent)  
        toolbar.update()  
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  
    
    def buy_item(self):  
        quantity = self.quantity_var.get()  
        
        if quantity <= 0:  
            self.message_label.config(text="购买数量必须大于0", fg="red")  
            return  
        
        success, message = self.user.buy_item(self.item_name, self.current_price, quantity)  
        
        if success:  
            self.message_label.config(text=message, fg="green")  
            self.controller.user_manager.save_users()  # 保存用户数据  
            
            # 更新余额显示  
            for widget in self.winfo_children():  
                if isinstance(widget, tk.Frame) and widget.winfo_children():  
                    for child in widget.winfo_children():  
                        if isinstance(child, tk.Label) and "余额" in child.cget("text"):  
                            child.config(text=f"余额: ¥{self.user.balance:.2f}")  
        else:  
            self.message_label.config(text=message, fg="red")  

# 库存界面  
class InventoryFrame(tk.Frame):  
    def __init__(self, parent, controller):  
        super().__init__(parent)  
        self.controller = controller  
        self.user = controller.user_manager.current_user  
        
        # 创建顶部状态栏  
        self.create_status_bar()  
        
        # 创建主体内容  
        self.create_main_content()  
    
    def create_status_bar(self):  
        status_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=5)  
        status_frame.pack(fill=tk.X)  
        
        # 用户名和余额  
        user_label = tk.Label(status_frame, text=f"用户: {self.user.username}", font=("微软雅黑", 10), bg="#f0f0f0")  
        user_label.pack(side=tk.LEFT, padx=5)  
        
        balance_label = tk.Label(status_frame, text=f"余额: ¥{self.user.balance:.2f}", font=("微软雅黑", 10), bg="#f0f0f0")  
        balance_label.pack(side=tk.LEFT, padx=20)  
        
        # 导航按钮  
        market_btn = tk.Button(status_frame, text="市场", width=8, command=self.controller.show_market_frame)  
        market_btn.pack(side=tk.RIGHT, padx=5)  
        
        inventory_btn = tk.Button(status_frame, text="库存", width=8, command=self.controller.show_inventory_frame)  
        inventory_btn.pack(side=tk.RIGHT, padx=5)  
        
        history_btn = tk.Button(status_frame, text="交易历史", width=8, command=self.controller.show_history_frame)  
        history_btn.pack(side=tk.RIGHT, padx=5)  
    
    def create_main_content(self):  
        main_frame = tk.Frame(self, padx=20, pady=10)  
        main_frame.pack(fill=tk.BOTH, expand=True)  
        
        # 标题  
        title_label = tk.Label(main_frame, text="我的库存", font=("微软雅黑", 16, "bold"))  
        title_label.pack(anchor=tk.W, pady=(0, 10))  
        
        # 库存统计  
        stats_frame = tk.Frame(main_frame, bg="#f5f5f5", padx=15, pady=10)  
        stats_frame.pack(fill=tk.X, pady=10)  
        
        total_items = len(self.user.inventory)  
        total_value = sum(item.purchase_price * item.quantity for item in self.user.inventory)  
        
        stats_label = tk.Label(  
            stats_frame,   
            text=f"总物品数: {total_items}/1000    总价值: ¥{total_value:.2f}",   
            font=("微软雅黑", 12),  
            bg="#f5f5f5"  
        )  
        stats_label.pack()  
        
        # 创建表格  
        columns = ("序号", "物品名称", "购买价格", "数量", "购买日期", "冷却状态", "操作")  
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")  
        
        # 设置列宽  
        self.tree.column("序号", width=50, anchor=tk.CENTER)  
        self.tree.column("物品名称", width=200, anchor=tk.W)  
        self.tree.column("购买价格", width=100, anchor=tk.CENTER)  
        self.tree.column("数量", width=50, anchor=tk.CENTER)  
        self.tree.column("购买日期", width=120, anchor=tk.CENTER)  
        self.tree.column("冷却状态", width=120, anchor=tk.CENTER)  
        self.tree.column("操作", width=100, anchor=tk.CENTER)  
        
        # 设置表头  
        for col in columns:  
            self.tree.heading(col, text=col)  
        
        # 添加数据  
        self.populate_tree()  
        
        # 添加滚动条  
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)  
        self.tree.configure(yscroll=scrollbar.set)  
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  
        self.tree.pack(fill=tk.BOTH, expand=True)  
        
        # 消息区域  
        self.message_label = tk.Label(main_frame, text="", font=("微软雅黑", 10))  
        self.message_label.pack(pady=10)  
        
        # 绑定双击事件查看详情  
        self.tree.bind("<Double-1>", self.on_item_double_click)  
    
    def populate_tree(self):  
        # 清空现有数据  
        for i in self.tree.get_children():  
            self.tree.delete(i)  
        
        # 加载最新价格  
        current_prices = {}  
        for item_name, url in DATA_SOURCES.items():  
            try:  
                today = datetime.now().strftime('%Y-%m-%d')  
                yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  
                df = get_kline(url, yesterday, today)  
                current_prices[item_name] = df['close'].iloc[-1] if not df.empty else 0  
            except Exception as e:  
                print(f"获取价格失败 {item_name}: {e}")  
                current_prices[item_name] = 0  
        
        # 添加库存数据  
        for i, item in enumerate(self.user.inventory):  
            cooldown_status = f"{item.remaining_cooldown_days()}天" if not item.is_tradable() else "可交易"  
            cooldown_color = "red" if not item.is_tradable() else "green"  
            
            # 获取当前价格  
            current_price = current_prices.get(item.name, 0)  
            
            # 创建交易按钮  
            if item.is_tradable():  
                sell_text = f"卖出 (¥{current_price:.2f})"  
            else:  
                sell_text = f"冷却中 ({item.remaining_cooldown_days()}天)"  
            
            values = (  
                i + 1,  
                item.name,  
                f"¥{item.purchase_price:.2f}",  
                item.quantity,  
                item.purchase_date.strftime("%Y-%m-%d"),  
                cooldown_status  
            )  
            
            # 插入条目  
            item_id = self.tree.insert("", tk.END, values=values + (sell_text,))  
            
            # 设置颜色  
            if not item.is_tradable():  
                self.tree.item(item_id, tags=("cooldown",))  
        
        # 配置标签颜色  
        self.tree.tag_configure("cooldown", foreground="gray")  
        
        # 绑定点击事件  
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)  
    
    def on_tree_click(self, event):  
        # 获取点击的区域  
        region = self.tree.identify_region(event.x, event.y)  
        if region == "cell":  
            # 获取点击的列  
            column = self.tree.identify_column(event.x)  
            column_idx = int(column.replace('#', '')) - 1  
            
            # 如果点击的是"操作"列  
            if column_idx == 6:  # "操作"是第7列，索引为6  
                item_id = self.tree.identify_row(event.y)  
                if item_id:  
                    item_idx = self.tree.index(item_id)  
                    item = self.user.inventory[item_idx]  
                    
                    if item.is_tradable():  
                        # 获取当前价格  
                        try:  
                            today = datetime.now().strftime('%Y-%m-%d')  
                            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')  
                            url = DATA_SOURCES.get(item.name)  
                            if url:  
                                df = get_kline(url, yesterday, today)  
                                current_price = df['close'].iloc[-1] if not df.empty else 0  
                                
                                # 弹出确认对话框  
                                confirm = messagebox.askyesno(  
                                    "确认卖出",  
                                    f"确定要以 ¥{current_price:.2f} 的价格卖出 {item.name} 吗？\n" +  
                                    f"购买价: ¥{item.purchase_price:.2f}\n" +  
                                    f"盈亏: ¥{(current_price - item.purchase_price) * item.quantity:.2f}"  
                                )  
                                
                                if confirm:  
                                    # 执行卖出  
                                    success, message = self.user.sell_item(item_idx, current_price)  
                                    if success:  
                                        self.message_label.config(text=message, fg="green")  
                                        self.controller.user_manager.save_users()  # 保存用户数据  
                                        self.refresh()  # 刷新显示  
                                    else:  
                                        self.message_label.config(text=message, fg="red")  
                        except Exception as e:  
                            print(f"卖出失败: {e}")  
                            self.message_label.config(text=f"卖出失败: {str(e)}", fg="red")  
                    else:  
                        self.message_label.config(  
                            text=f"该物品还在交易冷却期，剩余 {item.remaining_cooldown_days()} 天",   
                            fg="red"  
                        )  
    
    def on_item_double_click(self, event):  
        """双击物品查看详情"""  
        item_id = self.tree.focus()  
        if item_id:  
            item_idx = self.tree.index(item_id)  
            if 0 <= item_idx < len(self.user.inventory):  
                item = self.user.inventory[item_idx]  
                self.controller.show_item_detail(item.name)  
    
    def refresh(self):  
        """刷新界面"""  
        # 更新余额显示  
        for widget in self.winfo_children():  
            if isinstance(widget, tk.Frame) and widget.winfo_children():  
                for child in widget.winfo_children():  
                    if isinstance(child, tk.Label) and "余额" in child.cget("text"):  
                        child.config(text=f"余额: ¥{self.user.balance:.2f}")  
        
        # 刷新表格  
        self.populate_tree()  

# 交易历史界面  
class HistoryFrame(tk.Frame):  
    def __init__(self, parent, controller):  
        super().__init__(parent)  
        self.controller = controller  
        self.user = controller.user_manager.current_user  
        
        # 创建顶部状态栏  
        self.create_status_bar()  
        
        # 创建主体内容  
        self.create_main_content()  
    
    def create_status_bar(self):  
        status_frame = tk.Frame(self, bg="#f0f0f0", padx=10, pady=5)  
        status_frame.pack(fill=tk.X)  
        
        # 用户名和余额  
        user_label = tk.Label(status_frame, text=f"用户: {self.user.username}", font=("微软雅黑", 10), bg="#f0f0f0")  
        user_label.pack(side=tk.LEFT, padx=5)  
        
        balance_label = tk.Label(status_frame, text=f"余额: ¥{self.user.balance:.2f}", font=("微软雅黑", 10), bg="#f0f0f0")  
        balance_label.pack(side=tk.LEFT, padx=20)  
        
        # 导航按钮  
        market_btn = tk.Button(status_frame, text="市场", width=8, command=self.controller.show_market_frame)  
        market_btn.pack(side=tk.RIGHT, padx=5)  
        
        inventory_btn = tk.Button(status_frame, text="库存", width=8, command=self.controller.show_inventory_frame)  
        inventory_btn.pack(side=tk.RIGHT, padx=5)  
        
        history_btn = tk.Button(status_frame, text="交易历史", width=8, command=self.controller.show_history_frame)  
        history_btn.pack(side=tk.RIGHT, padx=5)  
    
    def create_main_content(self):  
        main_frame = tk.Frame(self, padx=20, pady=10)  
        main_frame.pack(fill=tk.BOTH, expand=True)  
        
        # 标题  
        title_label = tk.Label(main_frame, text="交易历史", font=("微软雅黑", 16, "bold"))  
        title_label.pack(anchor=tk.W, pady=(0, 10))  
        
        # 统计信息  
        stats_frame = tk.Frame(main_frame, bg="#f5f5f5", padx=15, pady=10)  
        stats_frame.pack(fill=tk.X, pady=10)  
        
        # 计算统计数据  
        total_trades = len(self.user.transaction_history)  
        buy_trades = sum(1 for t in self.user.transaction_history if t['type'] == 'buy')  
        sell_trades = sum(1 for t in self.user.transaction_history if t['type'] == 'sell')  
        
        # 计算总盈亏  
        total_profit = sum(t.get('profit', 0) for t in self.user.transaction_history if t['type'] == 'sell')  
        
        stats_label = tk.Label(  
            stats_frame,   
            text=f"总交易次数: {total_trades}    买入: {buy_trades}    卖出: {sell_trades}    总盈亏: ¥{total_profit:.2f}",   
            font=("微软雅黑", 12),  
            bg="#f5f5f5"  
        )  
        stats_label.pack()  
        
        # 筛选选项  
        filter_frame = tk.Frame(main_frame, pady=10)  
        filter_frame.pack(fill=tk.X)  
        
        filter_label = tk.Label(filter_frame, text="交易类型:", font=("微软雅黑", 10))  
        filter_label.pack(side=tk.LEFT, padx=5)  
        
        self.filter_var = tk.StringVar(value="全部")  
        filter_combobox = ttk.Combobox(  
            filter_frame,   
            textvariable=self.filter_var,  
            values=["全部", "买入", "卖出"],  
            width=10,  
            state="readonly"  
        )  
        filter_combobox.pack(side=tk.LEFT, padx=5)  
        
        # 绑定筛选变化事件  
        self.filter_var.trace_add("write", lambda *args: self.populate_tree())  
        
        # 创建表格  
        if total_trades > 0:  
            # 根据交易类型设置列  
            self.create_trade_tree(main_frame)  
        else:  
            no_data_label = tk.Label(main_frame, text="暂无交易记录", font=("微软雅黑", 14))  
            no_data_label.pack(pady=50)  
    
    def create_trade_tree(self, parent):  
        # 创建表格框架  
        tree_frame = tk.Frame(parent)  
        tree_frame.pack(fill=tk.BOTH, expand=True)  
        
        # 创建表格  
        columns = ("序号", "类型", "物品", "价格", "数量", "日期", "总额", "盈亏")  
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")  
        