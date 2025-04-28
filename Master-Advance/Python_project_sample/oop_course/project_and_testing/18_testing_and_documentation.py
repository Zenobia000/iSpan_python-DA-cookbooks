# 18_testing_and_documentation.py
# This file is part of the OOP course

"""
測試與文檔 (Testing and Documentation)
===================================
本模組介紹Python中的測試方法和文檔撰寫最佳實踐。

主題:
1. 單元測試 (Unit Testing)
2. 測試驅動開發 (TDD)
3. doctest和doctstring的使用
4. Sphinx文檔生成
5. 整合測試與持續集成
"""

import doctest
import unittest
import math


print("="*50)
print("測試與文檔簡介")
print("="*50)
print("測試和文檔是專業Python開發的重要組成部分")
print("好的測試確保代碼質量，好的文檔提高代碼可維護性")
print("本模組將介紹Python中的測試框架和文檔工具")


# 1. 單元測試
print("\n"+"="*50)
print("1. 單元測試 (Unit Testing)")
print("="*50)

print("單元測試是測試程序中最小單位（函數/方法）的方式")
print("Python內置了unittest框架用於單元測試")

# 待測試的代碼
class Calculator:
    """簡單計算器類，用於演示單元測試"""
    
    def add(self, a, b):
        """返回兩個數的和"""
        return a + b
    
    def subtract(self, a, b):
        """返回兩個數的差"""
        return a - b
    
    def multiply(self, a, b):
        """返回兩個數的積"""
        return a * b
    
    def divide(self, a, b):
        """返回兩個數的商"""
        if b == 0:
            raise ValueError("除數不能為零")
        return a / b
    
    def square_root(self, x):
        """返回數字的平方根"""
        if x < 0:
            raise ValueError("不能對負數求平方根")
        return math.sqrt(x)


