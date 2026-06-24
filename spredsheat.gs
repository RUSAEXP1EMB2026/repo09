function doPost(e) {
  // パラメータエラー時のレスポンス用オブジェクト
  const createResponse = (status, message) => {
    return ContentService.createTextOutput(JSON.stringify({ status: status, message: message }))
                         .setMimeType(ContentService.MimeType.JSON);
  };

  try {
    // 1. PythonやLINEから送られてきたJSONデータをパース
    const requestData = JSON.parse(e.postData.contents);
    const type = requestData.type; // "log" または "teacher"
    const temperature = requestData.temperature;
    const humidity = requestData.humidity;
    const label = requestData.label; // AI判定結果、またはユーザーの体感

    // 2. 開いているスプレッドシートを取得
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet;
    let rowData = [new Date(), temperature, humidity, label]; // 書き込むデータ（先頭に現在日時）

    // 3. タイプに応じて書き込み先のシートを振り分け
    if (type === "log") {
      sheet = ss.getSheetByName("稼働状況ログ");
    } else if (type === "teacher") {
      sheet = ss.getSheetByName("教師データ");
    } else {
      return createResponse("error", "Invalid type specified. Use 'log' or 'teacher'.");
    }

    // シートが存在しない場合のチェック
    if (!sheet) {
      return createResponse("error", "Target sheet not found.");
    }

    // 4. シートの最下行にデータを追記
    sheet.appendRow(rowData);

    // 成功レスポンスを返す
    return createResponse("success", "Data recorded successfully.");

  } catch (error) {
    // エラーが発生した場合の処理
    return createResponse("error", error.toString());
  }
}