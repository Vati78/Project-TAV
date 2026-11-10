import asyncio
import json
import secrets
import websockets
import os
import csv

DELAI_GRACE = 10  # secondes avant abandon
FICHIER = "users.csv"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

connexions = {}          # nom -> ws actuelle
sessions = {}            # token -> {"nom": ...}
parties_par_nom = {}     # nom -> Partie
attente = []             # liste de noms
taches_abandon = {}      # nom -> task du délai de grâce


class Partie:
    def __init__(self, j1, j2):
        self.joueurs = [j1, j2]   # noms
        self.tour = 0

    def adversaire(self, nom):
        return self.joueurs[1] if nom == self.joueurs[0] else self.joueurs[0]


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
        partie = Partie(j1, j2)
        parties_par_nom[j1] = partie
        parties_par_nom[j2] = partie
        await envoyer(j1, {"action": "partie_trouvee", "couleur": 0})
        await envoyer(j2, {"action": "partie_trouvee", "couleur": 1})


async def quitter_partie(nom):
    partie = parties_par_nom.pop(nom, None)
    if partie:
        adv = partie.adversaire(nom)
        parties_par_nom.pop(adv, None)
        await envoyer(adv, {"action": "adversaire_parti"})



async def delai_grace(nom):
    await asyncio.sleep(DELAI_GRACE)
    taches_abandon.pop(nom, None)
    await quitter_partie(nom)


def recevoir_coup():
    pass

def envoyer_coup():
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
                print("#")
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

                print(sessions)
                



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