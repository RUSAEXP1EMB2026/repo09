import requests

# ==========================================
# 設定情報の入力
# ==========================================
# 1. 取得したNature Remoのアクセストークン
ACCESS_TOKEN = ''

# 2. エアコンのID
APPLIANCE_ID = ''

# APIのベースURLと認証ヘッダー
BASE_URL = 'https://api.nature.global'
HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def get_environment_and_ac_state():
    """
    Nature Remo 3から現在の温度・湿度を取得し、
    同時に指定されたエアコンの現在の設定状態を取得するプログラム
    """
    print("Nature Remoから各種データを取得しています...\n")

    try:
        # --------------------------------------------------
        # 1. デバイス（Nature Remo本体）から温度・湿度を取得
        # --------------------------------------------------
        devices_res = requests.get(f'{BASE_URL}/1/devices', headers=HEADERS)
        devices_res.raise_for_status()
        devices = devices_res.json()

        # 一般的に一番目に登録されているデバイス(Remo 3)のデータを取得
        device = devices[0]
        events = device.get('newest_events', {})

        # センサー値の取得 (te: 温度, hu: 湿度)
        current_temp = events.get('te', {}).get('val')
        current_humidity = events.get('hu', {}).get('val')

        print(f"【室内環境】温度: {current_temp}℃ / 湿度: {current_humidity}%")

        # --------------------------------------------------
        # 2. 家電一覧からエアコンの現在の稼働状態を取得
        # --------------------------------------------------
        appliances_res = requests.get(f'{BASE_URL}/1/appliances', headers=HEADERS)
        appliances_res.raise_for_status()
        appliances = appliances_res.json()

        ac_state = None
        for app in appliances:
            if app['id'] == APPLIANCE_ID:
                settings = app.get('settings', {})
                # 'button' が空文字列('')ならON、'power-off'ならOFF
                power = 'off' if settings.get('button') == 'power-off' else 'on'

                ac_state = {
                    'power': power,
                    'mode': settings.get('mode'),  # 'cool', 'warm', 'dry' 等
                    'temp': float(settings.get('temp', 0)) if settings.get('temp') else None
                }
                break

        if ac_state:
            power_disp = "ON" if ac_state['power'] == 'on' else "OFF"
            print(f"【エアコン状態】電源: {power_disp} / モード: {ac_state['mode']} / 設定温度: {ac_state['temp']}℃")
        else:
            print("エラー: 指定されたIDのエアコンが見つかりませんでした。")
            return None, None, None

        print("\n-> データ取得完了！")
        return current_temp, current_humidity, ac_state

    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")
        return None, None, None


# ==========================================
# テスト実行用のブロック
# ==========================================
if __name__ == '__main__':
    # 単体テストとして実行
    temp, humidity, state = get_environment_and_ac_state()

    if temp is not None:
        print("-" * 30)
        print("後続のプログラム（統計モデル・操作プログラム）へ渡すデータ:")
        print(f"・温度データ: {temp}")
        print(f"・湿度データ: {humidity}")
        print(f"・エアコン辞書: {state}")
        print("-" * 30)
