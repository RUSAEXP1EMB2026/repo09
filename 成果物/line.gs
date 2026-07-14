function handleLineEvent(event) {
  // messageイベント以外は安全に終了
  if (!event || event.type !== "message" || !event.message || event.message.type !== "text") {
    return ContentService.createTextOutput("OK");
  }

  const replyToken = event.replyToken;
  const userMessage = event.message.text.trim();

  const ss = SpreadsheetApp.openById("1rJFqfZjMPcKOTKm99SbbOYjI1MHMsO58N4_SwZTcac0");
  const settingSheet = ss.getSheetByName("設定");

  // ① 自動化ON/OFF → 設定シートに書き込み
  if (userMessage === "自動化ON") {
    settingSheet.getRange("A2").setValue("ON");
    replyMessage(replyToken, "自動化を ON にしました。");
    return ContentService.createTextOutput("OK");
  }

  if (userMessage === "自動化OFF") {
    settingSheet.getRange("A2").setValue("OFF");
    replyMessage(replyToken, "自動化を OFF にしました。");
    return ContentService.createTextOutput("OK");
  }

  // ② 暑い／寒い／快適 → Remoから温湿度取得
  if (["暑い", "寒い", "快適"].includes(userMessage)) {
    let devices;
    try {
      const res = UrlFetchApp.fetch("https://api.nature.global/1/devices", {
        method: "get",
        headers: { "Authorization": `Bearer ${REMO_ACCESS_TOKEN}` }
      });
      devices = JSON.parse(res.getContentText());
    } catch (e) {
      return ContentService.createTextOutput("OK");
    }

    if (!devices || devices.length === 0) {
      return ContentService.createTextOutput("OK");
    }

    const newest = devices[0].newest_events;
    const currentTemp = (newest && newest.te) ? newest.te.val : "";
    const currentHum = (newest && newest.hu) ? newest.hu.val : "";

    // ③ 教師データシートに書き込み
    handleSpreadsheetAction({
      type: "teacher",
      temperature: currentTemp,
      humidity: currentHum,
      label: userMessage
    });

    // 現在のエアコンの設定を取得
    const appRes = UrlFetchApp.fetch("https://api.nature.global/1/appliances", {
      method: "get",
      headers: { "Authorization": `Bearer ${REMO_ACCESS_TOKEN}` }
    });
    const appliances = JSON.parse(appRes.getContentText());
    const aircon = appliances.find(app => app.id === APPLIANCE_ID);

    // Remoが記憶している設定温度を取得
    let currentSettingTemp = Number(aircon.settings.temp || aircon.settings.temperature);

    // 電源OFF等で設定温度が不明な場合は、現在の「室温」を基準にする
    if (isNaN(currentSettingTemp) || currentSettingTemp === 0) {
      currentSettingTemp = Number(currentTemp) || 25;
    }

    // ④ Remoでエアコン操作
    // 確実に「整数」にするため Math.round を使用
    let newTemp = Math.round(currentSettingTemp);
    if (userMessage === "暑い") newTemp -= 1;
    if (userMessage === "寒い") newTemp += 1;

    // 安全装置（18度〜30度に制限）
    if (newTemp < 18) newTemp = 18;
    if (newTemp > 30) newTemp = 30;

    // Remo APIを直接叩く（強制送信）
    try {
      UrlFetchApp.fetch(`https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings`, {
        method: 'post',
        headers: { 'Authorization': `Bearer ${REMO_ACCESS_TOKEN}` },
        payload: {
          temperature: String(newTemp),
          operation_mode: "cool",
          button: ""
        }
      });
      
      // テスト用に、裏側でどういう数値が計算されたかをLINEに返信させる
      const originalTemp = aircon.settings.temp || "不明";
      replyMessage(replyToken, `${userMessage}を記録しました。\n\n【操作レポート】\nRemoの記憶: ${originalTemp}度\n送信した温度: ${newTemp}度`);
    } catch (apiError) {
      replyMessage(replyToken, `記録は完了しましたが、エアコン操作でエラーが発生しました:\n${apiError}`);
    }

    return ContentService.createTextOutput("OK");
  }

  // ⑤ 記録を見る
  if (userMessage === "記録を見る") {
    replyMessage(replyToken, `記録はこちらです!\n${SPREADSHEET_URL}`);
    return ContentService.createTextOutput("OK");
  }

  return ContentService.createTextOutput("OK");
}

function replyMessage(replyToken, text) {
  try {
    UrlFetchApp.fetch("https://api.line.me/v2/bot/message/reply", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${LINE_ACCESS_TOKEN}`
      },
      payload: JSON.stringify({
        replyToken: replyToken,
        messages: [{ type: "text", text: text }]
      })
    });
  } catch (e) {
    console.log("LINE返信エラー: " + e);
  }
}
