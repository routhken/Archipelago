import asyncio
from .EnemyRandomizer import enemyListNonBoss, enemyDangerous
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    get_base_parser,
    server_loop,
    ClientCommandProcessor
)
import subprocess
import os
import shutil
import urllib.parse
from NetUtils import ClientStatus


DEBUG = False
GAMENAME = "Grim Dawn"
ITEMS_HANDLING = 0b000

class GrimDawnCommandProcessor(ClientCommandProcessor):
    def _cmd_debug_patch(self):
        self.ctx.patch_game({})

    def _cmd_list_enemies(self):
        for enemy in self.ctx.slot_data["enemy_table"]:
            logger.info(f"Enemy entry: {enemy}")

    def _cmd_list_skills(self):
        for skill in self.ctx.slot_data["skill_balance_table"]:
            logger.info(f"Enemy entry: {skill}")

    #def _cmd_goal_game(self):
    #    self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


def patch_game(username, server_address, password, installPath, slot_data: dict[str, any]):
    
# Forth  Run the command from the grim dawn folder: arzedit.exe extract "..\Grim Dawn\mods\archipelago\database\Archipelago.arz" "..\Grim Dawn\mods\patchedMod"
    #This initiates the command line, join adds a slash (os specific) between the arguments
    #logger.info("Deleting existing patchedMod files so a new one can build.")
    patchedMod = "patchedArchipelago"
    subprocess.run([
        "rmdir",
        "/s",
        "/q",
        os.path.join(installPath,"mods",patchedMod),
        ], shell=True)
    #logger.info("Extracting database files.")
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

    #logger.info("Applying skill patch.")
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

                            #Certain attributes that can have negative modifiers do not function below -100%.
                            if attributename in ("skillManaCostReduction"):
                                patchedValue = max(patchedValue,-100)

                            #Certain attributes break when over 100%
                            if attributename in ("conversionPercentage","skillManaCostReduction","onHitActivationChance","skillChanceWeight","sparkChance","offensiveTauntMin","offensiveSleepChance",
                                                    "lifeMonitorPercent","offensiveTotalDamageReductionPercentMin","offensiveDisruptionChance","offensiveSlowPhysicalChance","offensiveSlowBleedingChance"
                                                    "skillCooldownReduction","conversionPercentage2","defensiveDisruption","retaliationStunChance","projectilePiercing","projectilePiercingChance",
                                                    "offensiveStunChance","offensiveFearChance","skillCooldownReductionChance","offensiveConfusionChance","offensiveKnockdownChance","offensiveFreezeChance",
                                                    "offensiveLightningChance","offensiveFumbleMin","offensiveProjectileFumbleMin","offensiveGlobalChance","retaliationSlowManaLeachChance",
                                                    "offensiveSlowLightningChance","offensiveSlowColdChance","offensiveLightningModifierChance","offensiveSlowFireChance","offensiveTrapChance"):
                                patchedValue = min(patchedValue,100)

                            #Certain attributes break game balance at 100% or more
                            if attributename in ("damageAbsorptionPercent","characterDeflectProjectile","offensivePercentCurrentLifeMin","offensivePercentCurrentLifeMax"):
                                patchedValue = min(patchedValue,85)

                            #To ensure skill usability, these attributes cannot be below 1
                            if attributename in ("skillTargetNumber","skillProjectileNumber","projectileLaunchNumber","petLimit","petBurstSpawn","sparkMaxNumber","skillChargeLevel",
                                                    "contagionMaxSpread","contagionLimit","tetherLimit","linkLimit","numProjectiles"):
                                patchedValue = max(patchedValue,1)

                            line = line + str(patchedValue) + ";"
                        line = line[:-1] + ",\n"
                        break
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)
    
    #Apply the free respec patch, if enabled
    #logger.info("Applying skill respec patch.")
    if slot_data.get("free_skill_respec",0) == 1:
        for filename in ("malepc01.dbr","femalepc01.dbr"):
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename)
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","pc",filename + "s")
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
                if line.startswith(("devotionReclamationAetherCost,","devotionReclamationPointCosts,","reclamationPointCosts,")):
                    words = line.split(",")
                    nums = words[1].split(";")
                    line = words[0] + ","
                    for i in nums:
                        line = line + "0;"
                    line = line[:-1] + ",\n"
                f2.write(line)
            f1.close()
            f2.close()
            os.replace(path2,path1)

    #Apply the enemy rando patch, if enabled
    #logger.info("Applying enemy rando patch.")
    if slot_data.get("enemy_randomizer",0) == 1:
        #TODO Prevent certain slith enemies from being randomized for slith charm quest.
        #First make a copy of every enemy so we can read from them without overwriting them.
        tempStoragePath = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage")
        os.makedirs(tempStoragePath)
        for sourceName in enemyListNonBoss:
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",sourceName)
            shutil.copy(path1,tempStoragePath)
        #slot_data["enemy_table"]
        #logger.info("singletonEnemy: " + singletonEnemy[0] + singletonEnemy[1] + singletonEnemy[2] + singletonEnemy[3])
        #logger.info("path1: " + path1)
        startingIndex = 0
        dangerIndex = len(slot_data["enemy_table"]) #(len(enemyDangerous))
        index = startingIndex
        #shouldLog = True
        #logger.info(f"Length of dangerous enemies list: {dangerIndex}")
        for targetName in enemyListNonBoss:
            path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","tempStorage",slot_data["enemy_table"][index])
            path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
            f1 = open(path1, 'r')
            f2 = open(path2, 'w')
            for line in f1:
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

    #logger.info("Building database files.")
    subprocess.run([
        os.path.join(installPath,"arzedit.exe"),
        "build",
        os.path.join(installPath,"mods",patchedMod),
        os.path.join(installPath,"mods",patchedMod),
        "-g",
        installPath,
        ], shell=True)
    
