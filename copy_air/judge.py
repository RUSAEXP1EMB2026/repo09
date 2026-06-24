import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

# ==========================================
# 設定: スプレッドシートのURL
# ==========================================
# 教師データが入っているスプレッドシートのURLに書き換えてください
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1YmnRv4Tb193kPnGcdSPfs1BXbj3VPmeRM5Q7PowQ680/edit?gid=973525101#gid=973525101"


def statistical_model(current_temp, current_hum):
    """
    現在の温度と湿度を受け取り、スプレッドシートの教師データから
    k-NN（K近傍法）を用いて体感を推論して返す関数
    """
    print("【統計モデル】スプレッドシートから最新の教師データを取得中...")

    try:
        # URLをCSVダウンロード用のアドレスに変換
        sheet_id = SPREADSHEET_URL.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"

        # データを取得
        df = pd.read_csv(csv_url, header=0)

        # データが1件もない場合の安全対策
        if len(df) < 1:
            print("【警告】教師データが空です。安全のため「快適」判定とします。")
            return "快適"

        # 特徴量（温度、湿度）とターゲット（体感ラベル）の抽出
        X_train = df.iloc[:, [1, 2]]
        y_train = df.iloc[:, 3]

        # データの正規化
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        # Kの値をデータ件数に合わせて調整（最大3、最小1）
        data_count = len(X_train)
        k_value = min(3, max(1, data_count))
        print(f"-> {data_count}件のデータで学習完了 (k={k_value})")

        # モデルの構築と学習
        knn = KNeighborsClassifier(n_neighbors=k_value)
        knn.fit(X_train_scaled, y_train)

        # 取得した現在の温度・湿度を推論にかける
        X_new = pd.DataFrame({'温度': [current_temp], '湿度': [current_hum]})
        X_new_scaled = scaler.transform(X_new)
        predicted_label = knn.predict(X_new_scaled)[0]

        return predicted_label

    except Exception as e:
        print(f"【統計モデル エラー】データの読み込みや判定に失敗しました: {e}")
        # システムを止めないための安全策として「快適（現状維持）」を返す
        return "快適"


# 単体テスト用ブロック
if __name__ == '__main__':
    print("単体テストを実行します...")
    result = statistical_model(28.0, 65.0)
    print(f"テスト判定結果: {result}")