from PIL import Image
from pathlib import Path
import seg
import subprocess
import os

def generate_fig(target_latex_exp, img_name="temp.bmp"):
    ''' 
    Example: generate_fig("\\pi\ \\xi") 
    '''
    with open("main.tex", 'r') as file:
        data = file.readlines()
        i = data.index("\\begin{align*}\n")
        data[i+1] = "\t".expandtabs(4) + target_latex_exp + "\n"
        data[i+2] = "\\end{align*}\n"
        data[i+3] = "\\end{document}"
        data = data[:i+4]
    with open("main.tex", 'w') as file:
        file.writelines(data)
    with open(os.devnull, 'w') as devnull:
        subprocess.run(["powershell", "./my_run.ps1 -img_name "+img_name], stdout=devnull)

def generate(img_name):
    ''' Generate and show 0-1 black-white img '''
    all_seg, black_and_white = seg.seg_one_line(img_name)
    for i in range(len(all_seg)):
        a, b, c, d = all_seg[i]
        Image.fromarray(black_and_white[c:d, a:b] * 255).convert("L").save("imgs/"+str(i)+".bmp")
        black_and_white[c:d, a] = 1
        black_and_white[c:d, b] = 1
        black_and_white[c, a:b] = 1
        black_and_white[d-1, a:b] = 1
    Image.fromarray(black_and_white * 255).show()

def get_latex_of_all_symbols():
    with open("all_symbols.txt", 'r') as file:
        data = file.readlines()
        all_symbols = []
        for each_line in data:
            if each_line[0] in ['#', '\n']:
                continue
            if each_line[0] != '\\':
                for i in each_line[:-1]:
                    all_symbols.append(i)
                if each_line[-1] != '\n':
                    all_symbols.append(each_line[-1])
            else:
                if each_line[-1] == '\n':
                    all_symbols.append(each_line[:-1])
                else:
                    all_symbols.append(each_line)
        return all_symbols

if __name__=="__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    Path(dir_path+"/imgs").mkdir(parents=True, exist_ok=True)
    all_symbols = get_latex_of_all_symbols()
    generate_fig(r"\ ".join(all_symbols), "all_symbols.bmp") # generate temp.bmp that contains all symbols
    generate("all_symbols.bmp") # split it into multiple small 0-1 bmps for each symbol, stored in ./imgs/