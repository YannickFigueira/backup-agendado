# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import re

# Adiciona o diretório atual (onde está o main.spec e o config.py) ao sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Agora o import do config funcionará sem erro!
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
    with open(os.path.join(BASE_DIR, "version.txt"), "w", encoding="utf-8") as f:
        f.write(conteudo_version_txt)

    version_file = os.path.join(BASE_DIR, "version.txt")

# Restante do seu .spec (Analysis, PYZ, EXE, etc.)...