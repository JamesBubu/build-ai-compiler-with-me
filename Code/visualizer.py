import os
import webbrowser
import json

def visualize_graph(root_node, output_file="graph.html"):
    """
    將計算圖轉換為 HTML 視覺化檔案，並自動在瀏覽器中開啟。
    不需要安裝任何額外套件，使用 CDN 載入 vis.js 繪圖。
    """
    nodes_data = []
    edges_data = []
    visited = set()

    def traverse(node):
        if id(node) in visited:
            return
        visited.add(id(node))
        
        # 決定節點的顏色與形狀
        node_type = node.__class__.__name__
        color = "#97C2FC" # 預設藍色
        shape = "box"
        
        if node_type == "Variable":
            color = "#FB7E81" # 紅色
            shape = "ellipse"
        elif node_type == "Constant":
            color = "#C2FABC" # 綠色
            shape = "ellipse"
        elif node_type in ["Add", "ReLU"]:
            color = "#FFA807" # 橘色
            
        # 顯示名稱與類型
        label = f"{node.name}\n({node_type})"
        if hasattr(node, 'value'):
            label += f"\nval: {node.value}"
            
        nodes_data.append({
            "id": id(node),
            "label": label,
            "color": color,
            "shape": shape
        })

        # 建立邊 (Edge)，方向從 input 指向目前節點
        for inp in node.inputs:
            edges_data.append({
                "from": id(inp),
                "to": id(node),
                "arrows": "to" # 箭頭指向當前節點 (資料流方向)
            })
            traverse(inp) # 遞迴走訪輸入節點

    # 開始走訪圖結構
    traverse(root_node)

    # 將 Python 字典轉換為 JSON 字串，放入 HTML 中
    nodes_json = json.dumps(nodes_data)
    edges_json = json.dumps(edges_data)

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Compiler Graph Visualizer</title>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style type="text/css">
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }}
            #mynetwork {{
                width: 100vw;
                height: 100vh;
                border: 1px solid lightgray;
                background-color: #ffffff;
            }}
            #title {{
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 100;
                background: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div id="title">
            <h3>Computational Graph (Netron-like)</h3>
            <p>🔴 Variable, 🟢 Constant, 🟠 Operator</p>
        </div>
        <div id="mynetwork"></div>

        <script type="text/javascript">
            // 從 Python 導入的資料
            var nodes = new vis.DataSet({nodes_json});
            var edges = new vis.DataSet({edges_json});

            // 取得容器
            var container = document.getElementById('mynetwork');

            // 將資料放入 vis-network
            var data = {{
                nodes: nodes,
                edges: edges
            }};
            
            // 設定圖形選項
            var options = {{
                layout: {{
                    hierarchical: {{
                        direction: 'UD', // Up to Down
                        sortMethod: 'directed',
                        nodeSpacing: 150,
                        levelSeparation: 150
                    }}
                }},
                physics: false, // 關閉物理引擎讓排版更固定 (類似 Netron)
                nodes: {{
                    font: {{
                        size: 14,
                        face: 'Arial'
                    }},
                    borderWidth: 2
                }},
                edges: {{
                    width: 2,
                    color: {{ inherit: 'from' }},
                    smooth: {{
                        type: 'cubicBezier',
                        forceDirection: 'vertical',
                        roundness: 0.4
                    }}
                }}
            }};

            // 初始化網絡圖
            var network = new vis.Network(container, data, options);
        </script>
    </body>
    </html>
    """

    # 寫入目標檔案
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"圖形視覺化檔案已生成: {output_file}")
    
    # 自動用瀏覽器打開
    file_path = os.path.abspath(output_file)
    webbrowser.open(f"file://{file_path}")
