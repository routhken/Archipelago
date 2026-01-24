import asyncio
from .EnemyRandomizer import enemyListNonBoss, enemyDangerous
from .SkillRandomizer import skillGroups
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    get_base_parser,
    server_loop,
    ClientCommandProcessor,
    handle_url_arg
)
import subprocess
import os
import shutil
import urllib.parse
from NetUtils import ClientStatus

DEBUG = False
GAMENAME = "Grim Dawn"
ITEMS_HANDLING = 0b000
minimumSupportedVersion = 2.4

class GrimDawnCommandProcessor(ClientCommandProcessor):
    def _cmd_debug_patch(self):
        """Patch game with default connect credentials and slot data"""
        self.ctx.patch_game({})

    def _cmd_list_enemies(self):
        """List enemy rando table"""
        if "enemy_table" in self.ctx.slot_data:
            for enemy in self.ctx.slot_data["enemy_table"]:
                logger.info(f"Enemy entry: {enemy}")
        else:
            logger.info("Enemy Table does not exist in this slot data.")

    def _cmd_list_skills(self):
        """List skill rando table"""
        if "skill_balance_table" in self.ctx.slot_data:
            for skill in self.ctx.slot_data["skill_balance_table"]:
                logger.info(f"Enemy entry: {skill}")
        else:
            logger.info("Skill Balance Table does not exist in this slot data.")

    #def _cmd_goal_game(self):
    #    """Goal the game"""
    #    self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

def simple_line_fix(line_to_fix, fix_value):
    words = line_to_fix.split(",")
    nums = words[1].split(";")
    line = words[0] + ","
    for i in nums:
        line = line + fix_value
    line = line[:-1] + ",\n"
    return line

def patching_sanity_check(patchedValue, attributename):
    #Certain attributes that can have negative modifiers do not function below -100%.
    if attributename in ("skillManaCostReduction"):
        return max(patchedValue,-100)

    #Certain attributes break when over 100%
    if attributename in ("conversionPercentage","skillManaCostReduction","onHitActivationChance","skillChanceWeight","sparkChance","offensiveTauntMin","offensiveSleepChance",
                            "lifeMonitorPercent","offensiveTotalDamageReductionPercentMin","offensiveDisruptionChance","offensiveSlowPhysicalChance","offensiveSlowBleedingChance"
                            "skillCooldownReduction","conversionPercentage2","defensiveDisruption","retaliationStunChance","projectilePiercing","projectilePiercingChance",
                            "offensiveStunChance","offensiveFearChance","skillCooldownReductionChance","offensiveConfusionChance","offensiveKnockdownChance","offensiveFreezeChance",
                            "offensiveLightningChance","offensiveFumbleMin","offensiveProjectileFumbleMin","offensiveGlobalChance","retaliationSlowManaLeachChance",
                            "offensiveSlowLightningChance","offensiveSlowColdChance","offensiveLightningModifierChance","offensiveSlowFireChance","offensiveTrapChance"):
        return min(patchedValue,100)

    #Certain attributes break game balance at 100% or more
    if attributename in ("damageAbsorptionPercent","characterDeflectProjectile","offensivePercentCurrentLifeMin","offensivePercentCurrentLifeMax"):
        return min(patchedValue,85)

    #To ensure skill usability, these attributes cannot be below 1
    if attributename in ("skillTargetNumber","skillProjectileNumber","projectileLaunchNumber","petLimit","petBurstSpawn","sparkMaxNumber","skillChargeLevel",
                            "contagionMaxSpread","contagionLimit","tetherLimit","linkLimit","numProjectiles"):
        return max(patchedValue,1)
    return patchedValue

def patch_game(username, server_address, password, installPath, slot_data: dict[str, any]):
    
# Forth  Run the command from the grim dawn folder: arzedit.exe extract "..\Grim Dawn\mods\archipelago\database\Archipelago.arz" "..\Grim Dawn\mods\patchedMod"
    #This initiates the command line, join adds a slash (os specific) between the arguments
    print("Deleting existing patchedMod files so a new one can build.", end='\r\n')
    patchedMod = "patchedArchipelago"
    subprocess.run([
        "rmdir",
        "/s",
        "/q",
        os.path.join(installPath,"mods",patchedMod),
        ], shell=True)
    print("Extracting database files.", end='\r\n')
    subprocess.run([
        os.path.join(installPath,"arzedit.exe"),
        "extract",
        os.path.join(installPath,"mods","archipelago","database","Archipelago.arz"),
        os.path.join(installPath,"mods",patchedMod),
        "-y",
        ], shell=True)
    
