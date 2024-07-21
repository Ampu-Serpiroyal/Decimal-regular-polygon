import tkinter as tk
import math

def draw_polygon():
    try:
        a = entry.get().strip()  # 前後の空白を除去
        if not a.replace('.', '', 1).isdigit():  # 小数点を1つまで含めた場合、数字でない場合のエラー処理
            raise ValueError("数字を入力してください。")

        a = float(a)  # 浮動小数点数に変換
        if a <= 2:
            raise ValueError("2より大きい有理数を入力してください。")
        
        # aを分数n/mに変換
        numerator = a
        denominator = 1
        while not math.isclose(numerator % 1, 0):  # 小数がなくなるまで繰り返す
            numerator *= 10
            denominator *= 10
        gcd_value = math.gcd(int(numerator), denominator)
        n = int(numerator / gcd_value)
        m = int(denominator / gcd_value)
        
        canvas.delete("all")  # キャンバスの内容をクリア

        center_x = 300
        center_y = 300
        radius = 280
        angle_increment = 2 * math.pi * m / n  # 円をm周分をn等分するための内角

        points = []
        for i in range(n):  # n回繰り返す
            angle = i * angle_increment
            x = center_x + radius * math.cos(angle)  # 座標の計算
            y = center_y + radius * math.sin(angle)
            points.append((x, y))

        # 初期のポリゴンを描画
        polygon_item = canvas.create_polygon(points, outline='yellow', fill='', width=2) 
        vertex_label.config(text=f"頂点: {n}個, 一つの内角: {180 - 360 * m / n:.2f}度")    # 頂点の座標

        # 回転
        def rotate_polygon():  # ポリゴンを回転
            nonlocal points
            angle_increment = math.radians(1)  # 1度ずつ回転させる
            rotated_points = []    # 座標を保存
            for x, y in points:
                # 中心を原点として回転行列を適用
                rotated_x = center_x + (x - center_x) * math.cos(angle_increment) - (y - center_y) * math.sin(angle_increment)
                rotated_y = center_y + (x - center_x) * math.sin(angle_increment) + (y - center_y) * math.cos(angle_increment)
                rotated_points.append((rotated_x, rotated_y))
            points = rotated_points   # 回転後の座標
            canvas.coords(polygon_item, *sum(points, ()))  # 新しい座標でポリゴンを更新
            canvas.after(40, rotate_polygon)  # 40ミリ秒後に再び回転の計算をする

        # 初回の回転を開始
        rotate_polygon()

    except ValueError as e:
        status_label.config(text=str(e))

# Tkinterウィンドウの作成
root = tk.Tk()
root.title("正n角形の作図")

# キャンバスの設定
canvas = tk.Canvas(root, width=600, height=600, bg='black')
canvas.pack(padx=10, pady=10)

# 入力フレームの設定
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

label = tk.Label(input_frame, text="数を入力してください（小数も可）:")
label.grid(row=0, column=0)

entry = tk.Entry(input_frame)
entry.grid(row=0, column=1)

button = tk.Button(input_frame, text="作図", command=draw_polygon)
button.grid(row=0, column=2, padx=10)

# 状態の表示
status_label = tk.Label(root, text="", fg="red")
status_label.pack()

# 頂点数の表示
vertex_label = tk.Label(root, text="頂点: 0個, 一つの内角: 0.00度")
vertex_label.pack()

root.mainloop()
