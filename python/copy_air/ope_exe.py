import time
from datetime import datetime


# ==========================================
# 外部プログラムの読み込み（イメージ）
# 実際はこれまでに作成した関数をここに統合するか、
# 別ファイルから import して使用します。
# ==========================================
# from data_fetcher import get_environment_and_ac_state
# from operator_program import operation_program

def get_environment_and_ac_state():
    """データ取得プログラム（先ほど作成したもの）"""
    # テストが動くように、仮のデータを返すようにしています。
    # 実際は先ほど作成した関数をそのまま使用してください。
    return 28.5, 60.0, {'power': 'on', 'mode': 'cool', 'temp': 27}


def operation_program(judgment, automation_on, current_ac_state):
    """操作プログラム（最初に作成したもの）"""
    # 実際は最初に作成したGASへ通信する関数を使用してください。
    print(f"【操作プログラム実行】判定:{judgment} / 自動化:{'ON' if automation_on else 'OFF'}")


# ==========================================
# 未作成プログラムのダミー
# ==========================================
def statistical_model(temp, humidity):
    """
    統計モデル（ダミー）
    本来はスプレッドシートの教師データを基にAIが判定しますが、
    今回はシステム全体をテストするため、温度の数値だけで簡易判定します。
    """
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
    # 自動化のON/OFF状態
    # （本来はLINEからの指示により、GAS経由で状態が書き換わります）
    automation_on = True

    # 実行間隔（15分 = 900秒）
    INTERVAL_SECONDS = 900

    print("=== 実行管理プログラムを起動しました ===")
    print(f"自動化モード: {'ON' if automation_on else 'OFF'}")
    print(f"実行間隔: {INTERVAL_SECONDS / 60}分\n")

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"--- 実行時刻: {current_time} ---")

        # 1. データ取得プログラムへ指示
        temp, humidity, ac_state = get_environment_and_ac_state()

        if temp is not None and ac_state is not None:
            # 2. 取得したデータを統計モデルへ渡し、判定を得る
            judgment = statistical_model(temp, humidity)
            print(f"推論結果: {judgment}")

            # 3. 判定結果とエアコン状態を操作プログラムへ渡し、操作を依頼する
            operation_program(judgment, automation_on, ac_state)
        else:
            print("データの取得に失敗したため、今回の処理をスキップします。")

        print(f"-> 次回の実行は{INTERVAL_SECONDS / 60}分後です。\n")

        # 指定した秒数だけプログラムを待機（スリープ）させる
        # ※テストですぐに動作を確認したい場合は、`INTERVAL_SECONDS` を 5 などに変更してください。
        time.sleep(INTERVAL_SECONDS)


if __name__ == '__main__':
    # 実行
    try:
        execution_management_program()
    except KeyboardInterrupt:
        print("\nプログラムが手動で停止されました。")