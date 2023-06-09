import math
from typing import Union

from many.engine import MigrationEngine
from many.revise import Revisions


class Migrator:
    def __init__(self, engine: MigrationEngine, revisions: Revisions):
        self.engine = engine
        self.revisions = revisions

    def init(self):
        if self.engine.remote_exists():
            print("Remote state already exists.")
            return
        self.engine.init_remote()
        print("Remote state initialized")

    def one_up_from(self, state: Union[str, int]):
        if not self.revisions.has_upgrade(state):
            print("Migrations complete. No upgrades to run.")
            return
        method, target_state = self.revisions.get_upgrade(state)

        # Run upgrade with arguments
        method(*self.engine.prepare_args())

        # Update remote state
        self.engine.update_remote(target_state)
        print(f"Migrated successfully (up) from {state} to {target_state}.")
        return target_state

    def one_down_from(self, state: Union[str, int]):
        if not self.revisions.has_downgrade(state):
            print("Migrations complete. No downgrades to run.")
            return

        method, target_state = self.revisions.get_downgrade(state)

        # Run downgrade with arguments
        method(*self.engine.prepare_args())

        # Update remote state
        self.engine.update_remote(target_state)
        print(f"Migrated successfully (down) from {state} to {target_state}.")
        return target_state

    def get_current_state(self):
        if not self.engine.remote_exists():
            raise ValueError("Remote state is not initialized.")
        return self.engine.get_remote()

    def up(self, level: str = "head"):
        if isinstance(level, str) and level.lower() != "head" and not level.isdigit():
            raise ValueError("level must be either 'head', or an integer")
        elif not level.isdigit():
            level = math.inf
        else:
            level = int(level)

        current_state = self.get_current_state()
        i = 0
        while i < level:
            new_state = self.one_up_from(current_state)
            if new_state is None:
                break
            current_state = new_state
            i += 1

    def down(self, level: Union[int, str] = "base"):
        if isinstance(level, str) and level.lower() != "base" and not level.isdigit():
            raise ValueError("level must be either 'base', or an integer")
        elif not level.isdigit():
            level = math.inf
        else:
            level = int(level)

        current_state = self.get_current_state()
        i = 0
        while i < level:
            new_state = self.one_down_from(current_state)
            if new_state is None:
                break
            current_state = new_state
            i += 1
