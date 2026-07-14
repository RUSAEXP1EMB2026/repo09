function handleLineEvent(event) {

  // messageイベント以外は安全に終了
  if (!event || event.type !== "message" || !event.message || event.message.type !== "text") {
    return;
  }

  if (event.type !== "message" || event.message.type !== "text") {
    return;
  }

  const replyToken = event.replyToken;
  const userMessage = event.message.text.trim();

  const ss = SpreadsheetApp.openById("1rJFqfZjMPcKOTKm99SbbOYjI1MHMsO58N4_SwZTcac0");
  const settingSheet = ss.getSheetByName("設定");

  // ① 自動化ON/OFF → 設定シートに書き込み
  if (userMessage === "自動化ON") {
    settingSheet.getRange("A2").setValue("ON");
    replyMessage(replyToken, "自動化を ON にしました。");
    return;
  }

  if (userMessage === "自動化OFF") {
    settingSheet.getRange("A2").setValue("OFF");
    replyMessage(replyToken, "自動化を OFF にしました。");
    return;
  }

  // ② 暑い／寒い／快適 → Remoから温湿度取得
  if (["暑い", "寒い", "快適"].includes(userMessage)) {

    replyMessage(replyToken, `${userMessage} を記録しました。設定温度を変更しました。`);

    let devices;
    try {
      const res = UrlFetchApp.fetch("https://api.nature.global/1/devices", {
        method: "get",
        headers: { "Authorization": `Bearer ${REMO_ACCESS_TOKEN}` }
      });
      devices = JSON.parse(res.getContentText());
    } catch (e) {
      return;
    }

    // デバイスがない場合
    if (!devices || devices.length === 0) {
      return;
    }

    const newest = devices[0].newest_events;

    if (!newest || !newest.te || !newest.hu) {
      // 温度・湿度が取れなくても教師データは書き込む
     handleSpreadsheetAction({
     type: "teacher",
     temperature: "",
     humidity: "",
     label: userMessage
     });
      return;
    }

    const currentTemp = newest.te.val;
    const currentHum = newest.hu.val;

    // ③ 教師データシートに書き込み（コード1の関数を呼び出し）
    handleSpreadsheetAction({
      type: "teacher",
      temperature: currentTemp,
      humidity: currentHum,
      label: userMessage
    });

    // ④ Remoでエアコン操作（コード2の関数を呼び出し）
    let newTemp = currentTemp;
    if (userMessage === "暑い") newTemp = currentTemp - 1;
    if (userMessage === "寒い") newTemp = currentTemp + 1;
    // 「快適」の場合は変更なし

    handleAirCon({
      temperature: String(newTemp),
      operation_mode: "cool"
    });
    return;
  }

  // ⑤ 記録を見る
  if (userMessage === "記録を見る") {
    replyMessage(replyToken, `記録はこちらです!\n${SPREADSHEET_URL}`);
    return;
  }
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
    // 例外が起きても落ちないようにする
    console.log("LINE返信エラー: " + e);
  }
}