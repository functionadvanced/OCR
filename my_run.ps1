param ($img_name='temp.bmp')
try{
    pdflatex -halt-on-error main.tex | Out-Null
    pdfcrop main.pdf | OUt-Null
    convert -density 300 main-crop.pdf -quality 100 -colorspace RGB $img_name | Out-Null
}
catch{
    "ERROR in powershell script."
}
