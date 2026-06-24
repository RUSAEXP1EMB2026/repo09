import requests
from send_log import send_log_program  # 追加：ログ送信プログラムを読み込む

GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbw5RftIai-nGH1XkG_E8LuDDj4RORjzj_VURanZ-GIGxvsJB0ej4aUQptiVJifoVHZO/exec"


# 引数に temp と humidity を追加
def operation_program(judgment, automation_on, current_ac_state, temp, humidity):
    """
    操作プログラム
    """
    print(f"【操作プログラム】判定: {judgment} / 自動化: {'ON' if automation_on else 'OFF'}")

    action_payload = {}

    if not automation_on:
        print("自動化OFFのため、GAS側へのエアコン操作依頼をスキップします。")
    else:
        if judgment == "暑い":
            if current_ac_state['power'] == 'off' or current_ac_state['mode'] != 'cool':
                action_payload = {'operation_mode': 'cool', 'button': ''}
            else:
                new_temp = current_ac_state['temp'] - 1
                action_payload = {'temperature': str(new_temp)}
        elif judgment == "寒い":
            new_temp = current_ac_state['temp'] + 1
            if new_temp > 28:
                action_payload = {'button': 'power-off'}
            else:
                action_payload = {'temperature': str(new_temp)}
        elif judgment == "快適":
            print("「快適」判定のため、現在の稼働状態および設定温度を維持します。")
            action_payload = None

        if action_payload:
            print(f"GAS側へ操作依頼を送信します: {action_payload}")
            try:
                response = requests.post(GAS_WEBAPP_URL, json=action_payload)
                response.raise_for_status()
                print(f"GASからの応答: {response.text}")
            except Exception as e:
                print(f"GASへの送信に失敗しました: {e}")

    # 追加：本物のログ送信プログラムへ終了通知とデータを渡す
    print("-> ログ送信プログラムへデータを渡します。")
    send_log_program(temp, humidity, judgment)