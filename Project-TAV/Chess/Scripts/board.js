const el = document.getElementById("board");
function stateUpdate(msg){
    board = msg.board;
    player = msg.turn;
    legal_moves = msg.legal_moves;
    //if premove exists and is in legal_moves, play it here
    afficher();
}

function afficher() {
    el.innerHTML = "";
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const div = document.createElement("div");
            div.className = "case " + ((r + c) % 2 ? "black" : "white");
            div.tabIndex = 0;
            if (!(board[r][c] === "")) {
                let img = document.createElement("img");
                switch (board[r][c]){
                    case "br": img.src = "../Sprites/Pieces_bitboards/blackRook.png"; break;
                    case "bn": img.src = "../Sprites/Pieces_bitboards/blackKnight.png"; break;
                    case "bb": img.src = "../Sprites/Pieces_bitboards/blackBishop.png"; break;
                    case "bq": img.src = "../Sprites/Pieces_bitboards/blackQueen.png"; break;
                    case "bk": img.src = "../Sprites/Pieces_bitboards/blackKing.png"; break;
                    case "bp": img.src = "../Sprites/Pieces_bitboards/blackPawn.png"; break;
                    case "wr": img.src = "../Sprites/Pieces_bitboards/whiteRook.png"; break;
                    case "wn": img.src = "../Sprites/Pieces_bitboards/whiteKnight.png"; break;
                    case "wb": img.src = "../Sprites/Pieces_bitboards/whiteBishop.png"; break;
                    case "wq": img.src = "../Sprites/Pieces_bitboards/whiteQueen.png"; break;
                    case "wk": img.src = "../Sprites/Pieces_bitboards/whiteKing.png"; break;
                    case "wp": img.src = "../Sprites/Pieces_bitboards/whitePawn.png"; break;
                    default: img.src = "../Sprites/Pieces_bitboards/"; break;
                }
                //img.draggable = true;
                img.addEventListener("pointermove", () => {
                    if(start[0] == r && start[1] == c) {
                        img.style.position = "relative";
                        img.style.transform = `translate(${event.clientX - drag_start[0]}px, ${event.clientY - drag_start[1]}px)`;
                    }
                });
                img.alt = board[r][c];
                img.dataset.r = r;
                img.dataset.c = c;
                div.appendChild(img);
            }
            div.dataset.r = r;
            div.dataset.c = c;
            if (r === first_click[0] && c === first_click[1]) div.className += " first_click";
            //if (legal_moves.some(m => m[0] === first_click[0] && m[1] === first_click[1] && m[2] === r && m[3] === c)) div.className += " legal_move";
            div.addEventListener("click", () => clic(r, c));
            div.addEventListener("keyup", () => {
                switch (event.key){
                    case "Enter": clic(r, c);break;
                    case "ArrowDown": getCase(r+1,c).focus();break;
                    case "ArrowUp": getCase(r-1,c).focus();break;
                    case "ArrowRight": getCase(r+(c===7?1:0),(c+1)%8).focus();break;
                    case "ArrowLeft": getCase(r-(c===0?1:0),(c+7)%8).focus();break;
                }});
            el.appendChild(div);
        }
    }

    document.getElementById("player_turn").innerHTML = (player === "w" ? "White" : "Black") + " is playing";
}
function clic(r,c){
    start = "";
    console.log("clic");
    if (first_click !== "" && (board[r][c][0] !== board[first_click[0]][first_click[1]][0])){
        if (r !== first_click[0] || c !== first_click[1]){
            if (board[r][c][0] !== player) {
                play_move(first_click, [r,c]);
            }else afficher();
        }else afficher();
    }
    else if (board[r][c][0] === player) {//=== local_player -> add also premove here
            first_click = [r, c];
            afficher();
            getCase(r, c).focus();
    }
}

function play_move(i,e){
    if ((e[0] !== i[0] || e[1] !== i[1]) && board[e[0]][e[1]][0] !== player && board[i[0]][i[1]][0] === player) {
        //if (legal_moves.includes([i[0],i[1],e[0],e[1]])) {
        //Send({type: "move", value: [i[0],i[1],e[0],e[1]]});
        board[e[0]][e[1]] = board[i[0]][i[1]];
        board[i[0]][i[1]] = "";
        player = player === "w" ? "b" : "w";
        start = ""; first_click = "";
    }
    afficher();
    console.log(getCase(e[0],e[1]));
    getCase(e[0],e[1]).focus();
}

function getCase(r, c) {
    return document.querySelector(`.case[data-r="${r}"][data-c="${c}"]`);
}
function getImg(c) {
    return document.querySelector(`img[data-r="${c[0]}"][data-c="${c[1]}"]`);
}

function getCoor(e){
    const cible = document.elementFromPoint(e.clientX, e.clientY).closest(".case");
    console.log(cible);
    return [parseInt(cible.dataset.r,10), parseInt(cible.dataset.c,10)];
}


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
let first_click = "";
let drag_start = "";
let start = "";
let player = "w";
let local_player = "";
let legal_moves = [];


document.getElementById("board").addEventListener("pointerdown", () => {
    console.log(event);
    let c = getCoor(event);
    console.log(board[c[0]][c[1]], player);
    if (board[c[0]][c[1]][0] === player || first_click !== ""){
        event.preventDefault();
        getImg(c).setPointerCapture(event.pointerId);
        start = c;
        drag_start = [event.clientX, event.clientY];
        console.log("start", start);
    }
});
el.addEventListener("pointerup", () => mouse_up(event));
el.addEventListener("pointercancel", () => mouse_up(event));
function mouse_up(e) {
    if ((drag_start[0] - e.clientX) ** 2 + (drag_start[1] - e.clientY) ** 2 > 25){
        console.log(e);
        getImg(start).style.visibility = "hidden";
        c = getCoor(e);
        getImg(start).style.visibility = "";
        getImg(start).releasePointerCapture(e.pointerId);
        play_move(start, c);
        start = "";
    }
}

afficher();

