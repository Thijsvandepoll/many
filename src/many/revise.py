import datetime
import glob
import os
import runpy
from typing import Union

from mako.template import Template

from many.templates import base_template
from many.utils import create_hash


class Revisions:
    def __init__(
        self,
        script_location: str,
        file_template: str = "%(year)d_%(month).2d_%(day).2d_%(hour).2d%(minute).2d-%(rev)s_%(slug)s",
        truncate_slug_length: int = 40,
        template: Template = base_template,
    ):
        self.script_location = script_location
        self.file_template = file_template
        self.truncate_slug_length = truncate_slug_length
        self.template = template

    @property
    def revisions(self):
        revisions = []
        for file_path in glob.glob(self.script_location.rstrip("/") + "/*.py"):
            module = runpy.run_path(file_path)
            revisions.append(module)
        return revisions

    @property
    def up_by_current(self):
        return {k["down_version"]: k for k in self.revisions}

    @property
    def down_by_current(self):
        return {k["version"]: k for k in self.revisions}

    def has_upgrade(self, current_state: Union[str, int]):
        return current_state in self.up_by_current.keys()

    def get_upgrade(self, current_state: Union[str, int]):
        template = self.up_by_current[current_state]
        return template["up"], template["version"]

    def has_downgrade(self, current_state: Union[str, int]):
        return current_state in self.down_by_current.keys()

    def get_downgrade(self, current_state: Union[str, int]):
        template = self.down_by_current[current_state]
        return template["down"], template["down_version"]

    def get_head(self):
        for template in self.revisions[::-1]:
            version = template["version"]
            if not self.has_upgrade(version):
                return version

    def create_revision(self, m: str):
        latest = self.get_head()
        version = create_hash(m)

        content = self.template.render(version=version, down_version=latest)

        now = datetime.datetime.now()
        if not os.path.exists(self.script_location):
            os.mkdir(self.script_location)

        file_name = self.file_template % {
            "slug": m.lower().replace(" ", "_")[: self.truncate_slug_length],
            "year": now.year,
            "month": now.month,
            "day": now.day,
            "hour": now.hour,
            "minute": now.minute,
            "rev": version,
        }
        file_name = f"{self.script_location}/{file_name}.py"
        with open(file_name, "w") as file:
            file.write(content)
        print(
            f"Created new migration template with version {version} and at path"
            f" {file_name}"
        )
