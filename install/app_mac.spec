# -*- mode: python -*-

block_cipher = None


a = Analysis(['../application.py'],
             pathex=['../python-anser'],
             binaries=[],
             datas=[('../config/configs/*.yaml', './config/configs/'),
                    ('../config/sensors/*.yaml', './config/sensors/'),
                    ('../config/templates/*.yaml', './config/templates/'),
                    ('../app/resources/icons/*', './app/resources/icons/'),
                    ('../app/resources/cad/*', './app/resources/cad/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Anser',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='../app/resources/icons/anser_logo.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Anser',
               console=True,
               icon='../app/resources/icons/anser_logo.icns')
app = BUNDLE(coll,
             name='Anser.app',
             bundle_identifier=None,
             icon='../app/resources/icons/anser_logo.icns')
