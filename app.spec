# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],  # Main entry point of your application
    pathex=['.'],
    binaries=[],
    datas=[
        ('images/', 'images/'),  # Include images directory
        ('.env', '.'),  # Include .env file
        ('excel_service.py', '.'),  # Include your additional Python files
        ('label_service.py', '.'),
        ('search_service.py', '.'),
        ('gui.py', '.')
    ],
    hiddenimports=[
        'reportlab.graphics.barcode.code128',  # Add missing hidden imports
        'reportlab.graphics.barcode.code39',   # Ensure code39 is included as well
        'reportlab.graphics.barcode.code93',   # Ensure code93 is included as well
        'reportlab.graphics.barcode.common',   # Include common barcode
        'reportlab.graphics.barcode.qr',       # Include QR code
        'reportlab.graphics.barcode.usps',     # Include USPS barcode
        'reportlab.graphics.barcode.usps4s',   # Include USPS 4-state barcode
        'reportlab.graphics.barcode.ecc200datamatrix', # Include DataMatrix barcode
        'reportlab.graphics.barcode.pdf417', # Include PDF417 barcode
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False  # Set to True if you want a console window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app'
)
