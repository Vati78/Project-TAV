import asyncio
import json
import secrets
import websockets
import os
import csv
import main as mn

DELAI_GRACE = 10  # secondes avant abandon
FICHIER = "users.csv"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

connexions = {}          # nom -> ws actuelle
sessions = {}            # token -> {"nom": ...}
parties_par_nom = {}     # nom -> Partie
attente = []             # liste de noms
taches_abandon = {}      # nom -> task du délai de grâce
adversaires = {}





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
        partie = mn.Gestionary([2,1,"r",True,[10,1]])

        parties_par_nom[j1] = [partie,0]
        parties_par_nom[j2] = [partie,1]
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


def recevoir_coup(joueur1,joueur2,partie_modifiee,couleur_joueur,coup_joue,type,piece_deplacee):
    partie_modifiee.chess_game.play_move(8 * coup_joue[0] + coup_joue[1], 8 * coup_joue[2] + coup_joue[3], couleur_joueur, True if type == 3 else False)

    print(joueur1,joueur2)

    pass

def envoyer_coup(joueur1,joueur2,partie_modifiee):
    '''
    board = [
    ["br","bn","bb","bq","bk","bb","bn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wn","wb","wq","wk","wb","wn","wr"]
];
    :return:
    -envoyer le plateau
    -coups légaux
    en json
    '''

    pass

def lire_utilisateurs():
    if not os.path.exists(FICHIER):
        return []
    with open(FICHIER, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def verifier(nom, mdp):
    return any(u["username"] == nom and u["password"] == mdp
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
        writer.writerow([nom, mdp])
    return True, "Account created!"


async def handler(ws):
    utilisateur = None
    global attente

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

                print("connexion :", sessions)
                print()

                

            elif action == "quitter_menu":
                token = d.get("token")
                s = sessions.get(token)

                if not s:
                    await ws.send(json.dumps({
                        "action": "erreur",
                        "message": "Session invalide"
                    }))
                    continue

                utilisateur = s["nom"]

                await quitter_partie(utilisateur)

                if utilisateur in attente:
                    attente.remove(utilisateur)

                sessions.pop(token, None)
                connexions.pop(utilisateur, None)

                print("sessions actives :",  sessions)
                print()
                
            elif action == "move":
                token = d.get("token")
                s = sessions.get(token)

                if not s:
                    await ws.send(json.dumps({
                        "action": "erreur",
                        "message": "Session invalide"
                    }))
                    continue

                utilisateur = s["nom"]
                partie_modifiee = parties_par_nom.get(utilisateur)[0]
                couleur_joueur_origine = parties_par_nom.get(utilisateur)[1]

                adversaire_utilisateur = adversaires[utilisateur]
                couleur_adversaire_origine = parties_par_nom.get(adversaire_utilisateur)[1]

                coup_joue = d["value"]
                type = d["special"]
                piece_deplacee = d["piece"]

                recevoir_coup(utilisateur,adversaire_utilisateur,partie_modifiee,couleur_joueur_origine,coup_joue,type,piece_deplacee)

                envoyer_coup(utilisateur,adversaire_utilisateur,partie_modifiee)


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

                    print("reprise effectuée")
                await ws.send(json.dumps({
                    "action": "reprise",
                    "ok": bool(s),
                    "en_partie": utilisateur in parties_par_nom
                }))




            elif action == "attente_partie":
                if utilisateur is None:
                    await ws.send(json.dumps({"action": "erreur", "message": "Non connecté"}))
                    continue
                await creer_partie(utilisateur)
                
                print("listed'attente : ",attente)
                print()

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