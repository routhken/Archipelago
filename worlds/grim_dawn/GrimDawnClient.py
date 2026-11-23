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
from tkinter import messagebox
from . import GrimDawnWorld
import urllib.request
import zipfile

DEBUG = False
GAMENAME = "Grim Dawn"
ITEMS_HANDLING = 0b000
minimumSupportedVersion = 3.0
apworldVersion = "0.5.0"
supportedAPworldVersions = ("0.4.0","0.4.1","0.4.2","0.5.0")
hasGrimDawn = True
hasMod = True
hasArzedit = True
hasHeinerLua = True
hasGrimRealLua = False
hasGrimBaseLua = True
hasLuaClient = True
dontContinue = False

class GrimDawnCommandProcessor(ClientCommandProcessor):
    def _cmd_patch(self):
        """Patch the game with current connect credentials and slot data"""
        self.ctx.patchGame()

    def _cmd_list_enemies(self):
        """Outputs enemy rando table to a log file"""
        self.ctx.logEnemyTable()

    def _cmd_list_skills(self):
        """Outputs skill rando table to a log file"""
        self.ctx.logSkillTable()

    #def _cmd_goal_game(self):
    #    """DEBUG Goal the game"""
    #    self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

#Replaces an existing value with a new value
def simple_line_fix(line_to_fix, fix_value):
    words = line_to_fix.split(",",2)
    nums = words[1].split(";")
    line = words[0] + ","
    for i in nums:
        line = line + fix_value
    line = line[:-1] + ",\n"
    return line

