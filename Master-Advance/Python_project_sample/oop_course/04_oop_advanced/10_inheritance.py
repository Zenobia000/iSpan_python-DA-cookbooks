# 10_inheritance.py
# This file is part of the OOP course

"""
繼承 (Inheritance)
===================
本模組展示Python中繼承的基本和進階概念。

主題:
1. 單一繼承基礎
2. 方法重寫 (Method Overriding)
3. super()函數的使用
4. 繼承層次結構
"""

# 1. 基本繼承示例
print("="*50)
print("基本繼承示例")
print("="*50)

class Animal:
    """動物基類"""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
        
    def make_sound(self):
        print("一些通用的動物聲音")
        
    def __str__(self):
        return f"{self.name} 是一隻 {self.species}"


class Dog(Animal):
    """繼承自Animal的狗類"""
    
    def __init__(self, name, breed):
        # 使用父類初始化
        super().__init__(name, species="狗")
        self.breed = breed
        
    def make_sound(self):
        # 方法重寫
        print("汪汪!")
        
    def __str__(self):
        return f"{self.name} 是一隻 {self.breed} 品種的狗"


# 創建動物和狗的實例
animal = Animal("泡泡", "未知")
dog = Dog("小黑", "拉布拉多")

print(animal)
print(dog)
print("動物叫聲:", end=" ")
animal.make_sound()
print("狗叫聲:", end=" ")
dog.make_sound()


# 2. 深入繼承層次
print("\n"+"="*50)
print("繼承層次結構")
print("="*50)

class Pet:
    """寵物基類"""
    
    def __init__(self, name):
        self.name = name
    
    def show_affection(self):
        print(f"{self.name} 顯示了一些感情")


class DomesticDog(Dog, Pet):
    """多重繼承示例: 同時繼承Dog和Pet"""
    
    def __init__(self, name, breed, owner):
        # 必須明確調用兩個父類的初始化方法
        Dog.__init__(self, name, breed)
        Pet.__init__(self, name)  # 這會覆蓋Dog.__init__設定的name
        self.owner = owner
        
    def show_affection(self):
        print(f"{self.name} 舔了 {self.owner} 的手")
        
    def __str__(self):
        return f"{self.name} 是 {self.owner} 的 {self.breed} 寵物狗"


# 創建家養狗的實例
pet_dog = DomesticDog("Lucky", "金毛獵犬", "小明")
print(pet_dog)
print("叫聲:", end=" ")
pet_dog.make_sound()  # 從Dog繼承的方法
pet_dog.show_affection()  # 從Pet繼承並重寫的方法


# 3. 使用isinstance()和issubclass()檢查繼承關係
print("\n"+"="*50)
print("檢查繼承關係")
print("="*50)

print(f"pet_dog 是 DomesticDog 的實例嗎? {isinstance(pet_dog, DomesticDog)}")
print(f"pet_dog 是 Dog 的實例嗎? {isinstance(pet_dog, Dog)}")
print(f"pet_dog 是 Animal 的實例嗎? {isinstance(pet_dog, Animal)}")
print(f"pet_dog 是 Pet 的實例嗎? {isinstance(pet_dog, Pet)}")

print(f"DomesticDog 是 Dog 的子類嗎? {issubclass(DomesticDog, Dog)}")
print(f"DomesticDog 是 Animal 的子類嗎? {issubclass(DomesticDog, Animal)}")
print(f"DomesticDog 是 Pet 的子類嗎? {issubclass(DomesticDog, Pet)}")


# 實際應用: 繼承設計
if __name__ == "__main__":
    print("\n"+"="*50)
    print("繼承設計示例: 資料庫連接器")
    print("="*50)
    
    class DatabaseConnector:
        """基本數據庫連接器基類"""
        
        def __init__(self, host, username, password):
            self.host = host
            self.username = username
            self.password = password
            self.connection = None
            
        def connect(self):
            print(f"建立到 {self.host} 的通用數據庫連接")
            self.connection = "已連接"
            
        def disconnect(self):
            print("關閉連接")
            self.connection = None
            
        def execute(self, query):
            print(f"執行查詢: {query}")
            
            
    class MySQLConnector(DatabaseConnector):
        """MySQL專用連接器"""
        
        def __init__(self, host, username, password, database):
            super().__init__(host, username, password)
            self.database = database
            
        def connect(self):
            print(f"使用MySQL協議連接到 {self.host}/{self.database}")
            self.connection = "MySQL已連接"
            
        def create_database(self):
            print(f"創建MySQL數據庫 {self.database}")
            
            
    class PostgreSQLConnector(DatabaseConnector):
        """PostgreSQL專用連接器"""
        
        def __init__(self, host, username, password, database, port=5432):
            super().__init__(host, username, password)
            self.database = database
            self.port = port
            
        def connect(self):
            print(f"使用PostgreSQL協議連接到 {self.host}:{self.port}/{self.database}")
            self.connection = "PostgreSQL已連接"
            
        def create_schema(self, schema_name):
            print(f"在{self.database}中創建schema {schema_name}")
    
    
    # 使用示例
    mysql_db = MySQLConnector("localhost", "root", "password", "users_db")
    mysql_db.connect()
    mysql_db.execute("SELECT * FROM users")
    mysql_db.create_database()  # MySQL特有方法
    mysql_db.disconnect()
    
    print()
    
    pg_db = PostgreSQLConnector("db.example.com", "admin", "secure123", "analytics", 5433)
    pg_db.connect()
    pg_db.execute("SELECT * FROM metrics")
    pg_db.create_schema("reports")  # PostgreSQL特有方法
    pg_db.disconnect()

