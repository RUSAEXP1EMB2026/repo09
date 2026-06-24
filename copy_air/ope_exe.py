import time
from datetime import datetime

# ==========================================
# 外部ファイルの読み込み（合体！）
# ==========================================
from get_temp import get_environment_and_ac_state
from operate import operation_program

# ==========================================
# 未作成プログラム（今回はダミーのまま）
# ==========================================
def statistical_model(temp, humidity):
    """統計モデル（ダミー）"""
    print(f"【統計モデル】温度{temp}℃、湿度{humidity}%から体感を推論中...")
    if temp >= 28.0:
        return "暑い"
    elif temp <= 22.0:
        return "寒い"
    else:
        return "快適"

# ==========================================
# 実行管理プログラム本体
# ==========================================
def execution_management_program():
    automation_on = True

    # テスト時は待ち時間を 10 などの短い秒数にするとすぐ確認できます
    INTERVAL_SECONDS = 900

    print("=== 実行管理プログラムを起動しました ===")
    print(f"自動化モード: {'ON' if automation_on else 'OFF'}")
    print(f"実行間隔: {INTERVAL_SECONDS / 60}分\n")

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- 実行時刻: {current_time} ---")

        # 1. データ取得（get_temp.pyから呼び出し）
        temp, humidity, ac_state = get_environment_and_ac_state()

        if temp is not None and ac_state is not None:
            # 2. 推論
            judgment = statistical_model(temp, humidity)
            print(f"推論結果: {judgment}")

            # 3. 操作とログ送信（operate.pyから呼び出し。温度・湿度も渡す）
            operation_program(judgment, automation_on, ac_state, temp, humidity)
        else:
            print("データの取得に失敗したため、今回の処理をスキップします。")

        print(f"-> 次回の実行は{INTERVAL_SECONDS / 60}分後です。")
        time.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    try:
        execution_management_program()
    except KeyboardInterrupt:
        print("\nプログラムが手動で（Ctrl+Cなどにより）停止されました。")