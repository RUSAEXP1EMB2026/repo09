import requests

# 取得済みのアクセストークンをここに貼り付けます
ACCESS_TOKEN = ''


def get_aircon_ids():
    url = 'https://api.nature.global/1/appliances'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    try:
        print("Nature Remoから家電データを取得中...\n")
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # エラーがあればここでストップ

        appliances = response.json()
        ac_found = False

        print("▼ 登録されているエアコン一覧 ▼")
        print("-" * 40)

        for appliance in appliances:
            # 家電の種類が 'AC' (エアコン) のものを抽出
            if appliance.get('type') == 'AC':
                print(f"【名前】 {appliance.get('nickname')}")
                print(f"【ID】   {appliance.get('id')}")
                print("-" * 40)
                ac_found = True

        if not ac_found:
            print("登録されている家電の中にエアコンが見つかりませんでした。")
            print("Nature Remoアプリでエアコンが正しく登録されているか確認してください。")

    except Exception as e:
        print(f"データの取得中にエラーが発生しました: {e}")


if __name__ == '__main__':
    get_aircon_ids()