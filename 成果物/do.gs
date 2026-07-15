// ==========================================
// グローバル設定（すべてのコードから参照されます）
// ==========================================
const REMO_ACCESS_TOKEN = PropertiesService.getScriptProperties().getProperty("REMO_ACCESS_TOKEN");
const APPLIANCE_ID = PropertiesService.getScriptProperties().getProperty("APPLIANCE_ID");
const LINE_ACCESS_TOKEN = PropertiesService.getScriptProperties().getProperty("LINE_ACCESS_TOKEN");
const SPREADSHEET_URL = PropertiesService.getScriptProperties().getProperty("SPREADSHEET_URL");

// ==========================================
// API エントリポイント
// ==========================================
function doPost(e) {
  try {
    // リクエストが空の場合は終了
    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput("OK");
    }

    const data = JSON.parse(e.postData.contents);

    // 1. LINEからのWebhookリクエストの場合
    if (data.events && data.events.length > 0) {
      const event = data.events[0];   // ← 一つづつイベントを取り出す
      handleLineEvent(event);
      return ContentService.createTextOutput("OK");
    }

    // 2. スプレッドシート操作リクエストの場合
    if (data.type === "log" || data.type === "teacher") {
      return handleSpreadsheetAction(data); // コード1を呼び出し
    } 
    
    // 3. それ以外（直接のエアコン操作リクエスト）の場合
    return handleAirCon(data); // コード2を呼び出し
    
  } catch (error) {
    // エラー発生時にLINE側に無駄な再送をさせないための対策
    console.error("doPost Error:", error);
    return ContentService.createTextOutput("OK");
  }
}

function doGet(e) {
  return handleGetRequest(e); // コード1を呼び出し
}
