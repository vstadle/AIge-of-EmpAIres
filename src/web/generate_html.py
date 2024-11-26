import model.Game as Game

def generateHtml(lstPlayers):
    clear_html()
    print("Generating HTML")
    print(lstPlayers)
    content = ""
    for player in lstPlayers:
        content += f"""
        <h2>{player.getPlayer().name}</h2>
        <div class="ressources">
            <h3>Ressources</h3>
            <p>Food: {player.getPlayer().food}</p>
            <p>Wood: {player.getPlayer().wood}</p>
            <p>Gold: {player.getPlayer().gold}</p>
        </div>
        <div class="units">
            <h3>Units</h3>
            <p>Number of Units: {len(player.getPlayer().units)}</p>
            <ul>
                {''.join([f"<li>{unit}</li>" for unit in player.getPlayer().units])}
            </ul>
        </div>
        <div class="buildings">
            <h3>Buildings</h3>
            <p>Number of Buildings: {len(player.getPlayer().buildings)}</p>
            <ul>
                {''.join([f"<li>{building}</li>" for building in player.getPlayer().buildings])}
            </ul>
        </div>
        """
    
    insert_html(content)

def insert_html(content):
    # Assure-toi que tu as bien le chemin complet vers ton fichier HTML
    with open("D:/AIge-of-EmpAIres/src/web/index.html", "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        updated_lines.append(line)
        if "<main id='game-state'>" in line:
            updated_lines.append(content + "\n")

    # Toujours fermer après avoir écrit
    with open("D:/AIge-of-EmpAIres/src/web/index.html", "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

def clear_html():
    with open("D:/AIge-of-EmpAIres/src/web/index.html", "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    erase = False
    for line in lines:
        if not erase:
            updated_lines.append(line)
        if "<main id='game-state'>" in line:
            erase = True
        if "</main>" in line:
            erase = False
            updated_lines.append(line)
    
    with open("D:/AIge-of-EmpAIres/src/web/index.html", "w", encoding="utf-8") as f:
        f.writelines(updated_lines)
