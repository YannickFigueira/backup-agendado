# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Módulos estáticos e dinâmicos necessários para o Linux e Windows
hidden_imports = [
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtGui',
    'PyQt6.QtCore',
    'pystray',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('imagens', 'imagens'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        # Opcional: exclui o gi completo ja que nao e mais usado no Linux
        'gi',
        'gi.repository',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='backup-agendado',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='imagens/backup.png',
)