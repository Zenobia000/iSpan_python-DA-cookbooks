# 更好的方式：使用類來管理狀態
class Counter:
    def __init__(self):
        self._count = 0
    
    def increment(self):
        self._count += 1
        return self._count
    
    def get_count(self):
        return self._count
    
    def reset(self):
        self._count = 0
        return self._count
