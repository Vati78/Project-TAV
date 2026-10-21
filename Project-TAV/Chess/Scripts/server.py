import asyncio
import csv
import json
import os
import websockets

FICHIER = "users.csv"

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
    async for message in ws:
        d = json.loads(message)

        if d["action"] == "connexion":
            ok = verifier(d["nom"], d["mdp"])
            await ws.send(json.dumps({"action": "connexion", "ok": ok}))

        elif d["action"] == "creation":
            ok, msg = creer(d["nom"], d["mdp"])
            await ws.send(json.dumps({"action": "creation", "ok": ok, "message": msg}))

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())