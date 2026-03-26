import os
import sys

# Ensure the Code/ directory is on the path so packages are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualizer import visualize_graph
from graph_types import Node, Variable, Constant, Add, ReLU

# ---------------------------------------------------------
# Compiler Pass 1: 形狀推導 (Shape Derivation)
# ---------------------------------------------------------
def shape_inference_pass(node: Node):
    """
    這是一個 Compiler Pass (編譯期優化)。
    它會在【不輸入真實數據】的情況下，利用計算圖本身的依賴關係推導出所有節點的 Shape。
    這對於底層預先配置記憶體 (Memory Allocation) 非常重要。
    """
    
    # 1. 遞迴走訪：先確保依賴的輸入節點都已經推導出 Shape 了
    for inp in node.inputs:
        if getattr(inp, 'shape', None) is None:
            shape_inference_pass(inp)

    # 2. 根據目前節點的運算邏輯，推導出自己的 Shape
    if isinstance(node, (Variable, Constant)):
        # 變數或常數在初始化的時候就已經被賦予 Shape 了，所以不用做任何事
        pass 
        
    elif isinstance(node, Add):
        # 簡化版邏輯：要求左右兩邊的矩陣形狀必須一模一樣 (暫不實作 Broadcasting 廣播機制)
        if node.left.shape != node.right.shape:
            raise ValueError(f"Shape Error! Node '{node.name}' 輸入形狀不匹配：左側為 {node.left.shape}，右側為 {node.right.shape}")
        
        # 加法運算輸出的矩陣形狀與輸入相同
        node.shape = node.left.shape 
        print(f"✅ Pass 推導：節點 '{node.name}' (Add) 的 shape 為: {node.shape}")
        
    elif isinstance(node, ReLU):
        # ReLU 是一種 element-wise 操作，不會改變輸入矩陣的形狀
        node.shape = node.input_node.shape
        print(f"✅ Pass 推導：節點 '{node.name}' (ReLU) 的 shape 為: {node.shape}")

# ---------------------------------------------------------
# 主程式測試區
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== [準備階段] 建立具有預期 Shape 的藍圖 (計算圖) ===")
    
    # 建立計算圖 (注意：我們給了 Shape，但沒有給真實數據 value!)
    x = Variable("x", shape=(1, 128))                   # 代表 batch_size=1, features=128 的特徵向量
    bias = Constant("bias", shape=(1, 128), value=None) # 加法偏置項，目前不在乎實際數值
    
    # 建構運算關係: ReLU(x + bias)
    add_node = Add("x_plus_bias", x, bias)
    relu_node = ReLU("output", add_node)
    
    print("藍圖建立完成！準備進入 Compiler 解析階段。")
    print(f"\n最初，算子的形狀是未知的:")
    print(f"- Add Node ('{add_node.name}') shape: {add_node.shape}")
    print(f"- ReLU Node ('{relu_node.name}') shape: {relu_node.shape}\n")
    
    print("=== [編譯期 Compile Time] 執行 Compiler Pass: Shape Inference ===")
    # 在執行引擎 (Evaluator) 提供真實運算數據之前運行 Compiler Pass！
    shape_inference_pass(relu_node)
    
    print("\n=== [結果展示] 通過 Pass 之後的信息收集 ===")
    print(f"最終輸出節點 '{relu_node.name}' 的 Shape 是: {relu_node.shape}")
    
    print("\n💡 觀察重點：")
    print("我們完全沒有傳入任何 feed_dict 真實數據，也沒有進行真正的加減運算！")
    print("但 Compiler 藉由走訪藍圖的輸入關係，成功預測出 `relu_node` 需要一塊 (1, 128) 大小的記憶體。")
    print("這就是 AI Compiler 前端最核心、也是最初始的工作之一。")
    
    # 運用視覺化腳本畫出帶有 shape 資訊的圖
    # 我們這邊簡單把 shape 塞進 value 屬性裡，好讓視覺化腳本直接顯示出來觀察
    add_node.value = f"shape={add_node.shape}"
    relu_node.value = f"shape={relu_node.shape}"
    x.value = f"shape={x.shape}"
    bias.value = f"shape={bias.shape}"
    
    print("\n--- 產生計算圖視覺化 (Netron-like) ---")
    visualize_graph(relu_node, "Code/shape_inference_graph.html")
