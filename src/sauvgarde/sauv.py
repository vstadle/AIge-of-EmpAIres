import json  

def sauvegarder_partie(etat, fichier):
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(etat, f, ensure_ascii=False, indent=4)
    print(f"Partie sauvegardée dans {fichier}.")



def charger_partie(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)


etat_partie = {
    "niveau": 3,
    "score": 1500,
    "joueur": "Alice",
    "inventaire": ["épée", "bouclier", "potion"]
}


sauvegarder_partie(etat_partie, "sauvegarde.json")


etat_charge = charger_partie("sauvegarde.json")
print("Partie chargée :", etat_charge)

