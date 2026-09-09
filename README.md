# novels referencing novels

A perpetually growing visual network of references in novels of other novels. 
This repo contains code for a program that allows a user to update the network when a new reference is found.

### 1. Acquire a Google API key
a. Sign into https://console.cloud.google.com/
b. Go to the **Credentials** tab
c. Create a new project or select an existing project
d. Go to **Create credentials** > **API key**
c. Copy API key

### 2. Clone the repository and navigate to the project folder:
```bash
git clone https://github.com/
cd books_referencing_books
```

### 3. Create your .env file to store your API key
```bash
cp .env.example .env

# then open .env and paste in your key
```

### 4. Create a virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the program
```bash
./run.sh
```

![Screenshot](https://raw.githubusercontent.com/nehapatel-git/novels_referencing_novels/main/screenshot.png)

[**Open the interactive example**](https://nehapatel-git.github.io/novels_referencing_novels/viz.html)

Some features: zoom, drag nodes, hover over nodes to see citation details, hover over links to see notes on the reference.
