function afficher() {
    const el = document.getElementById("board");
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
                //img.src = "../Sprites/Pieces_bitboards/";
                /*img.height = 100%;
                img.width = 100%;*/
                img.alt = board[r][c];
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
    if (first_click !== "" && (board[r][c][0] !== board[first_click[0]][first_click[1]][0])){
        console.log(board[r][c][0] !== board[first_click[0]][first_click[1]][0]);
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

function getCase(r, c) {
    return document.querySelector(`.case[data-r="${r}"][data-c="${c}"]`);
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
let player = "w";
afficher();

