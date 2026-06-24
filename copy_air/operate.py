import requests

GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbw5RftIai-nGH1XkG_E8LuDDj4RORjzj_VURanZ-GIGxvsJB0ej4aUQptiVJifoVHZO/exec"


def operation_program(judgment, automation_on, current_ac_state):
    """
    操作プログラム
    judgment: "暑い", "寒い", "快適" のいずれか
    automation_on: True(自動化ON) または False(自動化OFF)
    current_ac_state: 現在のエアコン状態の辞書 (例: {'power': 'on', 'mode': 'cool', 'temp': 26})
    """
    print(f"【操作プログラム】判定: {judgment} / 自動化: {'ON' if automation_on else 'OFF'}")

    if not automation_on:
        print("自動化OFFのため、GAS側へのエアコン操作依頼をスキップします。")
        notify_log_program(judgment, "スキップ", current_ac_state)
        return

    action_payload = {}
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

    notify_log_program(judgment, action_payload if action_payload else "維持", current_ac_state)


def notify_log_program(judgment, action_taken, current_ac_state):
    print("-> ログ送信プログラムへ終了通知を行いました。\n")


# ==========================================
# テストケース
# ==========================================
if __name__ == '__main__':
    print("=== テスト実行を開始します ===\n")

    # 仮想の「現在のエアコン状態」を定義
    dummy_ac_state = {
        'power': 'on',
        'mode': 'cool',
        'temp': 27
    }

    # テストケース1: 自動化ONで「暑い」と判定された場合（温度が1度下がるはず）
    print("【テスト1】稼働中(27度)で「暑い」判定の場合")
    operation_program(judgment="暑い", automation_on=True, current_ac_state=dummy_ac_state)

    # テストケース2: 自動化ONで「寒い」と判定された場合（温度が1度上がるはず）
    print("【テスト2】稼働中(27度)で「寒い」判定の場合")
    operation_program(judgment="寒い", automation_on=True, current_ac_state=dummy_ac_state)

    # テストケース3: 自動化OFFの場合（通信がスキップされるはず）
    print("【テスト3】自動化OFFで「暑い」判定の場合")
    operation_program(judgment="暑い", automation_on=False, current_ac_state=dummy_ac_state)