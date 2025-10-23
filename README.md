# Wordle Game (Tkinter)

This is a Wordle game clone built with Python and the Tkinter library.

## Requirements

* **Python 3.12.12**
* **`Pillow`** library *(Used for image processing, e.g., `bg.jpg`)*

All necessary libraries are listed in the **`requirements.txt`** file.

## Setup and Run

Here are the steps to set up and run the project on your machine.

### 1. Get the Code

If you don't have it, clone the repository and move into the project directory:

```
git clone https://github.com/i8iiii/Wordle-Project.git 
cd Wordle-Project
```
### 2. Create a Virtual Environment (.venv)

Using a virtual environment is the best practice to manage project dependencies separately.

**On macOS/Linux**
*(You may need to use `python3.12` if you have multiple versions)*

```
python3 -m venv .venv
```

**On Windows**
*(You may need to use `python -3.12` if you have multiple versions)*
```
python -m venv .venv
```


### 3. Activate the Virtual Environment

You must activate this environment every time you want to work on the project.

**On macOS/Linux (Bash/Zsh):**
```
source .venv/bin/activate
```


**On Windows (Command Prompt):**
```
.venv\Scripts\activate.bat
```


**On Windows (PowerShell):**
```
.venv\Scripts\Activate.ps1
```

*(If you get an error on PowerShell, you may need to run `Set-ExecutionPolicy Unrestricted -Scope Process` first.)*

### 4. Install Libraries (Including Pillow)

The *recommended* way is to install from the `requirements.txt` file:
```
Make sure your virtual environment is activated!
pip install -r requirements.txt
```

**Alternatively**, you can manually install the `Pillow` library:
```
pip install Pillow
```

### 5. Run the Game

Once the environment is activated and the libraries are installed, you can launch the game:

**On macOS/Linux**
```
cd path_to_your_source
python3 main.py
```
**On Windows**
```
cd path_to_your_source
python main.py
```
