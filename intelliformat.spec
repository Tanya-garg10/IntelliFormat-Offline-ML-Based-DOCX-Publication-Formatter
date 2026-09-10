# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for IntelliFormat Desktop Application
Build command: pyinstaller intelliformat.spec
"""

import sys
from pathlib import Path

# Get the current directory
block_cipher = None
ROOT_DIR = Path.cwd()

# Collect all data files and packages
datas = [
    # Machine learning model
    (str(ROOT_DIR / "ml" / "model.pkl"), "ml"),
    
    # Sample files for testing
    (str(ROOT_DIR / "samples" / "input.docx"), "samples"),
    (str(ROOT_DIR / "samples" / "expected_output.docx"), "samples"),
    
    # Training data (optional, for ML retraining)
    (str(ROOT_DIR / "dataset" / "training_data.csv"), "dataset"),
    
    # Configuration files
    (str(ROOT_DIR / "ml" / "training_metrics.json"), "ml"),
    (str(ROOT_DIR / "performance" / "results.json"), "performance"),
]

# Collect all hidden imports (dependencies that PyInstaller might miss)
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui', 
    'PySide6.QtWidgets',
    'PySide6.QtUiTools',
    'docx',
    'docx.oxml',
    'docx.oxml.xmlchemy',
    'docx.oxml.ns',
    'sklearn',
    'sklearn.ensemble',
    'sklearn.tree',
    'sklearn.utils',
    'joblib',
    'numpy',
    'pandas',
    'psutil',
]

a = Analysis(
    ['app.py'],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'pytest', 'IPython', 'notebook', 'jupyter',
        'tkinter', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6.QtWebEngine'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IntelliFormat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
)