const ws = new WebSocket("ws://localhost:8765");
let connected = false;
let token = "";
const el = document.getElementById("board");
const timer = [document.getElementById("timer0"), document.getElementById("timer1")];
el.addEventListener("pointerup", () => mouse_up(event));
el.addEventListener("pointercancel", () => mouse_up(event));
let board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
];
let list_positions = [];
let move_index = 0;
let last_move = [[-1,-1],[-1,-1]]
let first_click = "";
let drag_start = "";
let start = "";
let player = "w";
let local_player = "w";
let legal_moves = [[0,1,2,2,0],[0,1,2,0,0],[0,1,1,3,0],[0,1,0,7,0],[6,4,4,4,0],[6,4,5,3,0],[6,4,5,5,0],[6,4,3,4,0],[4,4,3,4,0],[6,4,0,4,3],[1,5,3,5,0],[3,4,2,5,2],[3,4,2,4,0],[7,1,5,0,0],[7,1,5,2,0],[7,1,6,3,0],[7,1,7,3,0],[7,1,7,2,0],[7,1,7,0,0]];
                //[ligne départ, colonne départ, ligne arrivée, colonne arrivée, spécial]
                //spécial: {0:rien, 1:roque, 2:en passant, 3:promote}

let coor_letter = ["a","b","c","d","e","f","g","h"];
let date_move_start = new Date();
let time_move_start = [600, 600];

function stateUpdate(msg){
    board = msg.board;
    if (arrayEquals(board, list_positions[list_positions.length - 1]) === false){
        list_positions.push(structuredClone(board));
        move_index++;
    }
    player = msg.turn;
    legal_moves = msg.legal_moves;
    time_move_start = msg.time_move_start;
    date_move_start = new Date();
    //TODO: if premove exists and is in legal_moves, play it here
    draw();
}

function clic(ar,ac){
    let r = local_player === "w" ? ar : 7 - ar;
    let c = local_player === "w" ? ac : 7 - ac;
    start = "";
    console.log("clic");
    if (move_index !== list_positions.length - 1) return;
    if (first_click !== "" && (board[r][c][0] !== board[first_click[0]][first_click[1]][0])){
        if (r !== first_click[0] || c !== first_click[1]){
            if (board[r][c][0] !== player) {
                play_move(first_click, [r,c]);
            }else draw();
        }else draw();
    }
    else if (board[r][c][0] === player) {//=== local_player -> add also premove here
            first_click = [r, c];
            draw();
            getCase(ar, ac).focus();
    }
}

function play_move(i,e){
    let promotion = false;
    if ((e[0] !== i[0] || e[1] !== i[1]) && board[e[0]][e[1]][0] !== player && board[i[0]][i[1]][0] === player) {
        if (legal_moves.some(m => m[0] === i[0] && m[1] === i[1] && m[2] === e[0] && m[3] === e[1])) {
        let move = legal_moves.find(m => m[0] === i[0] && m[1] === i[1] && m[2] === e[0] && m[3] === e[1]);
        last_move = [i,e];
        board[e[0]][e[1]] = board[i[0]][i[1]];
        board[i[0]][i[1]] = "";
        start = ""; first_click = "";
        switch (move[4]){
            case 2: board[e[0]+1][e[1]] = "";
            case 0: end_move(i,e,move[4]); break;
            case 1:
                if (e[1]===6) {board[e[0]][5] = board[e[0]][7]; board[e[0]][7] = "";}
                else if (e[1]===2) {board[e[0]][5] = board[e[0]][7]; board[e[0]][7] = "";}
                else console.error("pas de roque ??? ;(");
                break;
            case 3: promote(i,e,player); promotion = true; break;
        }
        
        }
        else {
            console.log("illegal move");
            start = ""; first_click = "";
        }
    }
    if(!promotion) draw();
    getCase(e[0],e[1]).focus();
}
function end_move(i,e,special){
    //Send({type: "move", value: [i[0],i[1],e[0],e[1]]});
    let now = new Date();
    let p = player === local_player?0:1
    time_move_start[p] = date_move_start.getTime()/1000 + time_move_start[p] - now.getTime()/1000 + 2;
    date_move_start = new Date();
    player = player === "w" ? "b" : "w";
    move_index += 1;
    list_positions.push(structuredClone(board));
    if (connected){ ws.send(JSON.stringify({
        action: "move",
        value: [i[0],i[1],e[0],e[1]], //
        special: special,
        piece: special > 3 ? special - 3 : 0, // index 1 to 4
        token: token

    }));/*console.log(token);*/}
}

function getCase(r, c) {
    return document.querySelector(`.case[data-r="${r}"][data-c="${c}"]`);
}
function getImg(c) {
    return document.querySelector(`img[data-r="${c[0]}"][data-c="${c[1]}"]`);
}

function getCoor(e){
    const cible = document.elementFromPoint(e.clientX, e.clientY).closest(".case");
    //console.log(cible);
    return [parseInt(cible.dataset.r,10), parseInt(cible.dataset.c,10)];
}


document.getElementById("board").addEventListener("pointerdown", () => {
    //console.log(event);
    let c = getCoor(event);
    //console.log(board[c[0]][c[1]], player);
    if (board[c[0]][c[1]][0] === player || first_click !== ""){
        event.preventDefault();
        getImg(c).setPointerCapture(event.pointerId);
        start = c;
        drag_start = [event.clientX, event.clientY];
        console.log("start", start);
    }
});

function mouse_up(e) {
    if ((drag_start[0] - e.clientX) ** 2 + (drag_start[1] - e.clientY) ** 2 > 25){
        console.log("up", e);
        getImg(start).style.visibility = "hidden";
        let c = getCoor(e);
        getImg(start).style.visibility = "";
        getImg(start).releasePointerCapture(e.pointerId);
        play_move(start, c);
        start = "";
    }
}

window.onload = function() {
    list_positions = [structuredClone(board)];
    draw();
	setInterval('draw_timer()', 20);
};
ws.onopen = () => {
    token = sessionStorage.getItem("token");
    if (!token) { window.location.href = "login_page.html"; return; }
    ws.send(JSON.stringify({ action: "reprise", token }));
    connected = true;
    document.getElementById("connection").innerText = "Connected";
};
ws.onclose = () => {connected = false;    document.getElementById("connection").innerText = "Connection lost";}
socket.onmessage = (event) => {
  msg = JSON.parse(event.data)
  switch (msg.type){
    case "local_player": local_player = msg.value; break;
    case "state": stateUpdate(msg.value); break; //{ "type": "state", "board": {...}, "legal_moves": [...], "turn": "w", "check": false }
    default: console.log("Message inconnu:", msg);
  }
};