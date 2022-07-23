'''
This is the test script
'''
import engine
import generate
from PIL import Image

generate.generate_fig(r"a+b+\gamma-[a-b]=(\gamma)")
all_names = generate.get_latex_of_all_symbols()
results = engine.identify(Image.open("temp.bmp"))
print("".join(results))