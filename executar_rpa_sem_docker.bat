@echo off
echo Iniciando automação RPA Google Maps...

REM Vai até a pasta do projeto
cd C:\RPA\projeto_rpa_maps

REM Atualiza dependências
pip install --no-cache-dir -r requirements.txt

REM Executa o script
python app\main.py

REM Descomente caso queira que a tela não feche
REM pause
