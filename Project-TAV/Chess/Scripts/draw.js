function draw_div(r,c,to_click=true){
    const div = document.createElement("div");
    div.className = "case " + ((r + c) % 2 ? "black" : "white");
    div.tabIndex = 0;
    let p = local_player === "w";
    let ar = p?r:7-r;
    let ac = p?c:7-c;
    if (!(list_positions[move_index][ar][ac] === "")) {
        let img = document.createElement("img");
        switch (list_positions[move_index][ar][ac]){
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
                img.style.transform = `translate(${event.clientX - drag_start[0]}px, ${event.clientY - drag_start[1]}px) rotate(${event.movementX}deg) `;
            }
        });
        img.alt = list_positions[move_index][ar][ac];
        img.dataset.r = r;
        img.dataset.c = c;
        div.appendChild(img);
    }
    div.dataset.r = r;
    div.dataset.c = c;
    //affichage des coordonnées:
    if(c==0){let coor = document.createElement("p");coor.innerHTML=8-ar; coor.className=" lcoor"; div.appendChild(coor);}
    if(r==7){let coor = document.createElement("p");coor.innerHTML=coor_letter[ac];coor.className=" bcoor"; div.appendChild(coor);}
    //arrondi des bords:
    if(c==0 && r==0) div.className += " tlcorner";if(c==7 && r==0) div.className += " trcorner";if(c==0 && r==7) div.className += " blcorner";if(c==7 && r==7) div.className += " brcorner";
    //display last move
    if(last_move.some(m => ar === m[0] && ac === m[1])){div.className += " last_move";}
    //display first click
    if (ar === first_click[0] && ac === first_click[1]) div.className += " first_click";
    //display legal moves
    if (move_index === list_positions.length - 1){
        if (legal_moves.some(m => m[0] === first_click[0] && m[1] === first_click[1] && m[2] === ar && m[3] === ac)){
            let a = legal_moves.find(m => m[0] === first_click[0] && m[1] === first_click[1] && m[2] === ar && m[3] === ac);
            console.log(a);
            if (board[ar][ac] === "" && a[4] !== 2) div.className += " legal_move";
            else div.className += " capturable";
        }}
    if (to_click){
        div.addEventListener("click", () => clic(r, c));
        //TODO: add coloration of cases and arrows
        div.addEventListener("keyup", () => {
            let arrow = false;
            switch (event.key){
                case "Enter": clic(r, c);break;
                case "s": case "S": getCase(r+1,c).focus();break;
                case "z": case "Z": getCase(r-1,c).focus();break;
                case "d": case "D": getCase(r+(c===7?1:0),(c+1)%8).focus();break;
                case "q": case "Q": getCase(r-(c===0?1:0),(c+7)%8).focus();break;
                case "x": case "X": local_player = local_player === "w" ? "b" : "w"; draw(); getCase(7-r,7-c).focus(); break;
                case "ArrowDown": move_index = 0;arrow = true;break;
                case "ArrowUp": move_index = list_positions.length - 1;arrow = true;break;
                case "ArrowRight": move_index = Math.min(list_positions.length - 1, move_index+1);arrow = true;break;
                case "ArrowLeft": move_index = Math.max(0, move_index-1);arrow = true;break;
            }
            if (arrow){
                console.log("a");
                first_click = "";
                if (move_index === 0) last_move = [[-1,-1],[-1,-1]];
                else{
                    last_move = [];
                    for (let x = 0; x < 8; x++) {
                        for (let y = 0; y < 8; y++) {
                            let previous = list_positions[move_index-1][x][y];
                            let now = list_positions[move_index][x][y];
                            let p = move_index % 2 === 0 ? "b" : "w"; //player who played the last move
                            if (now !== previous && (now !== "" || (previous !== "" && previous[0] === p))) last_move.push([x,y]);
                        }}}            // if changed                except en passant; TODO : Roque proper draw
                draw();
                getCase(r,c).focus();
            }
        });}
    return div;
}
function draw_timer(){
    const now = new Date();
    const p = player === local_player ? "0" : "1";
    const t1 = Math.floor(date_move_start.getTime()/1000 + time_move_start[player === "w" ? 0 : 1] - now.getTime()/1000);
    const t2 = Math.floor(time_move_start[player === "w" ? 1 : 0]);
    timer[p].classList.add("active");
    if (t1 < 30) timer[p].classList.add("red");
    timer[-p+1].classList.remove("active");timer[-p+1].classList.remove("red");
    timer[p].innerHTML = t1 < 0 ? "Time out" : `${Math.floor(t1/60)}:${t1%60<10?"0":""}${t1%60}`;
    timer[-p+1].innerHTML = t2 < 0 ? "Time out" : `${Math.floor(t2/60)}:${t2%60<10?"0":""}${t2%60}`;
}
function draw() {
    el.innerHTML = "";
    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            el.appendChild(draw_div(r,c));
        }
    }
    //document.getElementById("player_turn").innerHTML = (player === "w" ? "White" : "Black") + " is playing";
}

function promote(i,e,p){
    let c = e[1];
    let d = p === local_player ? 1 : -1;
    let r = p === local_player  ? 0 : 7;
    //for (let i=r; i<4; i++){
    el.innerHTML = "";
    for (let x = 0; x < 8; x++) {
        for (let y = 0; y < 8; y++) {
            let div = draw_div(x,y,false);
            div.tabIndex = -1;
            if (y === c && x < 4){
                console.log("hello");
                div.innerHTML = "";
                div.tabIndex = 0;
                let img = document.createElement("img");
                let img_name; let text;
                switch (x){
                    case 0: img_name = "Queen"; text = "q"; break;
                    case 1: img_name = "Rook"; text = "r"; break;
                    case 2: img_name = "Bishop"; text = "b"; break;
                    case 3: img_name = "Knight"; text = "n"; break;
                }
                img.src = `../Sprites/Pieces_bitboards/${p==="w"?"white":"black"}${img_name}.png`
                img.alt = text;
                img.dataset.index = x;
                div.appendChild(img);
                div.className = "case promote";
                div.addEventListener("click",() => {
                    board[e[0]][e[1]] = `${p}${text}`;
                    end_move(i, e, 3 + 4 - x);
                    draw();
                });
                div.addEventListener("keyup", (ev) => {
                    switch (ev.key){
                        case "Enter":
                            board[e[0]][e[1]] = `${p}${text}`;
                            end_move(i, e, 3 + 4 - x);
                            draw();
                            break;
                        case "s": case "d": case "ArrowDown": case "ArrowRight": getCase(x==3?0:x+1,c).focus();break;
                        case "z": case "q": case "ArrowUp": case "ArrowLeft": getCase(x==0?3:x-1,c).focus();break;
                    }
                });
            }
            el.appendChild(div);
        }
    }
}
