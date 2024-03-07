# Grim Dawn Start Guide

Install Grim Dawn from steam.
In the Grim Dawn install directory, rename the file "lua51.dll" to "real_lua51.dll"
Download the lua51.dll file from Heinermann (download is in the pins) and place it in the install directory.
Download the lua51.7z under "lua-apclientpp v0.2.6-8" from Black Sliver's github https://github.com/black-sliver/lua-apclientpp/releases
Extract "lua51\lua51-clang32-dynamic" from the zip. Place only the "lua-apclientpp.dll" file in the Grim Dawn install directory
Download my mod from Nexus Mods https://www.nexusmods.com/grimdawn/mods/167/
Create a folder named "mods" in the Grim Dawn install directory if it doesn't already exist. Place the mod.zip inside and extract here.
Create a txt file named "apserverinfo.txt" in the Grim Dawn install directory. Open the text file and copy the following into it:
host = archipelago.gg:38281
slot = PlayerName
password = 

Edit the port and slot name in the txt to match that of the multiworld you are connecting to.
Download the grim_dawn.apworld made by Faris (download is in the pins), and place it in your Archipelago apworld directory "...\Archipelago\lib\worlds"
Launch the game. At the main menu, select the Custom Game tab -> Custom Game bubble -> "archipelago ~ world001.map"
Create a new character and start. Talk to Jarvis the hangman to connect to the multiworld.
