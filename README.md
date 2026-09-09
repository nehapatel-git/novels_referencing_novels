# novels referencing novels

A perpetually growing visual network of references in novels of other novels. 
This repo contains code for a program that allows a user to update the network when a new reference is found.

### 1. Clone the repository
```bash
git clone https://github.com/
```
### 2. Setup
```bash
# navigate to the project folder
cd novels_referencing_novels

# create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### 3. Run the program
```bash
./run.sh
```

![Screenshot](https://raw.githubusercontent.com/nehapatel-git/novels_referencing_novels/main/screenshot.png)

[**Open the interactive example**](https://nehapatel-git.github.io/novels_referencing_novels/viz.html)

Some features: zoom, drag nodes, hover over nodes to see citation details, hover over links to see notes on the reference.
