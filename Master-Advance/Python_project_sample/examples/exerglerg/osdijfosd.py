# library_system.py
"""
Python OOP 練習：圖書館管理系統
這個練習涵蓋了物件導向程式設計的主要概念：
1. 類別與實例
2. 繼承
3. 封裝
4. 多型
"""

# 第一部分：類別與實例
class Book:
    """基本的書籍類別"""
    
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False
    
    def borrow(self):
        """借出書籍"""
        if not self.is_borrowed:
            self.is_borrowed = True
            return True
        else:
            print(f"《{self.title}》已被借出，無法借閱。")
            return False
    
    def return_book(self):
        """歸還書籍"""
        if self.is_borrowed:
            self.is_borrowed = False
            return True
        else:
            print(f"《{self.title}》未被借出，無法歸還。")
            return False
    
    def __str__(self):
        status = "已借出" if self.is_borrowed else "可借閱"
        return f"《{self.title}》 作者：{self.author} ISBN：{self.isbn} 狀態：{status}"


# 第二部分：繼承
class FictionBook(Book):
    """小說類書籍"""
    
    def __init__(self, title, author, isbn, genre):
        super().__init__(title, author, isbn)
        self.genre = genre  # 小說類型，如奇幻、科幻、推理等
    
    def __str__(self):
        base_info = super().__str__()
        return f"{base_info} 類型：{self.genre}"


class ReferenceBook(Book):
    """參考書籍"""
    
    def __init__(self, title, author, isbn, subject):
        super().__init__(title, author, isbn)
        self.subject = subject  # 學科，如數學、物理、歷史等
        self.can_borrow = False  # 參考書通常不外借
    
    def borrow(self):
        """覆寫借書方法，參考書不可外借"""
        print(f"《{self.title}》是參考書，僅供館內閱讀，不可外借。")
        return False
    
    def __str__(self):
        base_info = super().__str__().replace("已借出" if self.is_borrowed else "可借閱", "僅供館內閱讀")
        return f"{base_info} 學科：{self.subject}"


# 第三部分：封裝
class Library:
    """圖書館類別"""
    
    def __init__(self, name):
        self.__name = name
        self.__books = []  # 私有屬性，存儲圖書館的所有書籍
    
    @property
    def name(self):
        """獲取圖書館名稱"""
        return self.__name
    
    @property
    def book_count(self):
        """獲取書籍總數"""
        return len(self.__books)
    
    def add_book(self, book):
        """添加書籍到圖書館"""
        self.__books.append(book)
        print(f"《{book.title}》已添加到{self.__name}。")
    
    def remove_book(self, isbn):
        """從圖書館移除書籍"""
        for book in self.__books:
            if book.isbn == isbn:
                self.__books.remove(book)
                print(f"《{book.title}》已從{self.__name}移除。")
                return True
        print(f"未找到ISBN為{isbn}的書籍。")
        return False
    
    def find_book(self, isbn):
        """查找書籍"""
        for book in self.__books:
            if book.isbn == isbn:
                return book
        return None
    
    def list_books(self):
        """列出所有書籍"""
        if not self.__books:
            print(f"{self.__name}目前沒有任何書籍。")
            return
        
        print(f"{self.__name}的書籍列表：")
        for i, book in enumerate(self.__books, 1):
            print(f"{i}. {book}")


# 第四部分：多型
def display_info(book):
    """顯示書籍信息，根據書籍類型顯示不同的信息"""
    print(f"書籍信息：{book}")
    
    # 根據書籍類型顯示不同的附加信息
    if isinstance(book, FictionBook):
        print(f"這是一本{book.genre}類型的小說，適合休閒閱讀。")
    elif isinstance(book, ReferenceBook):
        print(f"這是一本{book.subject}學科的參考書，適合學術研究。")
    else:
        print("這是一本普通書籍。")


# 綜合練習：用戶交互
def main():
    """主程序"""
    # 創建圖書館
    library = Library("Python學習圖書館")
    
    # 添加一些書籍
    library.add_book(Book("Python基礎教程", "Magnus Lie Hetland", "9787115547989"))
    library.add_book(FictionBook("哈利波特與魔法石", "J.K.羅琳", "9787020033299", "奇幻"))
    library.add_book(ReferenceBook("高等數學", "同濟大學數學系", "9787030212085", "數學"))
    
    # 用戶交互
    while True:
        print("\n" + "="*50)
        print(f"歡迎使用{library.name}管理系統")
        print("1. 查看所有書籍")
        print("2. 添加新書籍")
        print("3. 借閱書籍")
        print("4. 歸還書籍")
        print("5. 查詢書籍詳情")
        print("6. 移除書籍")
        print("0. 退出系統")
        
        choice = input("請選擇操作 (0-6): ")
        
        if choice == "1":
            library.list_books()
        
        elif choice == "2":
            title = input("請輸入書名: ")
            author = input("請輸入作者: ")
            isbn = input("請輸入ISBN: ")
            
            book_type = input("請選擇書籍類型 (1:普通書籍, 2:小說, 3:參考書): ")
            if book_type == "2":
                genre = input("請輸入小說類型: ")
                library.add_book(FictionBook(title, author, isbn, genre))
            elif book_type == "3":
                subject = input("請輸入學科: ")
                library.add_book(ReferenceBook(title, author, isbn, subject))
            else:
                library.add_book(Book(title, author, isbn))
        
        elif choice == "3":
            isbn = input("請輸入要借閱的書籍ISBN: ")
            book = library.find_book(isbn)
            if book:
                if book.borrow():
                    print(f"《{book.title}》借閱成功！")
            else:
                print(f"未找到ISBN為{isbn}的書籍。")
        
        elif choice == "4":
            isbn = input("請輸入要歸還的書籍ISBN: ")
            book = library.find_book(isbn)
            if book:
                if book.return_book():
                    print(f"《{book.title}》歸還成功！")
            else:
                print(f"未找到ISBN為{isbn}的書籍。")
        
        elif choice == "5":
            isbn = input("請輸入要查詢的書籍ISBN: ")
            book = library.find_book(isbn)
            if book:
                display_info(book)
            else:
                print(f"未找到ISBN為{isbn}的書籍。")
        
        elif choice == "6":
            isbn = input("請輸入要移除的書籍ISBN: ")
            library.remove_book(isbn)
        
        elif choice == "0":
            print(f"感謝使用{library.name}管理系統，再見！")
            break
        
        else:
            print("無效的選擇，請重新輸入。")


# 挑戰任務：實現更多高級功能
class User:
    """用戶類別"""
    
    def __init__(self, user_id, name):
        self.__user_id = user_id
        self.__name = name
        self.__borrowed_books = []  # 用戶借閱的書籍列表
    
    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def borrowed_books(self):
        return self.__borrowed_books.copy()  # 返回副本以保護原始數據
    
    def borrow_book(self, book):
        """借閱書籍"""
        if book.borrow():
            self.__borrowed_books.append(book)
            return True
        return False
    
    def return_book(self, book):
        """歸還書籍"""
        if book in self.__borrowed_books and book.return_book():
            self.__borrowed_books.remove(book)
            return True
        return False
    
    def __str__(self):
        return f"用戶ID：{self.__user_id}，姓名：{self.__name}，已借閱{len(self.__borrowed_books)}本書"


# 如果直接運行此文件，則執行主程序
if __name__ == "__main__":
    main()