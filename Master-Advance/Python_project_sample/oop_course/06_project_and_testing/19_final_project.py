# 19_final_project.py
# This file is part of the OOP course

"""
最終項目 (Final Project)
======================
本模組是OOP課程的最終項目，整合了所學的所有面向對象編程概念。

項目內容: 圖書管理系統
1. 系統設計與需求分析
2. 核心類結構設計
3. 設計模式應用
4. 測試與文檔
5. 項目展示與評估
"""

print("="*50)
print("最終項目: 圖書管理系統")
print("="*50)

print("這個圖書管理系統整合了課程中學習的OOP概念:")
print("- 類設計與封裝")
print("- 繼承與多態")
print("- 特殊方法與運算符重載")
print("- 設計模式 (單例、工廠、觀察者等)")
print("- 測試與文檔")

# 圖書管理系統的核心類

# 1. 圖書類
class Book:
    """圖書類，代表一本書籍"""
    
    def __init__(self, book_id, title, author, isbn, published_date, category, copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.published_date = published_date
        self.category = category
        self.copies = copies  # 總複本數
        self.available_copies = copies  # 可用複本數
    
    def checkout(self):
        """借出圖書"""
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    
    def return_book(self):
        """歸還圖書"""
        if self.available_copies < self.copies:
            self.available_copies += 1
            return True
        return False
    
    def __str__(self):
        """字符串表示"""
        status = "可借閱" if self.available_copies > 0 else "已借出"
        return f"{self.title} by {self.author} ({status}, {self.available_copies}/{self.copies}本可用)"
    
    def __eq__(self, other):
        """相等比較，基於ISBN"""
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn


# 2. 使用者相關類
class User:
    """使用者基類"""
    
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.borrowed_books = []  # 借閱的書籍列表
    
    def borrow_book(self, book):
        """借書方法"""
        if book.checkout():
            self.borrowed_books.append(book)
            return True
        return False
    
    def return_book(self, book):
        """還書方法"""
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        return False
    
    def __str__(self):
        """字符串表示"""
        return f"{self.name} (ID: {self.user_id}, 已借 {len(self.borrowed_books)} 本書)"


class Student(User):
    """學生用戶"""
    
    def __init__(self, user_id, name, email, grade):
        super().__init__(user_id, name, email)
        self.grade = grade
        self.max_books = 3  # 學生最多可借3本書
    
    def borrow_book(self, book):
        """覆寫借書方法，增加借書上限檢查"""
        if len(self.borrowed_books) >= self.max_books:
            print(f"已達借書上限 ({self.max_books}本)")
            return False
        return super().borrow_book(book)


class Faculty(User):
    """教職員用戶"""
    
    def __init__(self, user_id, name, email, department):
        super().__init__(user_id, name, email)
        self.department = department
        self.max_books = 10  # 教職員最多可借10本書
    
    def borrow_book(self, book):
        """覆寫借書方法，增加借書上限檢查"""
        if len(self.borrowed_books) >= self.max_books:
            print(f"已達借書上限 ({self.max_books}本)")
            return False
        return super().borrow_book(book)
    
    def request_purchase(self, title, author, isbn):
        """請求購買新書"""
        return {"title": title, "author": author, "isbn": isbn, "requested_by": self.name}


# 3. 圖書目錄 (使用單例模式)
class Catalog:
    """圖書目錄類 (單例)"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.books = {}  # 以ISBN為鍵的書籍字典
            cls._instance.observers = []  # 觀察者列表
        return cls._instance
    
    def add_book(self, book):
        """添加書籍到目錄"""
        self.books[book.isbn] = book
        self.notify_observers(f"新書已添加: {book.title}")
    
    def remove_book(self, isbn):
        """從目錄中移除書籍"""
        if isbn in self.books:
            book = self.books[isbn]
            del self.books[isbn]
            self.notify_observers(f"書籍已移除: {book.title}")
            return True
        return False
    
    def search_by_title(self, title):
        """按標題搜索書籍"""
        return [book for book in self.books.values() if title.lower() in book.title.lower()]
    
    def search_by_author(self, author):
        """按作者搜索書籍"""
        return [book for book in self.books.values() if author.lower() in book.author.lower()]
    
    def search_by_category(self, category):
        """按類別搜索書籍"""
        return [book for book in self.books.values() if category.lower() == book.category.lower()]
    
    def get_book(self, isbn):
        """根據ISBN獲取書籍"""
        return self.books.get(isbn)
    
    def register_observer(self, observer):
        """註冊觀察者"""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        """移除觀察者"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self, message):
        """通知所有觀察者"""
        for observer in self.observers:
            observer.update(message)


# 4. 圖書管理員 (使用觀察者模式)
class LibraryObserver:
    """圖書館觀察者接口"""
    
    def update(self, message):
        """接收更新"""
        pass


class Librarian(LibraryObserver):
    """圖書管理員類"""
    
    def __init__(self, staff_id, name):
        self.staff_id = staff_id
        self.name = name
        self.notifications = []
    
    def update(self, message):
        """接收目錄更新通知"""
        notification = f"[{self.staff_id}] {message}"
        self.notifications.append(notification)
        print(f"通知 {self.name}: {notification}")
    
    def process_return(self, user, book):
        """處理還書"""
        if user.return_book(book):
            print(f"{self.name} 已處理 {user.name} 歸還的 '{book.title}'")
            return True
        print(f"處理還書失敗: {user.name} 沒有借閱 '{book.title}'")
        return False
    
    def generate_report(self, catalog):
        """生成書籍報告"""
        total_books = len(catalog.books)
        available_books = sum(1 for book in catalog.books.values() if book.available_copies > 0)
        out_books = sum(book.copies - book.available_copies for book in catalog.books.values())
        
        report = f"圖書館報告:\n"
        report += f"總藏書: {total_books} 種\n"
        report += f"可借書籍: {available_books} 種\n"
        report += f"已借出: {out_books} 本\n"
        
        return report


# 5. 圖書館系統 (整合所有組件)
class LibrarySystem:
    """圖書館系統類"""
    
    def __init__(self, name):
        self.name = name
        self.catalog = Catalog()  # 單例的目錄
        self.users = {}  # 用戶字典
        self.librarians = {}  # 管理員字典
        self.next_book_id = 1
        self.next_user_id = 1
    
    def add_user(self, name, email, user_type, **kwargs):
        """添加用戶"""
        user_id = f"U{self.next_user_id:04d}"
        self.next_user_id += 1
        
        if user_type.lower() == "student":
            grade = kwargs.get("grade", "")
            user = Student(user_id, name, email, grade)
        elif user_type.lower() == "faculty":
            department = kwargs.get("department", "")
            user = Faculty(user_id, name, email, department)
        else:
            user = User(user_id, name, email)
        
        self.users[user_id] = user
        return user
    
    def add_librarian(self, name):
        """添加圖書管理員"""
        staff_id = f"L{len(self.librarians) + 1:04d}"
        librarian = Librarian(staff_id, name)
        self.librarians[staff_id] = librarian
        self.catalog.register_observer(librarian)
        return librarian
    
    def add_book(self, title, author, isbn, published_date, category, copies=1):
        """添加書籍"""
        book_id = f"B{self.next_book_id:04d}"
        self.next_book_id += 1
        
        book = Book(book_id, title, author, isbn, published_date, category, copies)
        self.catalog.add_book(book)
        return book
    
    def checkout_book(self, user_id, isbn):
        """處理借書"""
        user = self.users.get(user_id)
        if not user:
            return False, "用戶不存在"
        
        book = self.catalog.get_book(isbn)
        if not book:
            return False, "書籍不存在"
        
        if user.borrow_book(book):
            return True, f"{user.name} 成功借閱 '{book.title}'"
        else:
            return False, f"借閱失敗: '{book.title}' 無法借出"
    
    def return_book(self, user_id, isbn, librarian_id):
        """處理還書"""
        user = self.users.get(user_id)
        if not user:
            return False, "用戶不存在"
        
        book = self.catalog.get_book(isbn)
        if not book:
            return False, "書籍不存在"
        
        librarian = self.librarians.get(librarian_id)
        if not librarian:
            return False, "管理員不存在"
        
        if librarian.process_return(user, book):
            return True, f"{user.name} 已歸還 '{book.title}'"
        else:
            return False, "還書失敗"


# 測試圖書管理系統
print("\n"+"="*50)
print("圖書管理系統測試")
print("="*50)

# 創建圖書館系統
library = LibrarySystem("Python學習圖書館")

# 添加圖書管理員
librarian1 = library.add_librarian("張管理")
librarian2 = library.add_librarian("李管理")

# 添加用戶
student1 = library.add_user("小明", "ming@example.com", "student", grade="大一")
student2 = library.add_user("小紅", "hong@example.com", "student", grade="大二")
faculty1 = library.add_user("王教授", "wang@example.com", "faculty", department="計算機科學")

# 添加書籍
book1 = library.add_book("Python編程", "張三", "9781234567890", "2020-01-01", "編程", 3)
book2 = library.add_book("數據結構", "李四", "9789876543210", "2019-05-15", "計算機科學", 2)
book3 = library.add_book("機器學習入門", "王五", "9785678901234", "2021-03-10", "人工智能", 1)

# 測試借書
print("\n借書測試:")
result, message = library.checkout_book(student1.user_id, book1.isbn)
print(message)

result, message = library.checkout_book(student1.user_id, book2.isbn)
print(message)

result, message = library.checkout_book(faculty1.user_id, book3.isbn)
print(message)

result, message = library.checkout_book(student2.user_id, book1.isbn)
print(message)

# 查看書籍狀態
print("\n書籍狀態:")
print(book1)
print(book2)
print(book3)

# 查看用戶狀態
print("\n用戶狀態:")
print(student1)
print(student2)
print(faculty1)

# 測試還書
print("\n還書測試:")
result, message = library.return_book(student1.user_id, book1.isbn, librarian1.staff_id)
print(message)

# 再次查看書籍狀態
print("\n書籍狀態(還書後):")
print(book1)

# 生成報告
print("\n圖書館報告:")
print(librarian1.generate_report(library.catalog))


print("\n"+"="*50)
print("後續擴展建議")
print("="*50)

print("1. 持久化存儲:")
print("   - 使用JSON、CSV或資料庫存儲資料")
print("   - 實現保存/載入功能")

print("\n2. 圖形界面:")
print("   - 使用Tkinter或PyQt建立GUI")
print("   - 實現登入、搜索、借還書等功能")

print("\n3. 擴展功能:")
print("   - 預約功能")
print("   - 逾期提醒和罰款")
print("   - 書籍評論和評分系統")

print("\n4. 其他改進:")
print("   - 強化搜索功能")
print("   - 添加資料匯入/匯出")
print("   - 實現權限控制系統")

