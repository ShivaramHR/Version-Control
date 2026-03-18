# 🧩 Mini Version Control System (VCS)

A simplified version control system built in Python to understand how tools like Git work internally.

---

## 🚀 Overview

This project implements the core concepts of a version control system from scratch:

- Content-based file tracking using hashing  
- Staging area (index)  
- Commit history with parent linking  
- Status tracking (working vs staged vs committed)  
- Checkout to restore previous versions  

The goal is **learning by building**, not replicating Git fully.

---

## 🧠 How It Works (Core Concepts)

### 1️⃣ Objects (Storage)
- File contents are stored in `.vcs/objects/`
- Each file is saved using its **SHA-256 hash**
- Same content → stored only once (deduplication)

---

### 2️⃣ Index (Staging Area)
- Stored in `.vcs/index.json`
- Maps:

```json
{
  "file.py": "hash_value"
}
```

- Represents files staged for commit

---

### 3️⃣ Commits
- Stored in `.vcs/commits/`
- Each commit is a snapshot:

```json
{
  "id": "c2",
  "parent": "c1",
  "message": "updated file",
  "timestamp": "...",
  "files": {
    "app.py": "hash123"
  }
}
```

---

### 4️⃣ HEAD
- Stored in `.vcs/HEAD`
- Points to the latest commit:

```
c2
```

---

### 5️⃣ Status System

Compares three layers:

```
Working Directory ↔ Index ↔ HEAD
```

Tracks:
- Untracked files
- Modified files
- Staged files
- Deleted files

---

## ⚙️ Features

- `init` → Initialize repository  
- `add` → Stage files  
- `commit` → Save snapshot  
- `log` → View commit history  
- `status` → See changes  
- `checkout` → Restore previous commit  

---

## 📦 Project Structure

```
.vcs/
├── objects/      # file contents (hashed)
├── commits/      # commit snapshots
├── index.json    # staging area
└── HEAD          # current commit pointer
```

---

## 🛠️ Installation & Setup

### Option 1: Run with Python

```
python3 vcs.py <command>
```

---

### Option 2: Use as CLI Command (Recommended)

#### Step 1: Add alias in `.zshrc`

```
nano ~/.zshrc
```

Add:

```
alias vcs="python3 '/FULL/PATH/TO/vcs.py'"
```

Example:

```
alias vcs="python3 '/Volumes/Crucial X9/Learnings/Version-Control/vcs.py'"
```

---

#### Step 2: Reload terminal config

```
source ~/.zshrc
```

---

#### Step 3: Use globally

```
vcs init
vcs add file.py
vcs commit "message"
```

---

## 📌 Usage

### Initialize repo

```
vcs init
```

---

### Add files

```
vcs add file.py
```

---

### Commit changes

```
vcs commit "initial commit"
```

---

### View history

```
vcs log
```

---

### Check status

```
vcs status
```

---

### Checkout previous version

```
vcs checkout c1
```

---

## 🧠 Design Decisions

- **SHA-256 hashing** for content-based tracking  
- **Snapshot-based commits** (not diffs)  
- **Simple commit IDs (`c1`, `c2`)** for readability  
- JSON used for easy inspection and debugging  

---

## 📚 What I Learned

- How Git internally stores files and commits  
- Difference between working directory, staging, and commits  
- Designing systems with multiple states  
- Importance of hashing and immutability  
- Building CLI tools and handling user input  

---

## 🚀 Future Improvements

- `diff` command  
- `.vcsignore` support  
- branching and merging  
- better CLI formatting  

---

## 🔥 Key Insight

> A version control system is not just about storing files — it's about tracking **state transitions over time**.
