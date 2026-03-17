import sys
import json
import os
from pathlib import Path
import hashlib

# To initialise .vcs directory
def init(path):
    vcs_dir = path / ".vcs"
    vcs_dir.mkdir(exist_ok=True)

    (vcs_dir / "objects").mkdir(exist_ok=True)
    (vcs_dir / "commits").mkdir(exist_ok=True)

    # initialize index.json with empty dict
    index_file = vcs_dir / "index.json"
    if not index_file.exists():
        index_file.write_text("{}")

    # initialize HEAD
    head_file = vcs_dir / "HEAD"
    if not head_file.exists():
        head_file.write_text("None")

    print("VCS initialized successfully")

#To hash the file
def hash_file(content):
    h = hashlib.sha256(content)
    return h.hexdigest()

#To stage or add files
def add(path):
    doc = sys.argv[2]
    docPath = path / doc
    with open(docPath, "r") as f:
        content = Path(docPath).read_bytes()
    hashValue = hash_file(content)
    hashedPath = path / ".vcs" / "objects" / hashValue
    hashedPath.write_bytes(content)

commands = {
    "init": init,
    "add": add
}


def execute():
    if len(sys.argv) < 2:
        print("Usage: vcs <command>")
        return

    command = sys.argv[1]
    path = Path.cwd()

    if command in commands:
        commands[command](path)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    execute()