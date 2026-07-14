function handleAirCon(actionData) {
  try {
    // 現在の設定を取得
    const res = UrlFetchApp.fetch(`https://api.nature.global/1/appliances/${APPLIANCE_ID}`, {
      method: "get",
      headers: { "Authorization": `Bearer ${REMO_ACCESS_TOKEN}` }
    });

    const appliance = JSON.parse(res.getContentText());
    const current = appliance.settings;

    // Remoが要求する完全な設定を送る（キー名を正しく合わせる）
    const payload = {
      temperature: actionData.temperature,   // ← 変更したい温度
      operation_mode: current.mode,          // ← 冷房/暖房/自動
      air_volume: current.vol,               // ← 風量
      air_direction: current.dir,            // ← 風向
      button: "power"                        // ← 必須
    };

    UrlFetchApp.fetch(
      `https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings`,
      {
        method: "post",
        headers: {
          "Authorization": `Bearer ${REMO_ACCESS_TOKEN}`,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        payload: payload
      }
    );

  } catch (e) {
    console.log("AirCon操作エラー: " + e);
  }
}
