from .nodes import Node


class Add(Node):
    """
    加法算子 (element-wise addition).
    要求兩個輸入的 shape 相同 (暫不支援 Broadcasting)。
    """

    def __init__(self, name: str, left: Node, right: Node):
        super().__init__(name)
        self.inputs = [left, right]
        self.left = left
        self.right = right


class ReLU(Node):
    """
    ReLU 激活函數 (element-wise).
    輸出 shape 與輸入相同。
    """

    def __init__(self, name: str, input_node: Node):
        super().__init__(name)
        self.inputs = [input_node]
        self.input_node = input_node