# 為Calculator類編寫測試
class TestCalculator(unittest.TestCase):
    """Calculator類的測試用例"""
    
    def setUp(self):
        """每個測試方法執行前的設置"""
        self.calc = Calculator()
    
    def test_add(self):
        """測試加法功能"""
        self.assertEqual(self.calc.add(3, 5), 8)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(-1, -1), -2)
    
    def test_subtract(self):
        """測試減法功能"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(1, 5), -4)
        self.assertEqual(self.calc.subtract(-1, -1), 0)
    
    def test_multiply(self):
        """測試乘法功能"""
        self.assertEqual(self.calc.multiply(3, 5), 15)
        self.assertEqual(self.calc.multiply(-1, 5), -5)
        self.assertEqual(self.calc.multiply(-1, -1), 1)
    
    def test_divide(self):
        """測試除法功能"""
        self.assertEqual(self.calc.divide(6, 3), 2)
        self.assertEqual(self.calc.divide(5, 2), 2.5)
        self.assertEqual(self.calc.divide(-6, 2), -3)
        self.assertEqual(self.calc.divide(-6, -2), 3)
    
    def test_divide_by_zero(self):
        """測試除以零時是否拋出異常"""
        with self.assertRaises(ValueError):
            self.calc.divide(6, 0)
    
    def test_square_root(self):
        """測試平方根功能"""
        self.assertEqual(self.calc.square_root(4), 2)
        self.assertEqual(self.calc.square_root(2), math.sqrt(2))
    
    def test_square_root_negative(self):
        """測試對負數求平方根時是否拋出異常"""
        with self.assertRaises(ValueError):
            self.calc.square_root(-4)
    
    def tearDown(self):
        """每個測試方法執行後的清理"""
        pass  # 本例中不需要特別清理


# 執行單元測試
print("\n執行單元測試:")
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)

print("\n單元測試的斷言方法:")
print("assertEqual(a, b) - 檢查 a == b")
print("assertNotEqual(a, b) - 檢查 a != b")
print("assertTrue(x) - 檢查 bool(x) 為 True")
print("assertFalse(x) - 檢查 bool(x) 為 False")
print("assertRaises(exc, func, *args, **kwargs) - 檢查調用函數是否拋出指定異常")
print("assertAlmostEqual(a, b) - 檢查 a 和 b 近似相等，用於浮點數比較")


# 2. 測試驅動開發 (TDD)
print("\n"+"="*50)
print("2. 測試驅動開發 (TDD)")
print("="*50)

print("TDD是一種開發方法，先寫測試後寫代碼")
print("TDD的步驟: 1. 寫測試 2. 運行測試（失敗） 3. 編寫代碼使測試通過 4. 重構代碼")

# TDD示例 - 開發一個密碼驗證器
print("\nTDD示例 - 開發密碼驗證器:")

# 步驟1: 先寫測試
class TestPasswordValidator(unittest.TestCase):
    """密碼驗證器的測試用例"""
    
    def test_length(self):
        """測試密碼長度是否符合要求"""
        validator = PasswordValidator()
        self.assertFalse(validator.validate("short"))  # 密碼太短
        self.assertTrue(validator.validate("longenoughpassword"))  # 密碼夠長
    
    def test_has_number(self):
        """測試密碼是否包含數字"""
        validator = PasswordValidator()
        self.assertFalse(validator.validate("noNumbersHere"))  # 沒有數字
        self.assertTrue(validator.validate("contains1Number"))  # 有數字
    
    def test_has_uppercase(self):
        """測試密碼是否包含大寫字母"""
        validator = PasswordValidator()
        self.assertFalse(validator.validate("no_uppercase_letters123"))  # 沒有大寫字母
        self.assertTrue(validator.validate("Contains_Uppercase123"))  # 有大寫字母


# 步驟2: 根據測試編寫代碼
class PasswordValidator:
    """密碼驗證器，用於檢查密碼是否符合安全要求"""
    
    def validate(self, password):
        """
        驗證密碼是否符合以下條件:
        1. 長度至少為8個字符
        2. 包含至少一個數字
        3. 包含至少一個大寫字母
        
        Parameters:
            password (str): 要驗證的密碼
            
        Returns:
            bool: 密碼是否有效
        """
        # 檢查長度
        if len(password) < 8:
            return False
        
        # 檢查是否包含數字
        has_number = False
        for char in password:
            if char.isdigit():
                has_number = True
                break
        
        if not has_number:
            return False
        
        # 檢查是否包含大寫字母
        has_uppercase = False
        for char in password:
            if char.isupper():
                has_uppercase = True
                break
        
        if not has_uppercase:
            return False
        
        # 所有條件都滿足
        return True


# 步驟3: 運行測試，確認代碼正確
print("\n運行密碼驗證器測試:")
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPasswordValidator)
test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)

# 步驟4: 重構代碼使其更簡潔
class ImprovedPasswordValidator:
    """改進的密碼驗證器"""
    
    def validate(self, password):
        """檢查密碼是否有效"""
        # 檢查長度
        if len(password) < 8:
            return False
        
        # 使用any()簡化檢查
        if not any(char.isdigit() for char in password):
            return False
        
        if not any(char.isupper() for char in password):
            return False
        
        return True


# 確認重構的代碼仍然通過測試
print("\n測試重構後的密碼驗證器:")
# 創建一個新的測試類以使用重構的驗證器
class TestImprovedPasswordValidator(unittest.TestCase):
    def test_validation(self):
        validator = ImprovedPasswordValidator()
        self.assertFalse(validator.validate("short"))
        self.assertFalse(validator.validate("longenoughbutnonumbers"))
        self.assertFalse(validator.validate("longenoughwith1butnouppercase"))
        self.assertTrue(validator.validate("GoodPassword123"))

test_suite = unittest.TestLoader().loadTestsFromTestCase(TestImprovedPasswordValidator)
test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)


# 3. doctest
print("\n"+"="*50)
print("3. doctest和docstring")
print("="*50)

print("doctest允許你在文檔字符串中包含測試用例")
print("有助於確保文檔和代碼保持同步，並驗證示例的正確性")

# doctest示例
def split_name(full_name):
    """
    將全名分割為名和姓。
    
    Parameters:
        full_name (str): 完整姓名，格式為 "名 姓"
    
    Returns:
        tuple: 包含 (名, 姓) 的元組
    
    Examples:
        >>> split_name("John Doe")
        ('John', 'Doe')
        >>> split_name("Jane Smith")
        ('Jane', 'Smith')
        >>> split_name("Robert Johnson")
        ('Robert', 'Johnson')
        >>> split_name("")
        Traceback (most recent call last):
            ...
        ValueError: 名字不能為空
        >>> split_name("SingleName")
        Traceback (most recent call last):
            ...
        ValueError: 全名必須包含名和姓
    """
    if not full_name:
        raise ValueError("名字不能為空")
    
    parts = full_name.split()
    if len(parts) < 2:
        raise ValueError("全名必須包含名和姓")
    
    first_name = parts[0]
    last_name = ' '.join(parts[1:])
    
    return (first_name, last_name)


# 運行doctest
print("\n運行doctest:")
doctest_results = doctest.testmod(verbose=True)
print(f"失敗的測試: {doctest_results.failed}")
print(f"嘗試的測試: {doctest_results.attempted}")

# 文檔字符串最佳實踐
print("\n文檔字符串最佳實踐:")
print("1. 使用Google、NumPy或reStructuredText風格")
print("2. 包含功能描述、參數說明、返回值說明和示例")

# Google風格示例
def google_style_docstring(param1, param2, param3=None):
    """這是Google風格的文檔字符串示例。
    
    這是函數的詳細描述，可以跨越多行。
    
    Args:
        param1 (int): 第一個參數的描述
        param2 (str): 第二個參數的描述
        param3 (list, optional): 第三個參數的描述，默認為None
    
    Returns:
        bool: 返回值的描述
    
    Raises:
        ValueError: 異常的描述
    
    Examples:
        >>> google_style_docstring(1, "test")
        True
    """
    return True

# NumPy風格示例
def numpy_style_docstring(param1, param2, param3=None):
    """
    這是NumPy風格的文檔字符串示例。
    
    這是函數的詳細描述，可以跨越多行。
    
    Parameters
    ----------
    param1 : int
        第一個參數的描述
    param2 : str
        第二個參數的描述
    param3 : list, optional
        第三個參數的描述，默認為None
    
    Returns
    -------
    bool
        返回值的描述
    
    Raises
    ------
    ValueError
        異常的描述
    
    Examples
    --------
    >>> numpy_style_docstring(1, "test")
    True
    """
    return True


# 4. Sphinx文檔生成
print("\n"+"="*50)
print("4. Sphinx文檔生成")
print("="*50)

print("Sphinx是一個強大的文檔生成工具，可以從Python代碼創建HTML、PDF等格式的文檔")
print("Sphinx使用步驟:")
print("1. 安裝: pip install sphinx")
print("2. 初始化: sphinx-quickstart")
print("3. 配置: conf.py")
print("4. 生成: make html")

print("\nSphinx支持的特性:")
print("1. 自動從docstrings生成API文檔")
print("2. 跨引用和超連接")
print("3. 支持數學公式和圖表")
print("4. 可擴展的主題和插件")

# 符合Sphinx格式的文檔字符串示例
class SphinxExample:
    """
    這是一個符合Sphinx格式的類文檔字符串。
    
    這個類用於展示Sphinx文檔生成。
    
    :param param1: 第一個參數的描述
    :type param1: int
    :param param2: 第二個參數的描述
    :type param2: str
    :raises ValueError: 當參數無效時
    """
    
    def __init__(self, param1, param2):
        """
        初始化方法
        
        :param param1: 第一個參數
        :param param2: 第二個參數
        """
        self.param1 = param1
        self.param2 = param2
    
    def method(self, x):
        """
        一個示例方法
        
        :param x: 輸入參數
        :type x: float
        :return: 計算結果
        :rtype: float
        
        .. note::
           這是一個注意事項
        
        .. warning::
           這是一個警告
        """
        return x * self.param1


# 5. 整合測試與持續集成
print("\n"+"="*50)
print("5. 整合測試與持續集成")
print("="*50)

print("整合測試驗證多個組件一起工作的能力")
print("持續集成(CI)在每次代碼變更時自動運行測試")

print("\n常用的CI工具:")
print("1. GitHub Actions")
print("2. GitLab CI/CD")
print("3. Jenkins")
print("4. Travis CI")
print("5. CircleCI")

print("\nCI配置示例 (GitHub Actions):")
print("""
name: Python Testing

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        pip install -e .
    - name: Test with pytest
      run: |
        pytest --cov=./
    - name: Upload coverage reports
      uses: codecov/codecov-action@v1
