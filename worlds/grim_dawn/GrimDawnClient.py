import asyncio
from .EnemyRandomizer import enemyListNonBoss
from .EnemyRandomizer import enemyListLoads
from .EnemyRandomizer import enemyListDebug
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    get_base_parser,
    server_loop,
    ClientCommandProcessor
)
import Utils
import settings
import subprocess
import os
import urllib.parse


DEBUG = False
GAMENAME = "Grim Dawn"
ITEMS_HANDLING = 0b000

class GrimDawnCommandProcessor(ClientCommandProcessor):
    def _cmd_debug(self):
        self.ctx.patch_game({})


class ProxyGameContext(CommonContext):
    game = GAMENAME
    items_handling = ITEMS_HANDLING
    command_processor = GrimDawnCommandProcessor

    def patch_game(self, slot_data: dict[str, any]):
    # First  confirm the path to the grim dawn executable upon startup
    #TODO This also triggers when a disconnect -> reconnect occurs
        from . import GrimDawnWorld
        installPath = GrimDawnWorld.settings.grimDawnInstallPath
        print(f"Grim Dawn install path is: {installPath}")

    # Second confirm that arzedit is in the grim dawn root folder

        #isfile returns true if the file is found, join adds a slash (os specific) between the arguments
        if not os.path.isfile(os.path.join(installPath,"arzedit.exe")):
            logger.info("arzedit is not in your Grim Dawn install directory.")
            logger.info(f"Current Grim Dawn install directory: {installPath}")
            return

    # Third  confirm that the archipelago mod for grim dawn is installed correctly

        if not os.path.isfile(os.path.join(installPath,"mods","archipelago","database","Archipelago.arz")):
            logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
            logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\database\Archipelago.arz")
            logger.info(f"Current Grim Dawn install directory: {installPath}")
            return
        
        if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Conversations.arc")):
            logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
            logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Conversations.arc")
            logger.info(f"Current Grim Dawn install directory: {installPath}")
            return
        
        if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Quests.arc")):
            logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
            logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Quests.arc")
            logger.info(f"Current Grim Dawn install directory: {installPath}")
            return
        
        if not os.path.isfile(os.path.join(installPath,"mods","archipelago","resources","Scripts.arc")):
            logger.info("Archipelago mod for Grim Dawn is not correctly installed.")
            logger.info(r"Expected path: ...\Grim Dawn\mods\archipelago\resources\Scripts.arc")
            logger.info(f"Current Grim Dawn install directory: {installPath}")
            return
        
        logger.info("Grim Dawn Archipelago installation found.")
        
    # Forth  Run the command from the grim dawn folder: arzedit.exe extract "..\Grim Dawn\mods\archipelago\database\Archipelago.arz" "..\Grim Dawn\mods\patchedMod"

        patchedMod = "patchedArchipelago"
        logger.info("Patching game. This may take a while.")

        #This initiates the command line, join adds a slash (os specific) between the arguments
        #logger.info("Deleting existing patchedMod files so a new one can build.")
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

        if not self.username:
            slot_name = "Player1"
        else:
            slot_name = self.username
        #Remove @slotname from the url so it can connect to servers, otherwise an "unrecoverable" socket error could occur
        if not self.server_address:
            server = "ws://localhost:38281"
        else:
            x = urllib.parse.urlsplit(self.server_address)
            server = urllib.parse.urlunsplit(x._replace(netloc=x.netloc.rsplit("@", 1)[-1]))
        password = self.password
        
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

                                #Certain attributes break the game at 100% or more
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

            #First rename the existing enemy names so that there won't be any name conflicts
            for sourceName in slot_data["enemy_table"]:
                path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",sourceName)
                path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","_" + sourceName)
                os.rename(path1,path2)

            #Iterates through each file at the same time, renaming the enemy files
            for sourceName, targetName in zip(enemyListNonBoss,slot_data["enemy_table"]):
                path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies","_" + sourceName)
                path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
                os.rename(path1,path2)

            #TODO Prevent certain slith enemies from being randomized for slith charm quest.

            #DEBUG overwrite every enemy with the contents of a single enemy, so that every enemy is the same
            #TODO make this debug thing a feature
            # singletonEnemy = enemyListDebug
            # logger.info("singletonEnemy: " + singletonEnemy[0] + singletonEnemy[1] + singletonEnemy[2] + singletonEnemy[3])
            # #logger.info("path1: " + path1)
            # index = 0
            # for targetName in enemyListNonBoss:
            #     if targetName != singletonEnemy:
            #         path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",singletonEnemy[index])
            #         path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
            #         f1 = open(path1, 'r')
            #         f2 = open(path2, 'w')
            #         for line in f1:
            #             f2.write(line)
            #         f1.close()
            #         f2.close()
            #     if index < 3:
            #         index += 1
            #     else:
            #         index = 0
            # for targetName in enemyListLoads:
            #     if targetName != singletonEnemy:
            #         path1 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",singletonEnemy[index])
            #         path2 = os.path.join(installPath,"mods",patchedMod,"records","creatures","enemies",targetName)
            #         f1 = open(path1, 'r')
            #         f2 = open(path2, 'w')
            #         for line in f1:
            #             f2.write(line)
            #         f1.close()
            #         f2.close()
            #     if index < 3:
            #         index += 1
            #     else:
            #         index = 0

                
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
        
    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == 'Connected':
            self.patch_game(args["slot_data"])

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