# OCR for Math expressions

## Main ideas
- Generate training images of math expressions by Latex.
- Train the model using those training samples.
- When doing OCR, capture the image of a math expressions by a snipping GUI made by PyQt6.
- Use the trained model to do OCR on the captured image.

## Required software and packages
The following instructions are tested on Windows 11, but I believe they can be adapted to other operating systems with modest modifications.

Install [Python3](https://www.python.org/), [Tex Live](https://www.tug.org/texlive/), [Ghostscript](https://www.ghostscript.com/), and [ImageMagick](https://imagemagick.org/index.php).
Don't forget to config the environment PATH if necessary. You may want to check the installation by typing the following command in the powershell.
```powershell
python --version
pdflatex --version
convert --version
```

Install python packages [NumPy](https://numpy.org/), [Pillow](https://pillow.readthedocs.io/en/stable/installation.html), [PyQt6](https://pypi.org/project/PyQt6/).

Make sure Windows allows executing PowerShell script. See [How to enable execution of PowerShell scripts?](https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts) for details about this issue.

## Building instructions
Generating all sample images:
```powershell
python generate.py
```

Run the snipping GUI
```powershell
python snipping.py
```
