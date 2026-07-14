// ==========================================
// グローバル設定（すべてのコードから参照されます）
// ==========================================
const REMO_ACCESS_TOKEN = 'ory_at_eV6D3JHuAvoVbZyHWGmCrfua9jdCsOV6OGbATs9DQPA.cuF1NtDKFK85Q9Yr9JAweebaBr2xqXS20ihy1iJh4-k';
const APPLIANCE_ID = '4d0aadb5-697a-4976-95ec-efc9496c94af';
const LINE_ACCESS_TOKEN = "/ttAY2K3NAF/+0i0RS+yg7rpTgGZtcd88fIwKBCT6p5XdOj/iwhYchBM7i/94RU+Xh9ZjoEl6gSsbrosai7ZcNDE9GqyLBboykDh/ihHNt8hdOYL9NZx5cdfjyikd1J4bUQ7c1J5yBb/4TohISNgygdB04t89/1O/w1cDnyilFU=";
const SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1rJFqfZjMPcKOTKm99SbbOYjI1MHMsO58N4_SwZTcac0/edit?gid=0#gid=0";

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
       const event = data.events[0];   
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