# Fifth  Modify the dbr files based on the table of values stored in slot data that was filled at generate

    if not username:
        slot_name = "Player1"
    else:
        slot_name = username
    #Remove @slotname from the url so it can connect to servers, otherwise an "unrecoverable" socket error could occur
    if not server_address:
        server = "ws://localhost:38281"
    else:
        x = urllib.parse.urlsplit(server_address)
        server = urllib.parse.urlunsplit(x._replace(netloc=x.netloc.rsplit("@", 1)[-1]))
    
    #Iterate through player skills and apply balance patch
    if slot_data.get("skill_balance_randomizer",0) == 1:
        print("Applying skill patch.", end='\r\n')
    for playerclass,skilltable in slot_data.get("skill_balance_table",{}).items():
        for skillname,valuetable in skilltable.items():
            if skillname.startswith("pets/"):
                filepath = os.path.join(*skillname.split("/"))
            else:
                filepath = skillname
            path1 = os.path.join(installPath,"mods",patchedMod,"records","skills",playerclass,filepath)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",playerclass,filepath + "s")
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                for attributename,attributevalue in valuetable.items():
                    # find
                    if line.startswith(attributename + ","):
                        # replace
                        words = line.split(",",2)
                        nums = words[1].split(";")
                        line = words[0] + ","
                        #Lines need to be reconstructed in the format of "attributename,0;1;2;3;4,"
                        for i in nums:
                            patchedValue = (float(i) * attributevalue)
                            line = line + str(patching_sanity_check(patchedValue, attributename)) + ";"
                        line = line[:-1] + ",\n"
                        break
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)
            
    #Apply the devotion skill balance rando patch, if enabled
    for playerclass,skilltable in slot_data.get("devotion_balance_table",{}).items():
        print("Applying devotion patch.", end='\r\n')
        for skillname,valuetable in skilltable.items():
            if skillname.startswith("pets/"):
                filepath = os.path.join(*skillname.split("/"))
            else:
                filepath = skillname
            path1 = os.path.join(installPath,"mods",patchedMod,"records","skills",playerclass,filepath)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",playerclass,filepath + "x")
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                for attributename,attributevalue in valuetable.items():
                    # find
                    if line.startswith(attributename + ","):
                        # replace
                        words = line.split(",",2)
                        nums = words[1].split(";")
                        line = words[0] + ","
                        #Lines need to be reconstructed in the format of "attributename,0;1;2;3;4,"
                        for i in nums:
                            patchedValue = (float(i) * attributevalue)
                            line = line + str(patching_sanity_check(patchedValue, attributename)) + ";"
                        line = line[:-1] + ",\n"
                        break
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)
            
    #Apply the skill shuffle patch, if enabled
    #print("Slot data skill shuffle: " + str(slot_data.get("skill_shuffler",0)), end='\r\n')
    if slot_data.get("skill_shuffler",0) == 1:
        logger.info("Applying skill shuffle patch.")
        print("Applying skill shuffle patch.", end='\r\n')
        #print("Inside skill shuffle function", end='\r\n')
        #First make a copy of every skill so we can read from them without overwriting them.
        tempStoragePath = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills")
        sourceDirectoryPath = os.path.join(installPath,"mods",patchedMod,"records","skills")
        shutil.copytree(sourceDirectoryPath,tempStoragePath)
        #For every skill
        # groupIndex = 0
        for groupIndex, skillGroup in enumerate(slot_data["skill_shuffle_table"]):
        # for skillGroup in slot_data["skill_shuffle_table"]:
            #print("Skill Group: " + str(skillGroup), end='\r\n')
            #Need to iterate through the randomized list while iterating through the true list.
            startingIndex = 0
            index = startingIndex
            # dangerIndex = len(slot_data["skill_shuffle_table"][groupIndex]) #(len(enemyDangerous))
            #randomSkillList = list(reversed(skillGroups[groupIndex]))
            baseSortedSkillGroup = sorted(skillGroups[groupIndex])
            for baseName,targetName in zip(baseSortedSkillGroup, skillGroup):
            # for targetName in skillGroup:
                #Skill names are "playerClass/skillName" which is to mimic the file structure
                targetClassSkill = targetName.split("/")
                sourceClassSkill = baseName.split("/") #slot_data["shuffle_table"][index])
                if sourceClassSkill[1] == "pets":
                    path1 = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills",sourceClassSkill[0],sourceClassSkill[1],sourceClassSkill[2])
                else:
                    path1 = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills",sourceClassSkill[0],sourceClassSkill[1])
                if targetClassSkill[1] == "pets":
                    path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",targetClassSkill[0],targetClassSkill[1],targetClassSkill[2])
                else:
                    path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",targetClassSkill[0],targetClassSkill[1])
                # if sourceClassSkill[1] in ("presenceofvirtue1_buff.dbr"):
                #     print("  Source Skill Name: " + sourceClassSkill[1], end='\r\n')
                # if targetClassSkill[1] in ("presenceofvirtue1_buff.dbr"):
                #     print("  Target Skill Name: " + targetClassSkill[1], end='\r\n')
                #To avoid messing up the skill window UI, the skill connector information needs remain where it was
                #But since writing into a file immediately overwrites its contents, the info needs to be copied out first
                print(" Skill Shuffle: Source -> Target: " + baseName + " -> " + targetName, end='\r\n')
                #print("  Target Skill Name: " + str(path2), end='\r\n')
                ftemp = open(path2, 'r')
                skillConnectionOff = ""
                skillConnectionOn = ""
                skillTier = ""
                for line in ftemp:
                    if line.startswith(("skillConnectionOff,")):
                        words = line.split(",",2)
                        skillConnectionOff = words[1]
                        #logger.info("skillConnectionOff = " + skillConnectionOff)
                    if line.startswith(("skillConnectionOn,")):
                        words = line.split(",",2)
                        skillConnectionOn = words[1]
                    if line.startswith(("skillTier,")):
                        words = line.split(",",2)
                        skillTier = words[1]
                # if sourceClassSkill[1] in ("presenceofvirtue1_buff.dbr"):
                #     print("  Source skillConnectionOn: " + skillConnectionOn, end='\r\n')
                #     print("  Source skillTier: " + skillTier, end='\r\n')
                # if targetClassSkill[1] in ("presenceofvirtue1_buff.dbr"):
                #     print("  Target skillConnectionOn: " + skillConnectionOn, end='\r\n')
                #     print("  Target skillTier: " + skillTier, end='\r\n')
                ftemp.close()
                #Now the file can be overwritten with the new skill
                f1 = open(path1, 'r')
                f2 = open(path2, 'w')
                for line in f1:
                    #Erase skill connectors from the incoming skill to replace it with the old one
                    if line.startswith(("skillConnectionOff,")):
                        line = ("")
                    if line.startswith(("skillConnectionOn,")):
                        line = ("")
                    if line.startswith(("skillTier,")):
                        line = ("skillTier," + skillTier + ",\n")
                    f2.write(line)
                f2.write("skillConnectionOff," + skillConnectionOff + ",\n")
                f2.write("skillConnectionOn," + skillConnectionOn + ",\n")
                f1.close()
                f2.close()

                #For skills that are two-part files, the second part needs the "buffSkillName" line edited to the new filepath of the shuffled skill. Otherwise the skill properties will possibly make it unusable.
                if baseName in ("playerclass03/bloodofdreeg1_buff.dbr","playerclass03/curse1_buff.dbr","playerclass03/pox1_buff.dbr","playerclass04/bladetrap1_buff.dbr","playerclass05/chillingsurge_buff.dbr",
                                  "playerclass06/devouringswarm1_buff.dbr","playerclass07/hunteraura1_buff.dbr","playerclass07/lightningnet1_buff.dbr","playerclass07/wordofpain1_buff.dbr","playerclass08/illomen1_buff.dbr",
                                  "playerclass08/soulsiphon1_buff.dbr","playerclass01/fieldcommand1buff.dbr","playerclass02/blastshield1_buff.dbr","playerclass04/veilofshadows1_buff.dbr",
                                  "playerclass05/elementalinfusion1_buff.dbr","playerclass06/natureblessing1_buff.dbr","playerclass07/auracensure1_buff.dbr","playerclass07/auraconviction1_buff.dbr",
                                  "playerclass09/presenceofvirtue1_buff.dbr"):
                    #Use the :-9 to truncate the _buff part from the skill name, since the file which points to this skill is the same name minus the _buff
                    path1 = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills",sourceClassSkill[0],(sourceClassSkill[1][:-9]) + ".dbr")
                    path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",targetClassSkill[0],(targetClassSkill[1][:-9]) + ".dbr")
                    print("Two part file path2: " + str(path2))
                    print("Two part file path1: " + str(path1))
                    print("Base skill index: " + baseName)
                    print("Target name: " + targetName)
                    if baseName == "playerclass01/fieldcommand1buff.dbr":
                        #For some reason, field command is the only two part skill missing the underscore in its name. idk I didn't make this game.
                        path1 = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills",sourceClassSkill[0],(sourceClassSkill[1][:-8]) + ".dbr")
                        print("Two part file path EDITED: " + str(path1))
                    if targetName == "playerclass01/fieldcommand1buff.dbr":
                        #For some reason, field command is the only two part skill missing the underscore in its name. idk I didn't make this game.
                        path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",targetClassSkill[0],(targetClassSkill[1][:-8]) + ".dbr")
                        print("Two part file path EDITED: " + str(path2))
                    f1 = open(path1, 'r')
                    f2 = open(path2, 'w')
                    for line in f1:
                        #These files are very short and the only thing that needs to change is the pointer to the skill's new file path from being shuffled
                        if line.startswith(("buffSkillName,")):
                            line = simple_line_fix(line, ("records/skills/" + targetClassSkill[0] + "/" + targetClassSkill[1] + ";"))
                        f2.write(line)

                index += 1
                # if not (index < dangerIndex):
                #     index = startingIndex
            # groupIndex += 1
            
        #Delete the tempStorage so it doesn't extend build time
        shutil.rmtree(tempStoragePath)
    
    #Apply the free respec patch, if enabled
    if slot_data.get("free_skill_respec",0) == 1:
        print("Applying skill respec patch.", end='\r\n')
        for filename in ("malepc01.dbr","femalepc01.dbr"):
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename + "y")
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                if line.startswith(("devotionReclamationAetherCost,","devotionReclamationPointCosts,","reclamationPointCosts,")):
                    line = simple_line_fix(line, "0;")
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)

    #Apply the enemy rando patch, if enabled
    if slot_data.get("enemy_randomizer",0) == 1:
        print("Applying enemy rando patch.", end='\r\n')
        #First make a copy of every enemy so we can read from them without overwriting them.
        tempStoragePath = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage")
        os.makedirs(tempStoragePath)
        for sourceName in enemyListNonBoss:
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",sourceName)
            shutil.copy(path1,tempStoragePath)
        #logger.info("singletonEnemy: " + singletonEnemy[0] + singletonEnemy[1] + singletonEnemy[2] + singletonEnemy[3])
        #logger.info("path1: " + path1)
        startingIndex = 0
        dangerIndex = len(slot_data["enemy_table"]) #(len(enemyDangerous))
        index = startingIndex
        #shouldLog = True
        #logger.info(f"Length of dangerous enemies list: {dangerIndex}")
        speedMultiplier = 1.00
        levelModifier = 0
        if slot_data.get("buff_enemies",2) == 0:
            speedMultiplier = 0.60
            levelModifier = -3
        elif slot_data.get("buff_enemies",2) == 1:
            speedMultiplier = 0.85
            levelModifier = -1
        elif slot_data.get("buff_enemies",2) == 3:
            speedMultiplier = 1.15
            levelModifier = 1
        elif slot_data.get("buff_enemies",2) == 4:
            speedMultiplier = 1.40
            levelModifier = 3
        for targetName in enemyListNonBoss:
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage",slot_data["enemy_table"][index])
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
            print(" Enemy Rando: Source -> Target: " + slot_data["enemy_table"][index] + " -> " + targetName, end='\r\n')
            #open the file we'll soon be writing to and extract some variable info to write back into it later, preserving certain variables we don't want to change
            ftemp = open(path2, 'r')
            factions = ""
            for line in ftemp:
                if line.startswith(("factions,")):
                    words = line.split(",",2)
                    factions = words[1]
                    #logger.info("factions = " + factions)
            ftemp.close()
            #Now the file can be overwritten with the new enemy
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                #Preserve enemy factions to reduce infighting
                if line.startswith(("factions,")):
                    line = simple_line_fix(line, factions + ";")
                #Make all enemies give exp
                if line.startswith(("giveXP,")):
                    line = simple_line_fix(line, "1;")
                #Make all enemies give non-zero exp
                if line.startswith(("experiencePoints,")):
                    words = line.split(",")
                    nums = words[1].split(";")
                    line = words[0] + ","
                    for i in nums:
                        if int(i) == 0:
                            line = line + "150;"
                        else:
                            line = line + words[1]
                    line = line[:-1] + ",\n"
                #Check for dynamic weapon loot tables in enemy files and replace them with generic ones.
                #  Otherwise if a dynamic loot drop gets transferred to an enemy with no equipped loot to drop, it crashes the game.
                # if line.startswith(("loot")):
                #     words = line.split(",")
                #     nums = words[1].split(";")
                #     line = words[0] + ","
                #     for i in nums:
                #         if "tdyn" in i:
                #             line = line + "records/items/loottables/mastertables/mt_compall_a01.dbr;"
                #         else:
                #             line = line + words[1]
                #     line = line[:-1] + ",\n"
                #Makes enemies only ever alerted by the player, making them not fight each other
                # if line.startswith(("angerMultiplier")):
                #     line = simple_line_fix(line, "0;")
                # if line.startswith(("causesAnger")):
                #     line = simple_line_fix(line, "0;")
                # if line.startswith(("distressCallRange")):
                #     line = simple_line_fix(line, "100;")
                # if line.startswith(("distressCall")):
                #     line = simple_line_fix(line, "1;")
                #The remaining lines are buffing/nerfing enemies based on chosen options
                if slot_data.get("buff_enemies",2) != 2:
                    #Action speed
                    if line.startswith(("characterAttackSpeed,","characterAttackSpeedModifier,","characterSpellCastSpeed,","characterSpellCastSpeedModifier,")): #,"characterRunSpeed,","characterRunSpeedModifier,","walkSpeed,")):
                        words = line.split(",")
                        nums = words[1].split(";")
                        line = words[0] + ","
                        for i in nums:
                            line = line + str(float(i) * speedMultiplier) + ";"
                        line = line[:-1] + ",\n"
                    #Size, also affects movement speed
                    if line.startswith(("scale,")):
                        words = line.split(",")
                        nums = words[1].split(";")
                        line = words[0] + ","
                        for i in nums:
                            line = line + str(float(i) * speedMultiplier) + ";"
                        line = line[:-1] + ",\n"
                    #Level of skills, cause enemies to do a ton more damage
                    if line.startswith(("skillLevel")):
                        words = line.split(",")
                        nums = words[1].split(";")
                        line = words[0] + ","
                        for i in nums:
                            line = line + i + "+(" + str(levelModifier) + ");"
                        line = line[:-1] + ",\n"
                f2.write(line)
            f1.close()
            f2.close()
            #if shouldLog:
                #logger.info(f"Enemy entry {index}: " + slot_data["enemy_table"][index])
            index += 1
            if not (index < dangerIndex):
                index = startingIndex
                #shouldLog = False
            
        #Delete the tempStorage so it doesn't extend build time
        shutil.rmtree(tempStoragePath)
        
