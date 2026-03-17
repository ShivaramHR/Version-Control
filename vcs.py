import os
import sys
import hashlib
from pathlib import Path


def init(path):
    init_dir = path / ".vcs"
    init_dir.mkdir(exist_ok=True)
    objects_dir = init_dir / 'objects'
    objects_dir.mkdir(exist_ok=True)
    commands_dir = init_dir / 'commands'
    commands_dir.mkdir(exist_ok=True)
    index_file = init_dir / 'index.json'
    index_file.touch()
    HEAD_file = init_dir / 'HEAD'
    HEAD_file.touch()
    print("VCS initialized successfully")

if __name__ == "__main__":
    commands = {
        "init" : init
    }
    def execute():
        path = Path.cwd()
        command = sys.argv[1]
        for key, value in commands.items():
            if key == command:
                value(path)
    
    execute()