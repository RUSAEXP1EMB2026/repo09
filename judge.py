import pandas as pd
import requests
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

# ==========================================
# 1. Googleの鍵なしでスプレッドシートを強制読み込み
# ==========================================
# あなたのスプレッドシートのURLに書き換えてください！
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YmnRv4Tb193kPnGcdSPfs1BXbj3VPmeRM5Q7PowQ680/edit?gid=0#gid=0"

# URLをCSVダウンロード用のアドレスに一瞬で変換するコード
sheet_id = SPREADSHEET_URL.split("/d/")[1].split("/")[0]
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

print("スプレッドシートからデータを取得中...")

# ==========================================
# 2. K近傍法（k-NN）による学習
# ==========================================
# 1行目（見出し）がおかしいので、読み込み方を少し変えます
df = pd.read_csv(csv_url, header=0)

# 文字での検索をやめて、C言語の配列のように「列番号（0スタート）」で直接データを引っこ抜きます
# [全行, [温度の列番号, 湿度の列番号]]
X_train = df.iloc[:, [1, 2]] 

# [全行, 体感ラベルの列番号]
y_train = df.iloc[:, 3]

scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)

# スプレッドシートから読み込めた実際のデータ件数を取得
data_count = len(X_train)

# データが3件未満の場合は、クラッシュを防ぐためにKの値をデータ件数に合わせる（最低1）
k_value = min(3, max(1, data_count))

print(f"現在のデータ件数: {data_count}件 (k={k_value} で判定します)")
knn = KNeighborsClassifier(n_neighbors=k_value)

knn.fit(X_train_scaled, y_train)
print("AIの学習が完了しました。")

# ==========================================
# 3. 今のデータで判定（実機想定：28.0度、65%）
# ==========================================
current_temp = 28.0
current_hum = 65.0

X_new = pd.DataFrame({'温度': [current_temp], '湿度': [current_hum]})
X_new_scaled = scaler.transform(X_new)

predicted_label = knn.predict(X_new_scaled)[0]
print(f"【判定結果】温度: {current_temp}℃ / 湿度: {current_hum}% ➔ 予測: {predicted_label}")

# ==========================================
# 4. 結果をスプレッドシートに書き戻す（GASのAPIを叩く）
# ==========================================
# ※もし黒川さんが手動操作用のGASのWebアプリURL（マクロURL）を作ってくれていたら、
# そこに予測結果をPOST（送信）するだけで書き込みが完了します。
#
# gas_url = "https://script.google.com/macros/s/XXXXX/exec"
# requests.post(gas_url, json={"temp": current_temp, "hum": current_hum, "predict": predicted_label})