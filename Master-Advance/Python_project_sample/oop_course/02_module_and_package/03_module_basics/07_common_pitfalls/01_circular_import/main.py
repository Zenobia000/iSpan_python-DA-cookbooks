print("=== 循環導入問題示範 ===")
print("這個示例展示了循環導入的問題")
print("當我們嘗試運行這個程式時，會看到錯誤")

try:
    from circular_a import a_function
    from circular_b import b_function
    
    a_function()
    b_function()
except Exception as e:
    print("\n發生錯誤:")
    print(f"錯誤類型: {type(e).__name__}")
    print(f"錯誤訊息: {str(e)}")
    
print("\n解決方案:")
print("1. 重構代碼，避免循環依賴")
print("2. 將導入語句移到函數內部")
print("3. 使用依賴注入的設計模式")
