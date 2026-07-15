import time
import requests

from datetime import datetime


from get_temp import get_environment_and_ac_state
from operate import operation_program
from judge import statistical_model  

# スプレッドシート（GAS）のWebアプリURL
GAS_SETTINGS_URL = "Web_App_URL"
def get_automation_status():
    """GAS経由でスプレッドシートの「設定」シートから自動化のON/OFFを取得する"""
    print("GASから自動化モードの状態を取得しています...")
    try:
        params = {"action": "get_status"}
        response = requests.get(GAS_SETTINGS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "automation_on" in data:
            return data["automation_on"]
        else:
            print(f"状態取得エラー: {data.get('message', '不明なエラー')}")
            return False

    except Exception as e:
        print(f"GASへの通信に失敗しました: {e}")
        return False

# ==========================================
# 実行管理プログラム本体
# =========================================
def execution_management_program():
    INTERVAL_SECONDS = 30

    print("=== 実行管理プログラムを起動しました ===")
    print(f"実行間隔: {INTERVAL_SECONDS / 60}分\n")

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- 実行時刻: {current_time} ---")

        # 0. 自動化状態の取得
        automation_on = get_automation_status()
        print(f"現在の自動化モード: {'ON' if automation_on else 'OFF'}")

        # 1. データ取得
        temp, humidity, ac_state = get_environment_and_ac_state()

        if temp is not None and ac_state is not None:
            # 2. 推論 
            judgment = statistical_model(temp, humidity)
            print(f"推論結果: {judgment}")

            # 3. 操作とログ送信
            operation_program(judgment, automation_on, ac_state, temp, humidity)
        else:
            print("データの取得に失敗したため、今回の処理をスキップします。")

        print(f"-> 次回の実行は{INTERVAL_SECONDS / 60}分後です。")
        time.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    try:
        execution_management_program()
    except KeyboardInterrupt:
        print("\nプログラムが手動で停止されました。")