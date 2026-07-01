import requests

# ==========================================
# 設定情報の入力
# ==========================================
# デプロイしたGAS（スプレッドシート書き込みプログラム）のWebアプリURLを設定します
GAS_LOG_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbwt5W0Ix-2Txgvlh0vIoqCzGrt9J-Hc-h7B2FOa8w0KvlN5lBJb9lCBkJYKOEg8QBYJ/exec"


def send_log_program(temp, humidity, judgment, action_taken=None, automation_on=None):
    """
    ログ送信プログラム
    取得した環境データとAIの判定結果をまとめ、GASへ記録依頼を送信する。
    """
    print("【ログ送信プログラム】スプレッドシートへ記録依頼を準備中...")

    # GAS側の仕様に合わせたJSONデータ
    log_data = {
        "type": "log",  # GAS側で「稼働状況ログ」シートに振り分けるための指定
        "temperature": temp,  # 温度
        "humidity": humidity,  # 湿度
        "label": judgment  # AIの判定結果（暑い/快適/寒い）
    }

    try:
        # GASのURLへPOSTリクエストでデータを送信
        response = requests.post(GAS_LOG_WEBAPP_URL, json=log_data)
        response.raise_for_status()

        # GASからの返答（作成いただいた createResponse の内容）を確認
        result = response.json()
        if result.get("status") == "success":
            print("-> GASへのログ送信とスプレッドシートへの書き込みが完了しました！")
        else:
            print(f"-> GAS側でエラーが発生しました: {result.get('message')}")

    except Exception as e:
        print(f"-> GASへの通信に失敗しました: {e}")
