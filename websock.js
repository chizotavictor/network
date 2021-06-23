var ws = new WebSocket('ws://127.0.0.1:15674/ws');
var client = Stomp.over(ws);