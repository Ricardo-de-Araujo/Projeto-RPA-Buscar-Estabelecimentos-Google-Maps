@echo off
echo =====================================
echo Iniciando Automacao Google Maps (Docker)
echo =====================================

REM Caminho local do projeto
cd C:\RPA\projeto_rpa_maps

echo.
echo [1/3] Construindo imagem Docker...
docker build -t rpa_maps .

echo.
echo [3/3] Executando container...
docker run --rm ^
  --name rpa_maps ^
  -v C:\RPA\projeto_rpa_maps\app\saida:/rpa/app/saida ^
  -v C:\RPA\projeto_rpa_maps\app\logs:/rpa/app/logs ^
  rpa_maps

echo Automação concluída.
echo =====================================

REM Descomente caso queira que a janela não feche
pause