# Seven  Delete the extracted files, leaving behind only the compiled mod files: rmdir /s /q "..\Grim Dawn\mods\patchedMod\records"

    #logger.info("Deleting temp files.")
    subprocess.run([
        "rmdir",
        "/s",
        "/q",
        os.path.join(installPath,"mods",patchedMod,"records"),
        ], shell=True)
    
# Eight  Copy arc files to new mod location: xcopy "..\Grim Dawn\mods\archipelago\resources" "..\Grim Dawn\mods\patchedArchipelago\resources" /i /y

    #logger.info("Copying arc files.")
    subprocess.run([
        "xcopy",
        os.path.join(installPath,"mods","archipelago","resources"),
        os.path.join(installPath,"mods",patchedMod,"resources"),
        "/i",
        "/y",
        ], shell=True)
    
# Ninth  Create a txt file containing connection info: echo message > "C:\SteamSuperSSD\steamapps\common\Grim Dawn\mods\patchedArchipelago\a.txt"

    #logger.info("Creating connect txt file.")
    with open(os.path.join(installPath,"connect.txt"), "w") as file:
        file.write("host = " + server + "\nslot = " + slot_name + "\npassword = " + (password if password else "") + "\nssp = " + ("true" if slot_data.get("starting_skill_points",0) == 1 else "false"))
    logger.info("Patching finished.")

class ProxyGameContext(CommonContext):
    game = GAMENAME
    items_handling = ITEMS_HANDLING
    command_processor = GrimDawnCommandProcessor

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.slot_data = {"enemy_table": [], "skill_balance_table": []}

        
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

        # Second confirm that arzedit is in the grim dawn root folder

            #isfile returns true if the file is found, join adds a slash (os specific) between the arguments
            if not os.path.isfile(os.path.join(installPath,"arzedit.exe")):
                logger.info("arzedit is not in your Grim Dawn install directory.")
                logger.info(f"Current Grim Dawn install directory: {installPath}")

        # Third  confirm that the archipelago mod for grim dawn is installed correctly

            elif not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","Archipelago.arz")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\database\Archipelago.arz")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
            
            elif not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Conversations.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Conversations.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
            
            elif not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Quests.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Quests.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
            
            elif not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Scripts.arc")):
                logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
                logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Scripts.arc")
                logger.info(f"Current Grim Dawn install directory: {installPath}")
            
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
    args = parser.parse_args(args)

    colorama.init()
    print(args) #TODO DEBUG
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    launch()