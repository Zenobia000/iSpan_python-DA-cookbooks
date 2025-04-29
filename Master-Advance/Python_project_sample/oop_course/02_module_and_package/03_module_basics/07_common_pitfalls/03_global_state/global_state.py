# 不良示例：使用全局變數
counter = 0

def increment():
    global counter
    counter += 1
    return counter

def get_counter():
    return counter

def reset_counter():
    global counter
    counter = 0


if __name__ == "__main__":
    print("初始狀態:", get_counter())
    print("增加一次:", increment())
    print("再增加:", increment())
    print("當前狀態:", get_counter())
    print("重置:", reset_counter())
    print("最終狀態:", get_counter())
