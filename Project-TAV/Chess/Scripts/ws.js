/*class GameConnection {
  constructor(gameId, onStateUpdate) {
    this.onStateUpdate = onStateUpdate;
    this.ws = new WebSocket(`wss://tondomaine.com/ws/game/${gameId}`);

    this.ws.onopen = () => console.log("Connecté");
    this.ws.onmessage = (event) => this.handleMessage(JSON.parse(event.data));
    this.ws.onclose = () => this.tryReconnect();
    this.ws.onerror = (err) => console.error("WS erreur:", err);
  }

  handleMessage(msg) {
    //msg.type, msg.value
  }

  send(msg) {
    if (this.ws.readyState === WebSocket.OPEN) this.ws.send(JSON.stringify(msg));
  }

  tryReconnect() {
    setTimeout(() => { /* reconnexion avec backoff *//* }, 1000);
  }
}
*/

const socket = new WebSocket(
  "ws://127.0.0.1:8765"
);

socket.onopen = () => {
  console.log("Connecté au serveur local");
};

socket.onmessage = (event) => {
  msg = JSON.parse(event.data)
  switch (msg.type){
    case "local_player": local_player = msg.value; break;
    case "state": stateUpdate(msg.value); break; //{ "type": "state", "board": {...}, "legal_moves": [...], "turn": "w", "check": false }
    default: console.log("Message inconnu:", msg);
  }
};

socket.onerror = () => {
  console.log("Erreur de connexion");
};

socket.onclose = () => {
  console.log("Connexion fermée");
};

function Send(msg){
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(msg));
  }else console.error(new Error("not ready. state:" + socket.readyState));
};
