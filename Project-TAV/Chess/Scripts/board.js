const el = document.getElementById("board");
function afficher() {
    el.innerHTML = "";
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const div = document.createElement("div");
            div.className = "case " + ((r + c) % 2 ? "black" : "white");
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
            div.addEventListener("click", () => clic(r, c));
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
                board[r][c] = board[first_click[0]][first_click[1]];
                board[first_click[0]][first_click[1]] = "";
                player = player === "w" ? "b" : "w";
                first_click = ""
            }
        }
        afficher();
    }
    else{
        if (board[r][c][0] === player) {
            first_click = [r, c];
            afficher();
            const div = getCase(r, c);
            div.classList.add("first_click");
        }
    }
}

function play_move(i,e){
    if ((e[0] !== i[0] || e[1] !== i[1]) && board[e[0]][e[1]][0] !== player && board[i[0]][i[1]][0] === player) {
        board[e[0]][e[1]] = board[i[0]][i[1]];
        board[i[0]][i[1]] = "";
        player = player === "w" ? "b" : "w";
        start = ""; first_click = "";
    }
    afficher();
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
    // ...
];
let first_click = "";
let drag_start = "";
let start = "";
let player = "w";


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

