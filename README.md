# 💾 Backup Agendado

Programa de controle para agendamento e automação de backups de arquivos entre diferentes unidades de armazenamento local ou em rede.

---

## 🚀 Sobre o Projeto

Este projeto nasceu da necessidade de automatizar a cópia de segurança de arquivos importantes de forma silenciosa e eficiente. O programa permite que o usuário configure uma **pasta de origem**, uma **unidade de destino** (como um HD Externo ou Pendrive) e defina **horários agendados** para que o backup aconteça automaticamente.

### 🛠️ Funcionalidades Principais

* **Mapeamento Flexível:** Seleção visual de qualquer diretório de origem e destino.
* **Agendamento Inteligente:** Configuração de rotinas automáticas (diárias, semanais ou em horários específicos).
* **Backup Incremental:** Copia apenas os arquivos que foram modificados desde o último backup, economizando tempo e espaço.
* **Histórico de Logs:** Criação de um arquivo `.log` para acompanhar o sucesso ou falhas das rotinas de backup.

---

## 📦 Tecnologias Utilizadas

* **Linguagem:** Python 3.12
* **Interface Gráfica:** Tkinter / CustomTkinter
* **Agendamento:** Biblioteca `schedule` ou `apscheduler`
* **Manipulação de Arquivos:** `shutil` e `os`
