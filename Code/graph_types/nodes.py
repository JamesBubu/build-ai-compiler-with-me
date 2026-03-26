from typing import Any, Optional


class Node:
    """所有計算圖節點的基礎類別 (Base class for all compute graph nodes)"""

    def __init__(self, name: str):
        self.name = name
        self.inputs: list["Node"] = []
        self.value: Any = None
        self.shape: Optional[tuple] = None


class Variable(Node):
    """
    變數節點，代表模型的符號輸入 (e.g. feature tensors).
    在編譯期 (compile time) 只知道 shape，沒有真實數值。
    """

    def __init__(self, name: str, shape: Optional[tuple] = None):
        super().__init__(name)
        self.shape = shape


class Constant(Node):
    """
    常數節點，代表固定的數值 (e.g. 權重 weights, 偏置 bias).
    同時持有 shape 與實際 value。
    """

    def __init__(self, name: str, shape: Optional[tuple] = None, value: Any = None):
        super().__init__(name)
        self.shape = shape
        self.value = value
