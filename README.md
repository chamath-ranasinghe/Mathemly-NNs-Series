# Mathemly — NNs Series

Repository of Manim animations and notes for the neural networks series.

## Contents
- A short description of each folder (add folders as needed)
- How to run Manim projects (example provided)
- Optional: VS Code Manim Sideview extension

## Prerequisites
- Python 3.8+ (use virtualenv/venv recommended)

## Using a virtual environment

01. Navigate to Animation Code folder

```
cd Animation Code
```

02. Install

```
python -m venv <name_for_venv>
```
03. Run the virtual environment

```
venv/scripts/activate
```

04. Manim Community Edition (manim)
    - Install: `pip install manim`

## Typical project structure
- venv
- NN/
    - main.py
    - manim.config
    - media/ (This is where the exported videos are stored)

(Other folders are not important)

## How to run Manim projects (one example)
Navigate to the *NN* folder and run Manim CLI. Basic command pattern:
```
manim -pql main.py SceneClassName
```
Options used above:
- `-p` : open the rendered video automatically
- `-q l` : quality "low" (use `-qh` for high, `-qm` for medium)

Example: If there is a scene class `NeuronIntro`, run:
```
manim -pql main.py NeuronIntro
```
To render all scenes in a file, omit the scene name (Manim may render the default scene or require explicit names depending on version):
```
manim -pql main.py
```
If you prefer module-style invocation:
```
python -m manim -pql main.py NeuronIntro
```

Notes:
- If animations fail due to missing fonts or packages, install the required system dependencies or fonts and re-run (This could happen when texts are rendering)

### Text rendering

- The interpreter may prompt an error where you need to install a LaTex package.

Install [text](https://miktex.org/) and setup accordingly

## Optional: VS Code — Manim Sideview
To improve authoring experience, install the "Manim Sideview" extension in VS Code. This would be helpful to view while coding and easier rendering:
1. Open VS Code → Extensions view (Ctrl+Shift+X).
2. Search for "Manim Sideview" and install it.
3. Configure the extension to the project Python interpreter (select the virtualenv).
4. Use the side panel to preview scenes and run renders from the editor.

If Sideview is unavailable for your Manim version, rely on the CLI commands above or the official Manim extensions.

## Tips
- Keep scene classes small and focused for faster iteration.
- Use `-ql` while developing; render high quality for final exports.

## Contributing
- Use this repo as a starting point for you animations or if you are looking for any inspiration

Enjoy animating!
