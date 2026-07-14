function handleAirCon(actionData) {
  const url = `https://api.nature.global/1/appliances/${APPLIANCE_ID}/aircon_settings`;
  let payload = {};
  
  if (actionData.button !== undefined) payload.button = actionData.button;
  if (actionData.temperature !== undefined) payload.temperature = actionData.temperature;
  if (actionData.operation_mode !== undefined) payload.operation_mode = actionData.operation_mode;
  
  const options = {
     method: 'post',
    headers: {
      'Authorization': `Bearer ${REMO_ACCESS_TOKEN}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    payload: payload
  };
  
  UrlFetchApp.fetch(url, options);
}