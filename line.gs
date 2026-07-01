const REMO_ACCESS_TOKEN = "YOUR_REMO_TOKEN";
const APPLIANCE_ID = "YOUR_APPLIANCE_ID";
const LINE_ACCESS_TOKEN = "/ttAY2K3NAF/+0i0RS+yg7rpTgGZtcd88fIwKBCT6p5XdOj/iwhYchBM7i/94RU+Xh9ZjoEl6gSsbrosai7ZcNDE9GqyLBboykDh/ihHNt8hdOYL9NZx5cdfjyikd1J4bUQ7c1J5yBb/4TohISNgygdB04t89/1O/w1cDnyilFU=";

function doPost(e) {
  const json = JSON.parse(e.postData.contents);
  const event = json.events[0];

  if (event.type !== "message" || event.message.type !== "text") {
    return ContentService.createTextOutput("OK");
  }

  const userMessage = event.message.text;
  const replyToken = event.replyToken;

  const ss = SpreadsheetApp.openById("1YmnRv4Tb193kPnGcdSPfs1BXbj3VPmeRM5Q7PowQ680");
  const settingSheet = ss.getSheetByName("設定");
  const teacherSheet = ss.getSheetByName("教師データ");


  // -----------------------------
  // ① 自動化ON/OFF → 設定シートに書き込み
  // -----------------------------
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

  // -----------------------------
  // ② 暑い／寒い／快適 → Remoから温湿度取得
  // -----------------------------
  if (["暑い", "寒い", "快適"].includes(userMessage)) {

    // Remoから現在の温度・湿度を取得
    const res = UrlFetchApp.fetch("https://api.nature.global/1/devices", {
      method: "get",
      headers: { "Authorization": "Bearer " + REMO_ACCESS_TOKEN }
    });

    const devices = JSON.parse(res.getContentText());
    const currentTemp = devices[0].newest_events.te.val;
    const currentHum = devices[0].newest_events.hu.val;

    // -----------------------------
    // ③ 教師データシートに書き込み
    // -----------------------------
    const rowData = [new Date(), currentTemp, currentHum, userMessage];
    teacherSheet.appendRow(rowData);

    // -----------------------------
    // ④ Remoでエアコン操作（±1℃）
    // -----------------------------
    let newTemp = currentTemp;

    if (userMessage === "暑い") newTemp = currentTemp - 1;
    if (userMessage === "寒い") newTemp = currentTemp + 1;
    if (userMessage === "快適") newTemp = currentTemp; // 変更なし

    const payload = {
      temperature: String(newTemp),
      operation_mode: "cool"
    };

    UrlFetchApp.fetch(
      `https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings`,
      {
        method: "post",
        headers: { "Authorization": "Bearer " + REMO_ACCESS_TOKEN },
        payload: payload
      }
    );

    replyMessage(replyToken, `${userMessage} を記録しました。設定温度を変更しました。`);
    return ContentService.createTextOutput("OK");
  }

  // -----------------------------
  // ⑤ 記録を見る
  // -----------------------------
  if (userMessage === "記録を見る") {
    replyMessage(replyToken, "記録はこちらです。\nhttps://docs.google.com/spreadsheets/d/1YmnRv4Tb193kPnGcdSPfs1BXbj3VPmeRM5Q7PowQ680/edit?gid=973525101#gid=973525101");
    return ContentService.createTextOutput("OK");
  }

  return ContentService.createTextOutput("OK");
}


// LINE返信
function replyMessage(replyToken, text) {
  UrlFetchApp.fetch("https://api.line.me/v2/bot/message/reply", {
    method: "post",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + LINE_ACCESS_TOKEN
    },
    payload: JSON.stringify({
      replyToken: replyToken,
      messages: [{ type: "text", text: text }]
    })
  });
}