""")

print("\n測試覆蓋率:")
print("測試覆蓋率衡量代碼被測試的百分比")
print("使用pytest-cov或coverage.py工具測量")
print("命令: pytest --cov=my_package tests/")

print("\n模擬和測試替身:")
print("使用unittest.mock模塊創建模擬對象")
print("模擬外部服務和難以測試的組件")

# 模擬示例
from unittest.mock import MagicMock, patch

def get_user_data(user_id):
    """從API獲取用戶數據"""
    # 在實際代碼中，這會調用外部API
    api_response = {"id": user_id, "name": "測試用戶", "email": "test@example.com"}
    return api_response

# 使用模擬進行測試
class TestWithMock(unittest.TestCase):
    @patch('__main__.get_user_data')
    def test_get_user_data(self, mock_get_user_data):
        # 設置模擬返回值
        mock_get_user_data.return_value = {"id": 42, "name": "模擬用戶", "email": "mock@example.com"}
        
        # 調用被測試的函數
        result = get_user_data(42)
        
        # 驗證結果
        self.assertEqual(result["name"], "模擬用戶")
        
        # 驗證函數被調用
        mock_get_user_data.assert_called_once_with(42)

print("\n運行模擬測試:")
test_suite = unittest.TestLoader().loadTestsFromTestCase(TestWithMock)
test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)


# 總結
print("\n"+"="*50)
print("總結")
print("="*50)

print("良好的測試和文檔是高質量軟件的關鍵組成部分:")
print("1. 單元測試確保個別組件正確工作")
print("2. TDD幫助設計健壯的代碼")
print("3. 文檔幫助用戶和開發者理解代碼")
print("4. CI確保代碼質量始終保持在高水平")

print("\n最佳實踐:")
print("1. 測試應該獨立、可重現且自動化")
print("2. 文檔應該清晰、準確且最新")
print("3. 優先測試核心功能和容易出錯的部分")
print("4. 結合不同類型的測試以提高代碼質量")

