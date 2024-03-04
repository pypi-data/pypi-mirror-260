"""
Specific file dataclass to for music specific functions and properties 
"""
from dataclasses import dataclass
from ._file import File as f


@dataclass
class MusicFile(f):

    tags: dict
    artwork: list

    def missing_tag(self) -> bool:
        if len(self.tags) == 0:
            return True
        return len({k: v for k, v in self.tags.items() if v is ''}) == 0

    def report_missing_tags(self) -> str:
        empty_tags = '\n'.join(
            [f'Missing tag {k}' for k, v in self.tags.items() if v is ''])
        return empty_tags
