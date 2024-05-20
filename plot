import matplotlib.pyplot as plt

# テキストファイルから数値データを読み取る関数
def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # 各行の数値を読み取ってリストに追加
                number = float(line.strip())
                data.append(number)
            except ValueError:
                # 数値に変換できない場合はスキップ
                continue
    return data

# 指定された条件に基づいてカウントする関数
def count_differences_within_threshold(data, threshold=10):
    count = 0
    for i in range(1, len(data)):
        if abs(data[i] - data[i - 1]) <= threshold:
            count += 1
    return count

# データファイルのパス
file_path = 'test.txt'

# ファイルからデータを読み取る
data = read_data_from_file(file_path)

# 指定された条件に基づいてカウントを計算
count = count_differences_within_threshold(data)

# 全体のデータの要素数で割り、割合を計算
percentage = (count / (len(data) - 1)) * 100 if len(data) > 1 else 0

# 結果を出力
print(f"数値の差が10以内であった数: {count}")
print(f"全体のデータの要素数: {len(data)}")
print(f"全体の中での割合: {percentage:.2f}%")

# データポイントのインデックスをx軸に使用
x = list(range(len(data)))

# 棒グラフの作成
plt.figure(figsize=(20, 10))
plt.bar(x, data, color='skyblue')

# グラフのタイトルとラベルの設定
plt.title('Number Sequence Bar Graph')
plt.xlabel('Index')
plt.ylabel('Value')

# グリッドの表示
plt.grid(True)

# グラフの表示
plt.show()

