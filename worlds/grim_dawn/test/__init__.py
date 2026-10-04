from test.bases import WorldTestBase
# from argparse import Namespace
# from test.general import gen_steps
# from worlds.AutoWorld import call_all
# from worlds import AutoWorld
import typing
from BaseClasses import CollectionState, MultiWorld  # , Item
from .. import GrimDawnWorld
from worlds import AutoWorld
from worlds.AutoWorld import call_all
import random
import unittest
from argparse import Namespace
from test.general import gen_steps
from Generate import get_seed_name
from Options import OptionError

class GrimDawnTestBase(WorldTestBase):
    game = "Grim Dawn"
    world: GrimDawnWorld

    def assertAccessIndependency(
            self,
            locations: typing.List[str],
            possible_items: typing.Iterable[typing.Iterable[str]],
            only_check_listed: bool = False) -> None:
        """Asserts that the provided locations can't be reached without
        the listed items but can be reached with any
        one of the provided combinations"""
        all_items = [
            item_name for
            item_names in
            possible_items for
            item_name in
            item_names
            ]

        state = CollectionState(self.multiworld)

        for item_names in possible_items:
            items = self.get_items_by_name(item_names)
            for item in items:
                self.collect_all_but(item)
            for location in locations:
                self.assertTrue(state.can_reach(location, "Location", 1),
                                f"{location} not reachable with {item_names}")
            for item in items:
                state.remove(item)

    def assertAccessWithout(
            self,
            locations: typing.List[str],
            possible_items: typing.Iterable[typing.Iterable[str]]) -> None:
        """Asserts that the provided locations can't be reached without the
        listed items but can be reached with any
        one of the provided combinations"""
        all_items = [
            item_name for
            item_names in
            possible_items for
            item_name in
            item_names
            ]

        state = CollectionState(self.multiworld)
        self.collect_all_but(all_items, state)
        for location in locations:
            self.assertTrue(
                state.can_reach(location, "Location", 1),
                f"{location} is not reachable without {all_items}")

class grimDawnOptionErrorTestBase():
    game = "Grim Dawn"
    world: GrimDawnWorld
    player = 1
    options = {}
    def test_world_setup(self):
        with self.assertRaises(OptionError):
            if type(self) is WorldTestBase or \
                    (hasattr(WorldTestBase, self._testMethodName)
                    and not self.run_default_tests and
                    getattr(self, self._testMethodName).__code__ is
                    getattr(WorldTestBase, self._testMethodName, None).__code__):
                return  # setUp gets called for tests defined in the base class. We skip world_setup here.
            if not hasattr(self, "game"):
                raise NotImplementedError("didn't define game name")
            self.multiworld = MultiWorld(1)
            self.multiworld.game[self.player] = self.game
            self.multiworld.player_name = {self.player: "Tester"}
            self.multiworld.set_seed(None)
            random.seed(self.multiworld.seed)
            self.multiworld.seed_name = get_seed_name(random)  # only called to get same RNG progression as Generate.py
            args = Namespace()
            for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
                setattr(args, name, {
                    1: option.from_any(self.options.get(name, option.default))
                })
            self.multiworld.set_options(args)
            self.multiworld.state = CollectionState(self.multiworld)
            self.world = self.multiworld.worlds[self.player]
            for step in gen_steps:
                call_all(self.multiworld, step)

class selectSeedGrimDawn(WorldTestBase):
    game = "Grim Dawn"
    seed = 0
    world: GrimDawnWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)
