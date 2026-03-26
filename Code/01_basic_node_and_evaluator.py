import os
import sys

# Ensure the Code/ directory is on the path so `types` package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graph_types import Node, Variable, Constant, Add, ReLU

def evaluate(node: Node, feed_dict: dict):
    """
    模擬 Runtime 執行引擎 (Lazy Evaluation)
    遞迴走訪計算圖，代入真實數值並算出結果。
    """
    if isinstance(node, Variable):
        return feed_dict[node.name]
    elif isinstance(node, Constant):
        return node.value
    elif isinstance(node, Add):
        return evaluate(node.left, feed_dict) + evaluate(node.right, feed_dict)
    elif isinstance(node, ReLU):
        val = evaluate(node.input_node, feed_dict)
        return val if val > 0 else 0
    else:
        raise NotImplementedError(f"尚未支援的算子: {type(node)}")

if __name__ == "__main__":
    from visualizer import visualize_graph
    
    # ===== 測試代碼 =====
    
    # 建立計算圖： z = ReLU(x + y) + bias
    # 其中 x, y 是變數 (Variable)，bias 是常數 (Constant)
    print("--- 建立計算圖 ---")
    x = Variable("x", shape=(1,))
    y = Variable("y", shape=(1,))
    bias = Constant("bias", value=5.0, shape=(1,))
    
    # x + y
    add_node_1 = Add("x_plus_y", x, y)
    
    # ReLU(x + y)
    relu_node = ReLU("relu", add_node_1)
    
    # ReLU(x + y) + bias
    out_node = Add("output", relu_node, bias)
    
    print("計算圖建立完成！")
    
    # 準備 Runtime 需要的輸入資料 (feed_dict)
    feed_dict = {
        "x": 2.0,
        "y": -5.0
    }
    
    print("\n--- 執行 Runtime (Evaluator) ---")
    print(f"輸入資料: {feed_dict}")
    print(f"bias 常數值: {bias.value}")
    
    # 執行計算圖
    # 1. x + y = 2.0 + (-5.0) = -3.0
    # 2. ReLU(-3.0) = 0.0
    # 3. 0.0 + bias(5.0) = 5.0
    result = evaluate(out_node, feed_dict)
    
    # 可選：將計算完的結果註冊回節點 (為了能在視覺化工具中看到 Runtime 數值)
    # 這邊簡單模擬將 result 掛載到最終輸出節點
    out_node.value = result
    
    print(f"\n計算結果 (z): {result}")
    assert result == 5.0, f"計算錯誤！預期 5.0，但得到 {result}"
    print("測試通過！ ✅")
    
    print("\n--- 產生計算圖視覺化 (Netron-like) ---")
    visualize_graph(out_node, "Code/graph_output.html")
