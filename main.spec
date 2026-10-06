# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import re

# SPECPATH é a variável global nativa do PyInstaller que aponta para o diretório do .spec
BASE_DIR = SPECPATH

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config

# --- GERADOR DINÂMICO DE RECURSO DE VERSÃO (APENAS PARA WINDOWS) ---
version_file = None

if sys.platform.startswith("win"):
    def formatar_versao(versao_str):
        numeros = [int(n) for n in re.findall(r'\d+', versao_str)]
        while len(numeros) < 4:
            numeros.append(0)
        return tuple(numeros[:4])

    v_tuple = formatar_versao(config.VERSION)
    v_str = ".".join(map(str, v_tuple))

    conteudo_version_txt = f"""VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={v_tuple},
    prodvers={v_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'YannickFigueira'),
            StringStruct(u'FileDescription', u'{config.NOME_PROGRAMA}'),
            StringStruct(u'FileVersion', u'{v_str}'),
            StringStruct(u'InternalName', u'{config.REPO}'),
            StringStruct(u'OriginalFilename', u'{config.REPO}.exe'),
            StringStruct(u'ProductName', u'{config.NOME_PROGRAMA}'),
            StringStruct(u'ProductVersion', u'{v_str}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    version_file_path = os.path.join(BASE_DIR, "version.txt")
    with open(version_file_path, "w", encoding="utf-8") as f:
        f.write(conteudo_version_txt)

    version_file = version_file_path

# --- CONFIGURAÇÃO DE COMPILAÇÃO DO PYINSTALLER ---

block_cipher = None

hidden_imports = [
    'PyQt6',
    'PyQt6.QtWidgets',
    'PyQt6.QtGui',
    'PyQt6.QtCore',
    'pystray',
]

a = Analysis(
    ['main.py'],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        ('imagens', 'imagens'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'gi',
        'gi.repository',
    ],
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
    name='backup-agendado',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='imagens/backup.png',
    version=version_file,
)