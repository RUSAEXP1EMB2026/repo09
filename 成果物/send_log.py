import requests

# ==========================================
# 設定情報の入力
# ==========================================
# デプロイしたGASのWebアプリURLを設定
GAS_LOG_WEBAPP_URL = "Web_App_URL"


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

        # GASからの返答を確認
        result = response.json()
        if result.get("status") == "success":
            print("-> GASへのログ送信とスプレッドシートへの書き込みが完了しました！")
        else:
            print(f"-> GAS側でエラーが発生しました: {result.get('message')}")

    except Exception as e:
        print(f"-> GASへの通信に失敗しました: {e}")


# ==========================================
# テスト実行用のブロック
# ==========================================
if __name__ == '__main__':
    print("=== ログ送信プログラムのテストを開始します ===\n")

    print("【テスト】稼働状況ログの送信")
    send_log_program(
        temp=28.5,
        humidity=60.0,
        judgment="暑い"
    )