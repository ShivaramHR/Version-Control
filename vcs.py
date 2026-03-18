import sys
import json
import os
from pathlib import Path
import hashlib
from datetime import datetime, timezone

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

def commit(path, message):
    timestamp = datetime.now(timezone.utc).isoformat()
    head_file = path / ".vcs" / "HEAD"
    commit_id = head_file.read_text()

    if commit_id == "None":
        new_commit_id = "c1"
        parent = "None"
    else:
        parent = commit_id
        new_commit_id = "c" + str(int(commit_id[1:]) + 1)  
    json_file = path / ".vcs" / "index.json"

    with open(json_file, 'r') as f:
        json_data = json.load(f)
    if not json_data:
        print("No files to commit")
        return
    commitFiles = json_data.copy()
    commitPath = path / ".vcs" / "commits" / f"{new_commit_id}.json"

    commitData = {
        'id': new_commit_id,
        'parent': parent,
        'message': message,
        'timestamp': timestamp,
        'files': commitFiles
    }

    commitPath.write_text(json.dumps(commitData, indent=2))
    json_file.write_text('{}')
    head_file.write_text(new_commit_id)
    print(f"Commit {new_commit_id} created successfully")

def log(path):
    headFile = path / ".vcs" / "HEAD"
    commit_id = headFile.read_text()
    while commit_id != 'None':
        commitFile = path / '.vcs' / 'commits' / f'{commit_id}.json'
        commitData = json.loads(commitFile.read_text())
        print(f"Commit ID: {commitData['id']}")
        print(f"Message: {commitData['message']}")
        print(f"Timestamp: {commitData['timestamp']}")
        print()
        commit_id = commitData['parent']


def status(path):
    headFile = path / ".vcs" / "HEAD"
    commit_id = headFile.read_text()
    commitData = {}
    if commit_id != 'None':
        commitFile = path / '.vcs' / 'commits' / f'{commit_id}.json'
        commitData = json.loads(commitFile.read_text())
    
    indexFile = path / '.vcs' / 'index.json'
    indexData = json.loads(indexFile.read_text())

    workingFiles = [f for f in path.iterdir() if f.is_file() and f.name != '.vcs']

    for file in workingFiles:
        name = file.name
        contents = file.read_bytes()
        current_hash = hash_file(contents)

        if name not in indexData:
            print(f"Untracked file: {name}")
        elif indexData[name] != current_hash:
            print(f"Modified file: {name}")
        elif name not in commitData.get('files', {}) and indexData[name] != commitData['files'][name]:
            print(f"Staged file: {name}")

        for name in commitData.get('files', {}):
            if not (path / name).exists():
                print(f"Deleted file: {name}")

def checkout(path, commit_id):
    commitFile = path / '.vcs' / 'commits' / f'{commit_id}.json'
    commitData = json.loads(commitFile.read_text())
    for name, hash in commitData['files'].items():
        file = path / name
        content = file.read_bytes()
        file.write_bytes(content)

                
commands = {
    "init": init,
    "add": add,
    "commit": commit,
    "log": log,
    'status': status,
    'checkout': checkout
}


def execute():
    if len(sys.argv) < 2:
        print("Usage: vcs <command>")
        return

    command = sys.argv[1]
    path = Path.cwd()

    if command in commands:
        commands[command](path, sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    execute()