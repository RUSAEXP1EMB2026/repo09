const REMO_ACCESS_TOKEN = '';
const APPLIANCE_ID = '';

/**
 * ローカル(Python)やLINE BotからのPOSTリクエストを受け取る窓口
 */
function doPost(e) {
  try {
    // 送信された操作指示(JSON)を読み込む
    const actionData = JSON.parse(e.postData.contents);
    
    // エアコン操作プログラムを実行
    const result = operateAirCon(actionData);
    
    // Python側へ成功レスポンスを返す
    return ContentService.createTextOutput(JSON.stringify({status: "success", result: result}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({status: "error", message: error.message}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 実際にNature Remo 3のAPIを実行してエアコンを操作する処理
 */
function operateAirCon(actionData) {
  const url = `https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings`;
  
  // Python側から送られた指示をAPI用のペイロードにセット
  let payload = {};
  if (actionData.button !== undefined) payload.button = actionData.button;
  if (actionData.temperature !== undefined) payload.temperature = actionData.temperature;
  if (actionData.operation_mode !== undefined) payload.operation_mode = actionData.operation_mode;
  
  const options = {
    method: 'post',
    headers: {
      'Authorization': `Bearer ${REMO_ACCESS_TOKEN}`
    },
    payload: payload
  };
  
  // Nature Remo APIへリクエスト送信
  const response = UrlFetchApp.fetch(url, options);
  return JSON.parse(response.getContentText());
}
