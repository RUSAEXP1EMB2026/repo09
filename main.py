import time
import schedule

# 💡 別のpyファイルから、必要な関数をインポート（呼び出し）する
from remo_api import get_environment_data
from ai_model import predict_discomfort_status
from ac_control import request_air_conditioner_control
from logger import send_execution_log

# 自動化状態の管理
IS_AUTOMATION_ON = True 

def main_job():
    print("\n==============================================")
    print(f"定期タイマー起動: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("==============================================")
    
    try:
        # 1. remo_api.py の関数を呼び出して温湿度を取得 [cite: 35]
        temp, humid = get_environment_data()
        
        # 2. ai_model.py の関数を呼び出して判定 [cite: 37]
        prediction = predict_discomfort_status(temp, humid)
        
        # 3. ac_control.py の関数を呼び出してエアコン操作（ON/OFF状態を渡す） [cite: 40]
        request_air_conditioner_control(prediction, IS_AUTOMATION_ON)
        
        # 4. logger.py の関数を呼び出して、GASのスプレッドシート書き込みへ送信 [cite: 42]
        send_execution_log(temp, humid, prediction)
        
        print("\n15分おきの定期処理が正常に完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    print("スマートエアコン制御システム 起動")
    schedule.every(15).minutes.do(main_job)
    
    # テスト用（起動直後に1回実行）
    main_job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)