#Multiplies an existing value with a scalar
def simple_line_scale(line_to_scale, scale_value):
    words = line_to_scale.split(",",2)
    nums = words[1].split(";")
    line = words[0] + ","
    for i in nums:
        line = line + str(float(i) * scale_value) + ";"
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
    logPath = os.path.join(installPath,"mods","PatcherLog.txt")
    try:
    # Forth  Run the command from the grim dawn folder: arzedit.exe extract "..\Grim Dawn\mods\archipelago\database\Archipelago.arz" "..\Grim Dawn\mods\patchedMod"
        # This initiates the command line, join adds a slash (os specific) between the arguments
        with open(logPath, "a") as f:
            f.write(f"Patching Game\nDeleting existing patchedMod files so a new one can build\n")
        patchedMod = "patchedArchipelago"
        env = os.environ.copy()
        for name, value in env.items():
            with open(logPath, "a") as f:
                f.write(f"Environment name,value: {name} -> {value}\n")
        subprocess.run([
            "rmdir",
            "/s",
            "/q",
            os.path.join(installPath,"mods",patchedMod),
            ], shell=True)
        with open(logPath, "a") as f:
            f.write(f"Extracting database files\n")
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
        # if slot_data.get("skill_balance_randomizer",0) == 1:
        with open(logPath, "a") as f:
            f.write(f"Applying skill patch\n")
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
                        if line.startswith(("spawnObjectsTimeToLive,","modSpawnObjectsTimeToLive,")):
                            if slot_data.get("pets_forever",0) == 1:
                                line = ""
                        elif line.startswith(attributename + ","):
                            # replace
                            # Incoming lines will be in the format of "attributename,0;1.000;2.000;3.000;4.000,
                            # If the user is in a region where the decimal separator is not a full stop, then arzedit will extract lines from db files like that
                            # and throw an exception here, which we want so we can yell at the user with an error message.
                            words = line.split(",",1)
                            numWords = words[1].rsplit(",",1)
                            nums = numWords[0].split(";")
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

        #Iterate through enemy skills and apply patch
        if slot_data.get("ultra_rapid_fire",0) == 1:
            with open(logPath, "a") as f:
                f.write(f"Applying enemy skill patch for ultra rapid fire\n")
            for directory in ("nonplayerskills","nonplayerskillsgdx1","nonplayerskillsgdx2","nonplayerskillsgdx3"):
                enemyskillroot = os.path.join(installPath,"mods",patchedMod,"records","skills",directory)
                # os walk return a tuple of three things: parent directory, sub folders, files
                # This list comprehension returns just the list of files we need to iterate over
                for enemyskillpath in [os.path.join(dir_name, file) for dir_name, folders, files in os.walk(enemyskillroot) for file in files]:
                    with open(logPath, "a") as f:
                        f.write(f"Enemy skill path: {enemyskillpath}\n")
                    f1 = open(enemyskillpath, 'r')
                    f2 = open(enemyskillpath + "s", 'w')
                    for line in f1:
                        if line.startswith(("skillCooldownReductionModifier,","skillManaCostReductionModifier,")):
                            line = simple_line_fix(line, "85;")
                        f2.write(line)
                    f1.close()
                    f2.close()
                    os.replace(enemyskillpath + "s",enemyskillpath)

        #Iterate through devotion shrines and apply patch
        if slot_data.get("easy_shrine_cost",0) == 1:
            with open(logPath, "a") as f:
                f.write(f"Applying devotion shrine patch\n")
            devotionshrineroot = os.path.join(installPath,"mods",patchedMod,"records","interactive")
            # os walk return a tuple of three things: parent directory, sub folders, files
            # This list comprehension returns just the list of files we need to iterate over
            for devotionshrinepath in [os.path.join(dir_name, file) for dir_name, folders, files in os.walk(devotionshrineroot) for file in files]:
                f1 = open(devotionshrinepath, 'r')
                f2 = open(devotionshrinepath + "s", 'w')
                for line in f1:
                    if line.startswith(("epicOffering1,","epicOffering2,","epicOffering3,","legendaryOffering1,","legendaryOffering2,","legendaryOffering3,","normalOffering1,","normalOffering2,","normalOffering3,")):
                        if slot_data.get("easy_shrine_cost",0) == 1:
                            line = simple_line_fix(line, "records/items/materia/compa_aethercrystal.dbr,")
                    f2.write(line)
                f1.close()
                f2.close()
                os.replace(devotionshrinepath + "s",devotionshrinepath)
                
        #Iterate through game engine files and apply patch
        with open(logPath, "a") as f:
            f.write(f"Applying game engine patch\n")
        gameengineroot = os.path.join(installPath,"mods",patchedMod,"records","game")
        # os walk return a tuple of three things: parent directory, sub folders, files
        # This list comprehension returns just the list of files we need to iterate over
        for gameenginepath in [os.path.join(dir_name, file) for dir_name, folders, files in os.walk(gameengineroot) for file in files]:
            f1 = open(gameenginepath, 'r')
            f2 = open(gameenginepath + "s", 'w')
            with open(logPath, "a") as f:
                f.write(f"Game engine root file name: {gameenginepath}\n")
            for line in f1:
                if slot_data.get("third_person_camera",0) == 1:
                    if line.startswith("CameraPitchDefault,"):
                        line = simple_line_fix(line, "11.000000,")
                    if line.startswith("CameraPitchMax,"):
                        line = simple_line_fix(line, "15.000000,")
                    if line.startswith("CameraPitchMin,"):
                        line = simple_line_fix(line, "5.000000,")
                if str(gameenginepath).endswith("gamerandomizerweights.dbr"):
                    if line.startswith("templateName"):
                        pass
                    # Ruthless
                    elif slot_data.get("generic_gear_quality",2) == 0:
                        if line.startswith("noPrefixNoSuffix"):
                            line = simple_line_fix(line, "9999.000000,")
                        else:
                            line = simple_line_fix(line, "0.000000,")
                    # Sparse
                    elif slot_data.get("generic_gear_quality",2) == 1:
                        if line.startswith("noPrefixNoSuffix"):
                            line = simple_line_fix(line, "2000.000000,")
                        else:
                            line = simple_line_scale(line, 0.5)
                    # Generous
                    elif slot_data.get("generic_gear_quality",2) == 3:
                        if line.startswith("rareBoth"):
                            line = simple_line_scale(line, 2)
                        else:
                            line = simple_line_scale(line, 0.5)
                    # Luxurious
                    elif slot_data.get("generic_gear_quality",2) == 4:
                        if line.startswith("rareBoth"):
                            line = simple_line_fix(line, "9999.000000,")
                        else:
                            line = simple_line_fix(line, "0.000000,")
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(gameenginepath + "s",gameenginepath)
                
        #Apply the devotion skill balance rando patch, if enabled
        for playerclass,skilltable in slot_data.get("devotion_balance_table",{}).items():
            with open(logPath, "a") as f:
                f.write(f"Applying devotion patch\n")
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
        if slot_data.get("skill_shuffler",0) == 1:
            with open(logPath, "a") as f:
                f.write(f"Applying skill shuffle patch\n")
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
                    with open(logPath, "a") as f:
                        f.write(f"Skill Shuffle: Source -> Target: {baseName} -> {targetName}\n")
                    ftemp = open(path2, 'r')
                    # skillClass = ""
                    skillConnectionOff = ""
                    skillConnectionOn = ""
                    skillTier = ""
                    for line in ftemp:
                        # if line.startswith(("Class,")):
                        #     words = line.split(",",2)
                        #     skillClass = words[1]
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
                        # if line.startswith(("Class,")):
                        #     # If current skill group is not the first skill in a tree, preserve their classification
                        #     if groupIndex == 0 or groupIndex == 2 or groupIndex == 3 or groupIndex == 4:
                        #         line = ("Class," + skillClass + ",\n")
                        if line.startswith(("skillConnectionOff,")):
                            line = ("")
                        if line.startswith(("skillConnectionOn,")):
                            line = ("")
                        if line.startswith(("skillTier,")):
                            line = ("skillTier," + skillTier + ",\n")
                        #Remove dependancies when shuffler is enabled or else it will likely depend on a skill in another mastery
                        if line.startswith(("skillDependancy,")):
                            line = ("")
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
                        with open(logPath, "a") as f:
                            f.write(f"Two part file path2: {path2}\nTwo part file path1: {path1}\nBase skill index: {baseName}\nTarget name: {targetName}\n")
                        if baseName == "playerclass01/fieldcommand1buff.dbr":
                            #For some reason, field command is the only two part skill missing the underscore in its name. idk I didn't make this game.
                            path1 = os.path.join(installPath,"mods",patchedMod,"records","tempStorage","skills",sourceClassSkill[0],(sourceClassSkill[1][:-8]) + ".dbr")
                            with open(logPath, "a") as f:
                                f.write(f"Two part file path EDITED: {path1}\n")
                        if targetName == "playerclass01/fieldcommand1buff.dbr":
                            #For some reason, field command is the only two part skill missing the underscore in its name. idk I didn't make this game.
                            path2 = os.path.join(installPath,"mods",patchedMod,"records","skills",targetClassSkill[0],(targetClassSkill[1][:-8]) + ".dbr")
                            with open(logPath, "a") as f:
                                f.write(f"Two part file path EDITED: {path2}\n")
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
        
        #Apply player patches
        with open(logPath, "a") as f:
            f.write(f"Applying player patches\n")
        for filename in ("malepc01.dbr","femalepc01.dbr"):
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename + "y")
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                if line.startswith(("devotionReclamationAetherCost,","devotionReclamationPointCosts,","reclamationPointCosts,")):
                    if slot_data.get("free_skill_respec",0) == 1:
                        line = simple_line_fix(line, "0;")
                # if line.startswith(("characterSpellCastSpeedModifier,",)):
                #     if slot_data.get("ultra_rapid_fire",0) == 1:
                #         line = simple_line_fix(line, "5;")
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)


        #Apply the enemy patches
        with open(logPath, "a") as f:
            f.write(f"Applying enemy patches\n")
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
            #If enemy rando is disabled or editing a summoned enemy, just pull info from the same file
            if (not targetName.endswith("summon.dbr")) and (slot_data.get("enemy_randomizer",0) == 1):
                path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage",slot_data["enemy_table"][index])
                with open(logPath, "a") as f:
                    f.write(f"Enemy Rando: Source -> Target: {slot_data["enemy_table"][index]} ->  + {targetName}\n")
            else:
                path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage",targetName)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
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
                #Preserve enemy factions to reduce infighting to vanilla amounts
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
                #Temporary fix to prevent case of deaths spawns summoning itself infinitely
                #TODO records/proxies/pools/
                if slot_data.get("enemy_randomizer",0) == 1:
                    if line.startswith(("poolToSpawnOnDeath,")):
                        line = ""
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
                    #Size and Action speed
                    if line.startswith(("scale,","characterAttackSpeed,","characterAttackSpeedModifier,","characterSpellCastSpeed,","characterSpellCastSpeedModifier,")): #,"characterRunSpeed,","characterRunSpeedModifier,","walkSpeed,")):
                        line = simple_line_scale(line, speedMultiplier)
                    #Level of skills, cause enemies to do more damage
                    if line.startswith(("skillLevel")):
                        words = line.split(",")
                        nums = words[1].split(";")
                        line = words[0] + ","
                        for i in nums:
                            line = line + i + "+(" + str(levelModifier) + ");"
                        line = line[:-1] + ",\n"
                #Give enemies increased cast speed and massive amounts of mana
                # if slot_data.get("ultra_rapid_fire",0) == 1:
                #     if line.startswith(("characterManaModifier,","characterMana,","characterManaRegen,","characterManaRegenModifier,")):
                #         line = simple_line_fix(line, "1000;")
                #     if line.startswith(("characterSpellCastSpeed,","characterSpellCastSpeedModifier,")):
                #         line = simple_line_scale(line, 2)
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

        with open(logPath, "a") as f:
            f.write(f"Building database files\n")
        subprocess.run([
            os.path.join(installPath,"arzedit.exe"),
            "build",
            os.path.join(installPath,"mods",patchedMod),
            os.path.join(installPath,"mods",patchedMod),
            "-g",
            installPath,
            ], shell=True)
        
    # Seven  Delete the extracted files, leaving behind only the compiled mod files: rmdir /s /q "..\Grim Dawn\mods\patchedMod\records"

        with open(logPath, "a") as f:
            f.write(f"Deleting temp files\n")
        subprocess.run([
            "rmdir",
            "/s",
            "/q",
            os.path.join(installPath,"mods",patchedMod,"records"),
            ], shell=True)
        
    # Eight  Copy arc files to new mod location: xcopy "..\Grim Dawn\mods\archipelago\resources" "..\Grim Dawn\mods\patchedArchipelago\resources" /i /y

        with open(logPath, "a") as f:
            f.write(f"Copying arc files\n")
        subprocess.run([
            "xcopy",
            os.path.join(installPath,"mods","archipelago","resources"),
            os.path.join(installPath,"mods",patchedMod,"resources"),
            "/i",
            "/y",
            ], shell=True)
        
    # Ninth  Create a txt file containing connection info: echo message > "C:\SteamSuperSSD\steamapps\common\Grim Dawn\mods\patchedArchipelago\a.txt"

        with open(logPath, "a") as f:
            f.write(f"Creating connect txt file\n")
        with open(os.path.join(installPath,"connect.txt"), "w") as file:
            file.write("host = " + server + "\nslot = " + slot_name + "\npassword = " + (password if password else "") + "\nssp = " + ("true" if slot_data.get("starting_skill_points",0) == 1 else "false"))
        with open(logPath, "a") as f:
            f.write(f"Patching finished\n")
        messagebox.showinfo("Grim Dawn Patcher", "Patching successful.")
    except ValueError as ex:
        with open(logPath, "a") as f:
            f.write(f"Patching failed due to ValueError. Reason: {ex}\n")
        messagebox.showerror("Grim Dawn Patcher", "Patching failed due to incorrect region. Go to Control Panel -> Change date, time, or number formats -> Format drop menu -> English (United States). Then try patching again. You can change the region back after patching is done.")
    except Exception as ex:
        with open(logPath, "a") as f:
            f.write(f"Patching failed. Reason: {ex}\n")
        messagebox.showerror("Grim Dawn Patcher", "Patching failed. Reason: " + str(ex) + "\nLog file saved at " + str(logPath))

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
            self.slot_data = args["slot_data"]

    def logEnemyTable(self):
        if "enemy_table" in (self.slot_data):
            if self.slot_data["enemy_table"]:
                installPath = GrimDawnWorld.settings.grimDawnInstallPath
                enemyLogPath = os.path.join(installPath,"mods","EnemyList.txt")
                with open(enemyLogPath, "w") as f:
                    for enemy in self.slot_data["enemy_table"]:
                        f.write(f"Enemy entry: {enemy}\n")
                logger.info("Enemy Table logged to " + enemyLogPath)
            else:
                logger.info("Enemies are not randomized in this slot.")
        else:
            logger.info("Enemy Table does not exist.")

    def logSkillTable(self):
        if "skill_balance_table" in (self.slot_data):
            if self.slot_data["skill_balance_table"]:
                installPath = GrimDawnWorld.settings.grimDawnInstallPath
                skillLogPath = os.path.join(installPath,"mods","SkillList.txt")
                with open(skillLogPath, "w") as f:
                    for className,playerClass in self.slot_data["skill_balance_table"].items():
                        for skillName,skill in playerClass.items():
                            for attributeName,value in skill.items():
                                f.write(f"Skill entry: {className} {skillName:30} {attributeName:55} {value}\n")
                logger.info("Skill Table logged to " + skillLogPath)
            else:
                logger.info("Skill balance is not randomized in this slot.")
        else:
            logger.info("Skill Balance Table does not exist.")

    def patchGame(self):
        if "dlc_aom" in (self.slot_data):
        # First  confirm the path to the grim dawn executable upon startup
            from Utils import async_start
            from worlds.LauncherComponents import launch_subprocess
            installPath = GrimDawnWorld.settings.grimDawnInstallPath
            logPath = os.path.join(installPath,"mods","PatcherLog.txt")
            with open(logPath, "w") as f:
                f.write(f"Grim Dawn install path is: {installPath} \n")
            hasGrimDawn = True
            hasMod = True
            hasArzedit = True
            hasHeinerLua = True
            hasGrimRealLua = False
            hasGrimBaseLua = True
            hasLuaClient = True
            dontContinue = False

        # Second confirm that the mod is a supported version for this apworld
            
            #isfile returns true if the file is found, join adds a slash (os specific) between the arguments
            if not os.path.isfile(os.path.join(installPath,"Grim Dawn.exe")):
                with open(logPath, "a") as f:
                    f.write("Grim Dawn.exe isfile returned false\n")
                logger.info("Did not find game executable. Make sure your path to the game install folder is correct.")
                logger.info(r"Example path: C:\Steam\steamapps\common\Grim Dawn\Grim Dawn.exe")
                logger.info(f"Current Grim Dawn install directory defined in host yaml: {installPath}")
                logger.info("If this path is incorrect, you can open your host.yaml found in your archipelago install folder and edit it.")
                hasGrimDawn = False
                dontContinue = True

            if hasGrimDawn == True:
                if not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","ver.txt")):
                    with open(logPath, "a") as f:
                        f.write("ver.txt isfile returned false\n")
                    hasMod = False
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
                        hasMod = False
                        dontContinue = True
                    with open(logPath, "a") as f:
                        f.write(f"Mod version detected {modVersion}, minimum apworld version supported {minimumSupportedVersion} \n")

        # Third  confirm that all the required files for archipelago grim dawn are installed correctly

                if not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","Archipelago.arz")):
                    hasMod = False
                    dontContinue = True
                
                if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Conversations.arc")):
                    hasMod = False
                    dontContinue = True
                
                if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Scripts.arc")):
                    hasMod = False
                    dontContinue = True

                if not os.path.isfile(os.path.join(installPath,"arzedit.exe")):
                    hasArzedit = False
                    dontContinue = True
                
                if not os.path.isfile(os.path.join(installPath,"lua51.dll")):
                    hasHeinerLua = False
                    hasGrimBaseLua = False
                    dontContinue = True
                else:
                    # Check the filesize to make sure it's the dll from Heinermann or the Grim Dawn base lua
                    sizeBytes = os.path.getsize(os.path.join(installPath,"lua51.dll"))
                    with open(logPath, "a") as f:
                        f.write(f"lua51.dll filesize: {sizeBytes}\n")
                    if (sizeBytes > 16000) and (sizeBytes < 20000):
                        # Is the Heinermann lua file
                        hasHeinerLua = True
                        hasGrimBaseLua = False
                    elif (sizeBytes > 330000) and (sizeBytes < 370000):
                        # Is the Grim Dawn lua file
                        hasHeinerLua = False
                        hasGrimBaseLua = True
                    else:
                        # Is something unknown
                        hasHeinerLua = False
                        hasGrimBaseLua = False
                    with open(logPath, "a") as f:
                        f.write(f"hasHeinerLua: {hasHeinerLua}\nhasGrimBaseLua: {hasGrimBaseLua}\n")
                
                if not os.path.isfile(os.path.join(installPath,"real_lua51.dll")):
                    hasGrimRealLua = False
                    dontContinue = True
                else:
                    # Check the filesize to make sure it's the dll from Grim Dawn base lua
                    sizeBytes = os.path.getsize(os.path.join(installPath,"real_lua51.dll"))
                    with open(logPath, "a") as f:
                        f.write(f"real_lua51.dll filesize: {sizeBytes}\n")
                    if (sizeBytes > 330000) and (sizeBytes < 370000):
                        # Is the Grim Dawn lua file
                        hasGrimRealLua = True
                    else:
                        hasGrimRealLua = False
                        if hasGrimBaseLua == False:
                            hasGrimDawn = False
                            logger.info("Grim Dawn lua51 dll is either missing or corrupted. Verify the file integrity of your Grim Dawn installation.")
                            with open(logPath, "a") as f:
                                f.write(f"Grim Dawn lua51 dll is either missing or corrupted. Verify the file integrity of your Grim Dawn installation.\nhasGrimRealLua: {hasGrimRealLua}\n")
                
                if not os.path.isfile(os.path.join(installPath,"lua-apclientpp.dll")):
                    hasLuaClient = False
                    dontContinue = True
                
                #Check if DLC files exist when DLC is enabled in slot data
                if (bool(self.slot_data["dlc_aom"])) and not os.path.isfile(os.path.join(installPath,"gdx1","database","GDX1.arz")):
                    logger.info("Missing Ashes of Malmouth DLC in your Grim Dawn install directory while enabled in this slot. Make sure you have ")
                    hasGrimDawn = False

                if (bool(self.slot_data["dlc_fg"])) and not os.path.isfile(os.path.join(installPath,"gdx2","database","GDX2.arz")):
                    logger.info("Missing Forgotten Gods DLC in your Grim Dawn install directory while enabled in this slot")
                    hasGrimDawn = False

                if (bool(self.slot_data["dlc_foa"])) and not os.path.isfile(os.path.join(installPath,"gdx3","database","GDX3.arz")):
                    logger.info("Missing Fangs of Asterkarn DLC in your Grim Dawn install directory while enabled in this slot")
                    hasGrimDawn = False

                if "ap_world_version" in (self.slot_data):
                    hostVersion = self.slot_data["ap_world_version"]
                    if hostVersion != apworldVersion:
                        # #Host version is different than client version
                        if not (hostVersion in supportedAPworldVersions):
                            logger.info("Apworld version mismatch. Host apworld version is different than yours. Features might be missing and compatability is not guaranteed.")
                            logger.info(f"Host apworld version: {hostVersion}")
                            logger.info(f"Your apworld version: {apworldVersion}")
                    else:
                        logger.info(f"Host and your apworld version match: {apworldVersion}")
                else:
                    #Doesn't exist yet, so must be older than 0.4.0
                    logger.info("Host apworld version older than 0.4.0 and is incompatible with your apworld")
                    dontContinue = True
                with open(logPath, "a") as f:
                    f.write(f"Host apworld version: {hostVersion}, Player apworld version: {apworldVersion} \n")
                
            with open(logPath, "a") as f:
                f.write(f"hasGrimDawn: {hasGrimDawn}\nhasMod: {hasMod}\nhasArzedit: {hasArzedit}\nhasHeinerLua: {hasHeinerLua}\nhasGrimRealLua: {hasGrimRealLua}\nhasGrimBaseLua: {hasGrimBaseLua}\nhasLuaClient: {hasLuaClient}\ndontContinue: {dontContinue}\n")
            if hasGrimDawn == False:
                logger.info("Patching aborted.")
            elif dontContinue == True:
                result = messagebox.askquestion("Grim Dawn Patcher", "Missing files required for Grim Dawn Archipelago. Would you like the patcher to download and install these files for you?")
                if result == 'yes':
                    with open(logPath, "a") as f:
                        f.write(f"User was missing files and responded with 'yes' to the message box.\n")
                    try:
                        # If base grim dawn lua51 is unchanged, rename it to real_lua
                        if hasGrimBaseLua:
                            with open(logPath, "a") as f:
                                f.write(f"Base grim dawn lua51 is unchanged, rename it to real_lua.\n")
                            # Make sure there is no real_lua first
                            if os.path.isfile(os.path.join(installPath,"real_lua51.dll")):
                                os.remove(os.path.join(installPath,"real_lua51.dll"))
                            os.rename(os.path.join(installPath,"lua51.dll"),os.path.join(installPath,"real_lua51.dll"))
                        # Attempt to download files
                        if hasHeinerLua == False:
                            url_HeinermannLua = "https://github.com/heinermann/GrimDawnLuaUnlocker/releases/download/1.0/lua51.dll"
                            filename, header = urllib.request.urlretrieve(url_HeinermannLua, filename=os.path.join(installPath,"lua51.dll"))
                            logger.info("Download response: " + str(filename))
                            with open(logPath, "a") as f:
                                f.write("Heinermann Lua Download response: " + str(filename) + str(header) + "\n")
                        if hasLuaClient == False:
                            url_BlackSliverLua = "https://github.com/routhken/Archipelago/releases/download/v0.4.0/lua-apclientpp.dll"
                            filename, header = urllib.request.urlretrieve(url_BlackSliverLua, filename=os.path.join(installPath,"lua-apclientpp.dll"))
                            logger.info("Download response: " + str(filename))
                            with open(logPath, "a") as f:
                                f.write("Black Sliver Lua Download response: " + str(filename) + str(header) + "\n")
                        if hasMod == False:
                            # Make sure there is no archipelago mod first
                            if os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Conversations.arc")):
                                shutil.rmtree(os.path.join(installPath,"mods","archipelago"))
                            url_GrimDawnMod = "https://github.com/routhken/Archipelago/releases/download/mod_3.0/archipelago.zip"
                            filename, header = urllib.request.urlretrieve(url_GrimDawnMod, filename=os.path.join(installPath,"mods","archipelago.zip"))
                            logger.info("Download response: " + str(filename))
                            with open(logPath, "a") as f:
                                f.write("Grim Dawn Mod Download response: " + str(filename) + str(header) + "\n")
                            with zipfile.ZipFile(os.path.join(installPath,"mods","archipelago.zip"), "r") as zip_ref:
                                zip_ref.extractall(os.path.join(installPath,"mods","archipelago"))
                        if hasArzedit == False:
                            url_Arzedit = "https://gitlab.com/QuasiMod/arzedit/uploads/b48b7ed4f74717d2a8cf6b67b4f9d842/arzedit.exe"
                            filename, header = urllib.request.urlretrieve(url_Arzedit, filename=os.path.join(installPath,"arzedit.exe"))
                            logger.info("Download response: " + str(filename))
                            with open(logPath, "a") as f:
                                f.write("Arzedit Download response: " + str(filename) + str(header) + "\n")
                    except Exception as ex:
                        with open(logPath, "a") as f:
                            f.write("Exception during download and install step: " + str(ex) + "\n")
                        messagebox.showerror("Grim Dawn Patcher", "File download and install failed. Reason: " + str(ex))
                        logger.info("Patching aborted.")
                    else:
                        logger.info("File download and install complete, run patch command again.")
                else:
                    if hasHeinerLua == False:
                        logger.info("Missing lua51.dll")
                    if hasLuaClient == False:
                        logger.info("Missing lua-apclientpp.dll")
                    if hasMod == False:
                        logger.info("Missing grim dawn archipelago mod")
                    if hasArzedit == False:
                        logger.info("Missing arzedit.exe")
                    logger.info("Patching aborted.")
            else:
                logger.info("Grim Dawn Archipelago installation found.")
                logger.info("Patching game. Please wait for a confirmation message to appear before starting a save file. This usually takes around 30 seconds.")
                launch_subprocess(patch_game, "patchgame", (self.username, self.server_address, self.password, installPath, self.slot_data,))
                #self.patch_game(self.username, self.server_address, self.password, args["slot_data"])
                #await self.update_death_link(args["slot_data"]["deathlink"])
                async_start(self.update_death_link(bool(self.slot_data["deathlink"])))
        else:
            logger.info("Client must connect to a slot first.")

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