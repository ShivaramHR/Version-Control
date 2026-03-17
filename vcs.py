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
    fileName = sys.argv[2]
    docPath = path / fileName

    #checks if file exists
    if not docPath.exists():
        print(f"File {fileName} does not exist")
        return
    content = docPath.read_bytes()

    #calls hash_file() to get hash value of the file
    hashValue = hash_file(content)

    #checks if the file is already hashed
    hashedPath = path / ".vcs" / "objects" / hashValue
    if not hashedPath.exists():
        hashedPath.write_bytes(content)

    #reads index.json
    json_file = path / ".vcs" / "index.json"

    #checks if index.json is valid JSON
    json_content = json_file.read_text()

    #if not valid JSON, initialize empty dict
    try:
        #parses the JSON content
        json_data = json.loads(json_content)
    except json.JSONDecodeError:
        json_data = {}
    
    #adds file to index
    json_data[fileName] = hashValue
    json_file.write_text(json.dumps(json_data, indent=2, sort_keys=True))
    
    #prints succes message
    print(f"File {fileName} added to index")

def commit(path):
    head_file = path / ".vcs" / "HEAD"
    commit_id = head_file.read_text()

    if commit_id == "None":
        commit_id = "c1"
        parent = "None"
        head_file.write_text(commit_id)
    elif "c" in commit_id:
        parent = commit_id
        commit_id = "c" + str(int(head_content[1:]) + 1)
    json_file = path / ".vcs" / "index.json"
    json_content = json_file.read_bytes()
    commit_hash = hash_file(json_content)
    hashedPath = path / ".vcs" / "commits" / commit_id
    hashedPath.write_bytes(json_content)

commands = {
    "init": init,
    "add": add,
    "commit": commit
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