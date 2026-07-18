import typing
from dataclasses import dataclass
from pathlib import Path

from CommonClient import logger


@dataclass
class RequiredFileList:
    files: list[str]
    message: str = ""
    condition: typing.Callable[[dict], bool] = lambda slot_data: True


all_required_files = [
    RequiredFileList(["arzedit.exe", "lua51.dll", "real_lua51.dll", "lua-apclientpp.dll"]),
    RequiredFileList(
        files=[
            "mods/archipelago/database/Archipelago.arz",
            "mods/archipelago/resources/Conversations.arc",
            "mods/archipelago/resources/Quests.arc",
            "mods/archipelago/resources/Scripts.arc",
        ],
        message="Archipelago mod for Grim Dawn is not correctly installed. Missing mod files.",
    ),
    RequiredFileList(
        files=["gdx1/database/GDX1.arz"],
        message="Missing Ashes of Malmouth DLC in your Grim Dawn install directory while enabled in this slot",
        condition=lambda slot_data: bool(slot_data["dlc_aom"]),
    ),
    RequiredFileList(
        files=["gdx2/database/GDX2.arz"],
        message="Missing Forgotten Gods DLC in your Grim Dawn install directory while enabled in this slot",
        condition=lambda slot_data: bool(slot_data["dlc_fg"]),
    ),
]


def verify_required_files(install_dir: str, slot_data: dict) -> bool:
    """
    Verifies that all required files are present in the game install directory,
    returning `True` if everything is fine. If any required file is missing,
    this function will return `False` and print details to the client log.
    """

    install_path = Path(install_dir).resolve()

    # Only verify files required by the provided slot data
    required_files = (file_list for file_list in all_required_files if file_list.condition(slot_data))
    any_missing = False

    for file_list in required_files:
        for file in file_list.files:
            target = install_path.joinpath(file)
            if not target.is_file():
                any_missing = True
                logger.info(file_list.message or f"Missing {target.name} in your Grim Dawn install directory")
                logger.info(f"Expected path: {target}")

    if any_missing:
        logger.info(f"Current Grim Dawn install directory: {install_path}")

    return not any_missing
