# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('Components', 'Components'), ('D:\\MyProjects\\Myjarvis\\.venv\\Lib\\site-packages\\pvporcupine\\resources', 'pvporcupine/resources'), ('D:\\MyProjects\\Myjarvis\\.venv\\Lib\\site-packages\\pvporcupine\\lib', 'pvporcupine/lib')],
    hiddenimports=['pyaudio', 'pyttsx3', 'speech_recognition', 'google.genai', 'dotenv'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon\\myjarvisicon.ico'],
)
