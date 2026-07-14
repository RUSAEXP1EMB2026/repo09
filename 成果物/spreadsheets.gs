function handleSpreadsheetAction(requestData) {
  const type = requestData.type;
  const temperature = requestData.temperature;
  const humidity = requestData.humidity;
  const label = requestData.label;

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheetName = (type === "log") ? "稼働状況ログ" : "教師データ";
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: "Sheet not found" }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  sheet.appendRow([new Date(), temperature, humidity, label]);
  return ContentService.createTextOutput(JSON.stringify({ status: "success", message: "Data recorded successfully." }))
    .setMimeType(ContentService.MimeType.JSON);
}

function handleGetRequest(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    
    if (e.parameter.action === "get_status") {
      const autoStatus = ss.getSheetByName("設定").getRange("A2").getValue().toString().trim();
      return ContentService.createTextOutput(JSON.stringify({ "automation_on": autoStatus === "ON" }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const values = ss.getSheetByName("教師データ").getDataRange().getValues();
    const data = [];
    
    for (let i = 1; i < values.length; i++) {
      if (values[i][1] !== "" && values[i][2] !== "" && values[i][3] !== "") {
        data.push({
          "temperature": parseFloat(values[i][1]),
          "humidity": parseFloat(values[i][2]),
          "label": values[i][3]
        });
      }
    }
    return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}