# Sixth  Run the command from the grim dawn folder: arzedit.exe build "..\Grim Dawn\mods\patchedMod" "..\Grim Dawn\mods\patchedMod" -g "..\Grim Dawn"

    print("Building database files.", end='\r\n')
    subprocess.run([
        os.path.join(installPath,"arzedit.exe"),
        "build",
        os.path.join(installPath,"mods",patchedMod),
        os.path.join(installPath,"mods",patchedMod),
        "-g",
        installPath,
        ], shell=True)
    
# Seven  Delete the extracted files, leaving behind only the compiled mod files: rmdir /s /q "..\Grim Dawn\mods\patchedMod\records"

    print("Deleting temp files.", end='\r\n')
    subprocess.run([
        "rmdir",
        "/s",
        "/q",
        os.path.join(installPath,"mods",patchedMod,"records"),
        ], shell=True)
    
# Eight  Copy arc files to new mod location: xcopy "..\Grim Dawn\mods\archipelago\resources" "..\Grim Dawn\mods\patchedArchipelago\resources" /i /y

    print("Copying arc files.", end='\r\n')
    subprocess.run([
        "xcopy",
        os.path.join(installPath,"mods","archipelago","resources"),
        os.path.join(installPath,"mods",patchedMod,"resources"),
        "/i",
        "/y",
        ], shell=True)
    
