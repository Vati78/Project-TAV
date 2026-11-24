import asyncio
import json
import secrets
import websockets
import os
import csv
import main as mn
import hashlib

DELAI_GRACE = 10  # secondes avant abandon
FICHIER = "users.csv"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

connexions = {}          # nom -> ws actuelle
sessions = {}            # token -> {"nom": ...}
parties_par_nom = {}     # nom -> [Partie, couleur]
attente = []             # liste de noms
taches_abandon = {}      # nom -> task du délai de grâce
adversaires = {}

COULEURS = ["w", "b"]
LETTRES_PIECES = "pnbrqk"   # index 0..5 dans pieces[]


async def envoyer(nom, msg):
    ws = connexions.get(nom)
    if ws:
        try:
            await ws.send(json.dumps(msg))
        except websockets.ConnectionClosed:
            pass


async def creer_partie(nom):
    if nom in attente or nom in parties_par_nom:
        return
    attente.append(nom)
    if len(attente) == 2:
        j1, j2 = attente[:]
        attente.clear()
        partie = mn.Gestionary([2, 1, "r", True, [10, 1]])

        parties_par_nom[j1] = [partie, 0]
        parties_par_nom[j2] = [partie, 1]
        adversaires[j1] = j2
        adversaires[j2] = j1
        await envoyer(j1, {"action": "partie_trouvee", "couleur": 0})
        await envoyer(j2, {"action": "partie_trouvee", "couleur": 1})


async def quitter_partie(nom):
    pass


async def delai_grace(nom):
    await asyncio.sleep(DELAI_GRACE)
    taches_abandon.pop(nom, None)
    await quitter_partie(nom)


# ---------------------------------------------------------------
# Lecture de l'état de la partie (bitboards -> format du client)
# ---------------------------------------------------------------
def lire_plateau(partie):
    jeu = partie.chess_game
    plateau = [["" for _ in range(8)] for _ in range(8)]
    for couleur, lettre in ((0, "w"), (1, "b")):
        for j in range(6):
            bb = jeu.players[couleur].pieces[j]
            for idx in range(64):
                if (bb >> idx) & 1:
                    plateau[idx // 8][idx % 8] = lettre + LETTRES_PIECES[j]
    return plateau


def lire_coups_legaux(partie):
    jeu = partie.chess_game
    # au début de la partie, les coups légaux n'ont pas encore été calculés
    if len(jeu.list_legal_moves) != 64:
        jeu.get_all_legal_moves(jeu.player_turn)

    plateau = lire_plateau(partie)
    coups = []
    for dep in range(64):
        arrivees = jeu.list_legal_moves[dep]
        if not arrivees:
            continue
        r1, c1 = divmod(dep, 8)
        piece = plateau[r1][c1]
        if not piece:
            continue
        for arr in range(64):
            if (arrivees >> arr) & 1:
                r2, c2 = divmod(arr, 8)
                special = 0
                if piece[1] == "k" and abs(c2 - c1) == 2:
                    special = 1                          # roque
                elif piece[1] == "p":
                    if c1 != c2 and plateau[r2][c2] == "":
                        special = 2                      # en passant
                    elif r2 in (0, 7):
                        special = 3                      # promotion
                coups.append([r1, c1, r2, c2, special])
    return coups


def lire_temps(partie):
    # TODO: remplacer par les vraies pendules du moteur (secondes restantes [blanc, noir])
    return [600, 600]


def etat_pour(nom):
    partie, couleur = parties_par_nom[nom]
    jeu = partie.chess_game
    return {
        "type": "state",
        "value": {
            "board": lire_plateau(partie),
            "legal_moves": lire_coups_legaux(partie),
            "turn": COULEURS[jeu.player_turn],
            "time_move_start": lire_temps(partie),
        },
    }


async def envoyer_etat(nom):
    if nom in parties_par_nom:
        await envoyer(nom, etat_pour(nom))


def jouer_coup(partie, couleur, coup, special, piece):
    jeu = partie.chess_game
    if special > 3:
        special = 3          # le client envoie 3 + (1..4) pour une promotion
    if jeu.player_turn != couleur:
        return False
    if not any(m[:4] == list(coup) and m[4] == special for m in lire_coups_legaux(partie)):
        return False

    jeu.play_move(
        1 << (8 * coup[0] + coup[1]),        # bitboard, pas un index
        1 << (8 * coup[2] + coup[3]),
        couleur,
        piece if special == 3 else False     # piece = 1..4 (cavalier..dame)
    )
    return True


# ---------------------------------------------------------------
# Comptes
# ---------------------------------------------------------------
def lire_utilisateurs():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hacher(mdp):
    return hashlib.sha256(mdp.encode("utf-8")).hexdigest()


def verifier(nom, mdp):
    return any(u["username"] == nom and u["password"] == hacher(mdp)
               for u in lire_utilisateurs())


def creer(nom, mdp):
    if not nom or not mdp:
        return False, "Please fill in both fields."
    if any(u["username"] == nom for u in lire_utilisateurs()):
        return False, "This username is already taken."

    nouveau_fichier = not os.path.exists(FICHIER)
    with open(FICHIER, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if nouveau_fichier:
            writer.writerow(["username", "password"])
        writer.writerow([nom, hacher(mdp)])
    return True, "Account created!"


# ---------------------------------------------------------------
# Handler
# ---------------------------------------------------------------
async def handler(ws):
    utilisateur = None

    try:
        async for message in ws:
            d = json.loads(message)
            action = d.get("action")

            if action == "connexion":
                ok = verifier(d["nom"], d["mdp"])
                token = None
                if ok:
                    token = secrets.token_urlsafe(32)
                    sessions[token] = {"nom": d["nom"]}
                await ws.send(json.dumps({"action": "connexion", "ok": ok, "token": token}))

            elif action == "quitter_menu":
                token = d.get("token")
                s = sessions.get(token)
                if not s:
                    await ws.send(json.dumps({"action": "erreur", "message": "Session invalide"}))
                    continue
                utilisateur = s["nom"]
                await quitter_partie(utilisateur)
                if utilisateur in attente:
                    attente.remove(utilisateur)
                sessions.pop(token, None)
                connexions.pop(utilisateur, None)

            elif action == "move":
                s = sessions.get(d.get("token"))
                if not s:
                    await ws.send(json.dumps({"action": "erreur", "message": "Session invalide"}))
                    continue
                utilisateur = s["nom"]
                entree = parties_par_nom.get(utilisateur)
                if not entree:
                    await ws.send(json.dumps({"action": "erreur", "message": "Pas en partie"}))
                    continue
                partie, couleur = entree
                jouer_coup(partie, couleur, d["value"], d["special"], d["piece"])
                # état renvoyé aux deux : si le coup est refusé, le joueur est resynchronisé
                await envoyer_etat(utilisateur)
                await envoyer_etat(adversaires[utilisateur])

            elif action == "creation":
                ok, msg = creer(d["nom"], d["mdp"])
                await ws.send(json.dumps({"action": "creation", "ok": ok, "message": msg}))

            elif action == "reprise":
                s = sessions.get(d.get("token"))
                if s:
                    utilisateur = s["nom"]
                    connexions[utilisateur] = ws
                    # annule l'abandon si le joueur revient à temps
                    tache = taches_abandon.pop(utilisateur, None)
                    if tache:
                        tache.cancel()
                en_partie = bool(s) and utilisateur in parties_par_nom
                await ws.send(json.dumps({"action": "reprise", "ok": bool(s), "en_partie": en_partie}))
                if en_partie:
                    couleur = parties_par_nom[utilisateur][1]
                    await ws.send(json.dumps({"type": "local_player", "value": COULEURS[couleur]}))
                    await ws.send(json.dumps(etat_pour(utilisateur)))

            elif action == "attente_partie":
                if utilisateur is None:
                    await ws.send(json.dumps({"action": "erreur", "message": "Non connecté"}))
                    continue
                await creer_partie(utilisateur)

    except websockets.ConnectionClosed:
        pass

    finally:
        if utilisateur and connexions.get(utilisateur) is ws:
            del connexions[utilisateur]
            if utilisateur in attente:
                attente.remove(utilisateur)
            if utilisateur in parties_par_nom:
                taches_abandon[utilisateur] = asyncio.create_task(delai_grace(utilisateur))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
