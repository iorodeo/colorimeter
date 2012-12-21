# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), '..\\..\\..\\colorimeter\\colorimeter\\python\\Colorimeter\\bin\\colorimeter-main'],
             pathex=['C:\\Users\\Olympiad\\work\\pyinstaller\\pyinstaller-1.5\\pyinstaller-1.5'])

# Add data files
data_path = os.path.join(os.environ['HOMEPATH'],'work','colorimeter', 'colorimeter', 'python', 'Colorimeter', 'colorimeter', 'data')
data_files = os.listdir(data_path)
for f in data_files:
    f_tuple = (os.path.join('data',f), os.path.join(data_path,f), 'DATA') 
    a.datas.append(f_tuple)

pyz = PYZ(a.pure)
exe = EXE( pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'colorimeter-v02.exe'),
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='colorimeter_icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'colorimeter-v02.exe.app'))
