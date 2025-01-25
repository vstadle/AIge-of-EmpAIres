from model.Archer import Archer
from model.Villager import Villager
from model.Horseman import Horseman
from model.Swordsman import Swordsman
from model.Farm import Farm
from model.Camp import Camp
from model.ArcheryRange import ArcheryRange
from model.Barracks import Barracks
from model.House import House
from model.Keep import Keep
from model.Stable import Stable
from model.TownCenter import TownCenter
from logs.logger import logs

import os
import logging

def generateHtml(lstPlayers):
    current_path = os.getcwd() + "/web/index.html"
    clear_html(current_path)
    logs("Generating HTML", level=logging.INFO)
    content = ""
    for player in lstPlayers:
        units_type = calculate_unit(player.getPlayer())
        buildings_type = calculate_building(player.getPlayer())
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
            <p>Number of Villager: {units_type[0]}</p>
            <p>Number of Archer: {units_type[1]}</p>
            <p>Number of Horseman: {units_type[2]}</p>
            <p>Number of Swordsman: {units_type[3]}</p>
            <ul>
                {''.join([f"<li>{unit}</li>" for unit in player.getPlayer().units])}
            </ul>
        </div>
        <div class="buildings">
            <h3>Buildings</h3>
            <p>Number of TownCenter: {buildings_type[0]}</p>
            <p>Number of Farm: {buildings_type[1]}</p>
            <p>Number of Camp: {buildings_type[2]}</p>
            <p>Number of Archery Range: {buildings_type[3]}</p>
            <p>Number of Barracks: {buildings_type[4]}</p>
            <p>Number of House: {buildings_type[5]}</p>
            <p>Number of Keep: {buildings_type[6]}</p>
            <p>Number of Stable: {buildings_type[7]}</p>
            <ul>
                {''.join([f"<li>{building}</li>" for building in player.getPlayer().buildings])}
            </ul>
        </div>
        """
    
    insert_html(content, current_path)
    logs("HTML generated", level=logging.INFO)

def calculate_unit(player):
    cptVillager = 0
    cptArcher = 0
    cptHorseman = 0
    cptSwordsman = 0

    for unit in player.units:
        if type(unit) == Villager:
            cptVillager += 1
        elif type(unit) == Archer:
            cptArcher += 1
        elif type(unit) == Horseman:
            cptHorseman += 1
        elif type(unit) == Swordsman:
            cptSwordsman += 1
    units = [cptVillager, cptArcher, cptHorseman, cptSwordsman]
    return units

def calculate_building(player):
    cptTownCenter = 0
    cptFarm = 0
    cptCamp = 0
    cptArcheryRange = 0
    cptBarracks = 0
    cptHouse = 0
    cptKeep = 0
    cptStable = 0

    for building in player.buildings:
        if type(building) == TownCenter:
            cptTownCenter += 1
        elif type(building) == Farm:
            cptFarm += 1
        elif type(building) == Camp:
            cptCamp += 1
        elif type(building) == ArcheryRange:
            cptArcheryRange += 1
        elif type(building) == Barracks:
            cptBarracks += 1
        elif type(building) == House:
            cptHouse += 1
        elif type(building) == Keep:
            cptKeep += 1
        elif type(building) == Stable:
            cptStable += 1
    buildings = [cptTownCenter, cptFarm, cptCamp, cptArcheryRange, cptBarracks, cptHouse, cptKeep, cptStable]
    return buildings

def insert_html(content, current_path):
    # Assure-toi que tu as bien le chemin complet vers ton fichier HTML
    with open(current_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        updated_lines.append(line)
        if "<main id='game-state'>" in line:
            updated_lines.append(content + "\n")

    # Toujours fermer après avoir écrit
    with open(current_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

def clear_html(current_path):
    with open(current_path, "r", encoding="utf-8") as f:
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
    
    with open(current_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)