# Ninth  Create a txt file containing connection info: echo message > "C:\SteamSuperSSD\steamapps\common\Grim Dawn\mods\patchedArchipelago\a.txt"

    print("Creating connect txt file.", end='\r\n')
    with open(os.path.join(installPath,"connect.txt"), "w") as file:
        file.write("host = " + server + "\nslot = " + slot_name + "\npassword = " + (password if password else "") + "\nssp = " + ("true" if slot_data.get("starting_skill_points",0) == 1 else "false"))
    logger.info("Patching finished.")

class ProxyGameContext(CommonContext):
    game = GAMENAME
    items_handling = ITEMS_HANDLING
    command_processor = GrimDawnCommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.slot_data = {"enemy_table": [], "skill_balance_table": [], "devotion_balance_table": []}
        
    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == 'Connected':
            from Utils import async_start
            self.slot_data = args["slot_data"]
            from worlds.LauncherComponents import launch_subprocess
        # First  confirm the path to the grim dawn executable upon startup
            from . import GrimDawnWorld
            installPath = GrimDawnWorld.settings.grimDawnInstallPath
            print(f"Grim Dawn install path is: {installPath}")

        # Second confirm that the mod is a supported version for this apworld
            dontContinue = False
            
            #isfile returns true if the file is found, join adds a slash (os specific) between the arguments
            if not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","ver.txt")):
                logger.info("Missing mod files. Make sure you are using the latest mod.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\database\ver.txt")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True

            #Version file found, now read the file to find the version number
            else:
                modVersion = 0
                f_ver = open(os.path.join(installPath,"mods","archipelago","database","ver.txt"), 'r')
                for line in f_ver:
                    if line.startswith(("version,")):
                        words = line.split(",")
                        modVersion = float(words[1])
                f_ver.close()
                if modVersion < minimumSupportedVersion:
                    logger.info(f"Mod version {modVersion} not supported, need at least v{minimumSupportedVersion}")
                    dontContinue = True

        # Third  confirm that all the required files for archipelago grim dawn are installed correctly

            if not os.path.isfile(os.path.join(installPath,"arzedit.exe")):
                logger.info("arzedit is not in your Grim Dawn install directory.")
                logger.info(r"Expected path: ...\Grim Dawn\arzedit.exe")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True

            if not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","Archipelago.arz")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed. Missing mod files.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\database\Archipelago.arz")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Conversations.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed. Missing mod files.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Conversations.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Quests.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed. Missing mod files.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Quests.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Scripts.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed. Missing mod files.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Scripts.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"lua51.dll")):
                logger.info("Missing lua51.dll in your Grim Dawn install directory")
                logger.info(r"Expected path: ...\Grim Dawn\lua51.dll")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"real_lua51.dll")):
                logger.info("Missing real_lua51.dll in your Grim Dawn install directory")
                logger.info(r"Expected path: ...\Grim Dawn\real_lua51.dll")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if not os.path.isfile(os.path.join(installPath,"lua-apclientpp.dll")):
                logger.info("Missing lua-apclientpp.dll in your Grim Dawn install directory")
                logger.info(r"Expected path: ...\Grim Dawn\lua-apclientpp.dll")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
                dontContinue = True
            
            if dontContinue == True:
                logger.info("Patching aborted.")
                logger.info("If the current install directory is wrong, you can change it in the host.yaml in your archipelago install folder.")

            else:
                logger.info("Grim Dawn Archipelago installation found.")
                logger.info("Patching game. Please wait 30 seconds before starting a save file.")
                launch_subprocess(patch_game, "patchgame", (self.username, self.server_address, self.password, installPath, args["slot_data"],))
                #self.patch_game(self.username, self.server_address, self.password, args["slot_data"])
                #await self.update_death_link(args["slot_data"]["deathlink"])
                async_start(self.update_death_link(bool(args["slot_data"]["deathlink"])))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

async def main(args):

    ctx = ProxyGameContext(args.connect, args.password)

    ctx.server_task = asyncio.create_task(
        server_loop(ctx),
        name="server loop"
        )

    if gui_enabled:
        ctx.run_gui()
        ctx.ui.base_title = "Grim Dawn Client"
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args):
    import colorama

    parser = get_base_parser(
        description="Grim Dawn Archipelago Client."
        )
    parser.add_argument("url", nargs="?", help="Archipelago Webhost url to auto connect to.")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    colorama.init()
    print(args) #TODO DEBUG
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch()