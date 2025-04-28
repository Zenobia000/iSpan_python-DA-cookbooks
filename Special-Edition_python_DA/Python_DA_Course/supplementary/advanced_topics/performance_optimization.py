# %% [markdown]
# # 🚀 數據分析效能優化技巧

# 本課程將介紹數據分析中的效能優化技巧，包括記憶體管理、運算加速、程式碼優化等進階主題。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 理解效能瓶頸
# - 🔄 學習記憶體優化
# - 🎨 掌握運算加速方法
# - 💡 實踐程式碼優化

# %%
# 環境設置
import numpy as np
import pandas as pd
import time
import memory_profiler
import psutil
import warnings
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
import gc

# 忽略警告
warnings.filterwarnings('ignore')

# %% [markdown]
# ## 1. 記憶體管理優化

# %%
def memory_usage_info():
    """顯示當前記憶體使用情況"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"記憶體使用情況：")
    print(f"- RSS (常駐集大小)：{memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"- VMS (虛擬記憶體大小)：{memory_info.vms / 1024 / 1024:.2f} MB")
    print(f"- 系統總記憶體：{psutil.virtual_memory().total / 1024 / 1024 / 1024:.2f} GB")
    print(f"- 系統可用記憶體：{psutil.virtual_memory().available / 1024 / 1024 / 1024:.2f} GB")

# %%
def optimize_dataframe_memory():
    """DataFrame 記憶體優化示例"""
    # 生成示例數據
    n_rows = 1000000
    df = pd.DataFrame({
        'id': range(n_rows),
        'float_col': np.random.random(n_rows),
        'int_col': np.random.randint(0, 100, n_rows),
        'category_col': np.random.choice(['A', 'B', 'C', 'D'], n_rows),
        'string_col': ['string_' + str(i) for i in range(n_rows)]
    })
    
    # 顯示優化前的記憶體使用
    print("優化前：")
    print(df.info(memory_usage='deep'))
    initial_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"總記憶體使用：{initial_memory:.2f} MB\n")
    
    # 優化數據類型
    df_optimized = df.copy()
    
    # 1. 將整數轉換為最小可用類型
    df_optimized['int_col'] = pd.to_numeric(df_optimized['int_col'], downcast='integer')
    
    # 2. 將浮點數轉換為最小可用類型
    df_optimized['float_col'] = pd.to_numeric(df_optimized['float_col'], downcast='float')
    
    # 3. 將字符類別轉換為category類型
    df_optimized['category_col'] = df_optimized['category_col'].astype('category')
    
    # 顯示優化後的記憶體使用
    print("優化後：")
    print(df_optimized.info(memory_usage='deep'))
    optimized_memory = df_optimized.memory_usage(deep=True).sum() / 1024 / 1024
    print(f"總記憶體使用：{optimized_memory:.2f} MB")
    print(f"節省記憶體：{initial_memory - optimized_memory:.2f} MB")
    print(f"優化比例：{((initial_memory - optimized_memory) / initial_memory * 100):.2f}%")
    
    return df_optimized

# %%
def chunk_processing_example():
    """分塊處理大數據示例"""
    # 創建大型數據文件
    n_rows = 1000000
    chunk_size = 100000
    
    df = pd.DataFrame({
        'value': np.random.random(n_rows),
        'group': np.random.choice(['A', 'B', 'C'], n_rows)
    })
    
    # 保存為 CSV 文件
    df.to_csv('large_file.csv', index=False)
    
    # 一次性讀取處理
    start_time = time.time()
    result_full = pd.read_csv('large_file.csv')['value'].mean()
    full_time = time.time() - start_time
    print(f"一次性處理時間：{full_time:.2f} 秒")
    
    # 分塊處理
    start_time = time.time()
    chunk_means = []
    chunk_weights = []
    
    for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
        chunk_means.append(chunk['value'].mean())
        chunk_weights.append(len(chunk))
    
    # 計算加權平均
    result_chunk = np.average(chunk_means, weights=chunk_weights)
    chunk_time = time.time() - start_time
    print(f"分塊處理時間：{chunk_time:.2f} 秒")
    
    print(f"\n結果比較：")
    print(f"一次性處理結果：{result_full:.6f}")
    print(f"分塊處理結果：{result_chunk:.6f}")
    print(f"效能提升：{((full_time - chunk_time) / full_time * 100):.2f}%")

# %% [markdown]
# ## 2. 運算加速優化

# %%
def parallel_processing_example():
    """並行處理示例"""
    def heavy_computation(x):
        """模擬耗時計算"""
        time.sleep(0.1)  # 模擬耗時操作
        return x ** 2
    
    data = list(range(100))
    
    # 串行處理
    start_time = time.time()
    serial_result = [heavy_computation(x) for x in data]
    serial_time = time.time() - start_time
    print(f"串行處理時間：{serial_time:.2f} 秒")
    
    # 多進程處理
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        parallel_result = list(executor.map(heavy_computation, data))
    parallel_time = time.time() - start_time
    print(f"並行處理時間：{parallel_time:.2f} 秒")
    
    print(f"加速比：{serial_time / parallel_time:.2f}x")

# %%
def vectorization_example():
    """向量化運算示例"""
    n = 1000000
    data = np.random.random(n)
    
    # 使用循環
    start_time = time.time()
    result_loop = []
    for x in data:
        result_loop.append(np.sin(x) + np.cos(x))
    loop_time = time.time() - start_time
    print(f"循環處理時間：{loop_time:.4f} 秒")
    
    # 使用向量化
    start_time = time.time()
    result_vector = np.sin(data) + np.cos(data)
    vector_time = time.time() - start_time
    print(f"向量化處理時間：{vector_time:.4f} 秒")
    
    print(f"加速比：{loop_time / vector_time:.2f}x")
    
    # 驗證結果
    print("\n結果驗證：")
    print(f"循環結果前5個元素：{result_loop[:5]}")
    print(f"向量化結果前5個元素：{result_vector[:5]}")
    print(f"結果是否相同：{np.allclose(result_loop, result_vector)}")

# %% [markdown]
# ## 3. 程式碼優化技巧

# %%
def code_optimization_examples():
    """程式碼優化示例"""
    # 1. 列表推導式 vs 循環
    start_time = time.time()
    result_loop = []
    for i in range(1000000):
        if i % 2 == 0:
            result_loop.append(i ** 2)
    loop_time = time.time() - start_time
    
    start_time = time.time()
    result_comprehension = [i ** 2 for i in range(1000000) if i % 2 == 0]
    comprehension_time = time.time() - start_time
    
    print("1. 列表推導式 vs 循環：")
    print(f"循環時間：{loop_time:.4f} 秒")
    print(f"推導式時間：{comprehension_time:.4f} 秒")
    print(f"加速比：{loop_time / comprehension_time:.2f}x\n")
    
    # 2. 集合操作 vs 列表操作
    data = list(range(1000000))
    search_items = list(range(500000, 1500000))
    
    start_time = time.time()
    result_list = [x for x in search_items if x in data]
    list_time = time.time() - start_time
    
    start_time = time.time()
    data_set = set(data)
    result_set = [x for x in search_items if x in data_set]
    set_time = time.time() - start_time
    
    print("2. 集合操作 vs 列表操作：")
    print(f"列表操作時間：{list_time:.4f} 秒")
    print(f"集合操作時間：{set_time:.4f} 秒")
    print(f"加速比：{list_time / set_time:.2f}x\n")
    
    # 3. 字典查找 vs 條件判斷
    data = list(range(1000000))
    
    start_time = time.time()
    result_if = []
    for x in data:
        if x % 3 == 0:
            result_if.append('fizz')
        elif x % 5 == 0:
            result_if.append('buzz')
        else:
            result_if.append(str(x))
    if_time = time.time() - start_time
    
    lookup = {0: 'fizz', 1: str(1), 2: str(2)}
    start_time = time.time()
    result_dict = [lookup.get(x % 3, str(x)) for x in data]
    dict_time = time.time() - start_time
    
    print("3. 字典查找 vs 條件判斷：")
    print(f"條件判斷時間：{if_time:.4f} 秒")
    print(f"字典查找時間：{dict_time:.4f} 秒")
    print(f"加速比：{if_time / dict_time:.2f}x")

# %% [markdown]
# ## 4. 效能監控與分析

# %%
def performance_monitoring():
    """效能監控示例"""
    @memory_profiler.profile
    def memory_intensive_function():
        """記憶體密集型函數"""
        # 創建大型數據
        data = [i ** 2 for i in range(1000000)]
        # 進行一些操作
        result = sum(data)
        return result
    
    print("記憶體使用分析：")
    result = memory_intensive_function()
    
    # CPU 使用率監控
    print("\nCPU 使用率監控：")
    print(f"CPU 核心數：{psutil.cpu_count()}")
    print(f"CPU 使用率：{psutil.cpu_percent(interval=1)}%")
    
    # 記憶體使用監控
    print("\n記憶體使用監控：")
    memory_usage_info()

# %% [markdown]
# ## 5. 最佳實踐建議

# 在進行數據分析效能優化時，請注意以下最佳實踐原則：

# 1. **記憶體管理**
#    - 使用適當的數據類型
#    - 及時釋放不需要的資源
#    - 採用分塊處理大數據

# 2. **運算優化**
#    - 善用向量化運算
#    - 適當使用並行處理
#    - 避免不必要的計算

# 3. **程式碼優化**
#    - 使用高效的數據結構
#    - 採用優化的算法
#    - 避免重複計算

# 4. **效能監控**
#    - 定期監控資源使用
#    - 識別效能瓶頸
#    - 及時進行優化

# %% [markdown]
# ## 6. 總結

# 本課程介紹了數據分析效能優化的核心概念：

# - **記憶體優化**：有效管理記憶體資源
# - **運算加速**：提升計算效能
# - **程式碼優化**：改進程式碼品質
# - **效能監控**：追蹤資源使用
# - **最佳實踐**：遵循優化原則 