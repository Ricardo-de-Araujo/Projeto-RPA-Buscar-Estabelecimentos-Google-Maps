## 1 - RPA Google Maps - Automação de Busca de Estabelecimentos

Este projeto realiza uma automação para pesquisar estabelecimentos no Google Maps, acessar cada resultado e coletar informações como nome, avaliação, endereço, número de avaliações e link da página. A automação roda em um ambiente Python Dockerizado e utiliza Selenium com Google Chrome.

## 2 - Tecnologias Utilizadas

As tecnologias utilzadas no processo foram:

- Python
- Selenium
- Pandas
- ChromeDriverManager

## 3 - Instalação

Requer python 3.13 e Google Chrome instalados.

## 4 - Configurações

As configurações estão parametrizadas no arquivo JSON `app/config/config.json`.

### 4.1 - Headless

Parâmetro responsável por executar a automação em background (sem interface gráfica) quando seu valor for TRUE.
Nota: Para executar a automação com docker, seu valor deve obrigatoriamente em TRUE.

### 4.2 - Tamanho da janela

O parâmetro "chrome_window_size" é responsável por definir a resolução da janela. Necessário para evitar elementos fora da tela.

### 4.3 - Link do site

O link do google maps é definido no parâmetro "link_google_maps" do arquivo de configuração.

### 4.4 - Nome do arquivo de saída

O nome do arquivo de saída pode é definido no parâmetro "output_file_name".

## 5 - Organização das pastas

- app
  - config
    - config.json #contém os parâmetros à serem configurados.
    - path_utils.py #define os diretórios de forma dinâmica para facilitar nas chamadas dos scripts além de facilitar qualquer alteração.
  - entrada
    - input.json #contém os dados de entrada.
  - logs
    - log_dd_mm_aaaa_hh_mm_ss #os logs são gerados com timestamp para cada execução.
  - saida #pasta onde é disponibilizado o arquivo Excel .xlsx preenchido com as informações requeridas.
  - tarefa
    - buscar_maps.py #task responsável por realizar a busca no google maps.
    - criar_driver.py #task responsável por criar o driver do Chrome com os parâmetros necessários.
    - criar_log.py #task responsável pela criação do log e configura o logging para ser utilizado nos scripts com a biblioteca logging importada.
    - salvar_excel.py #task responsável por inserir os dados no excel e formatar o tamanho das colunas.
  - main.py #ponto de partida inicial que contém o fluxo de execução das tarefas.
- Dockerfile #arquivo de configurações do Docker
- requirements.txt #Libs necessárias para execução.

## 6 - Fluxo Geral da Automação

  1. A automação lê um arquivo JSON de entrada.
  2. Abre o Google Maps (Chrome + Selenium).
  3. Realiza a busca conforme os parâmetros.
  4. Clica nos resultados e extrai informações.
  5. Salva os dados no Excel na pasta /saida.
  6. Gera logs de execução na pasta /logs.

## 7 - Execução

  Observação: Os diretórios devem ser substituídos de acordo com o local onde o projeto está instalado.

### 7.1 - Agendamento da Execução

  Para executação através do agendamento, basta criar uma tarefa no agendador de tarefa do windows e coloque para executar um dos arquivos
  Sem Docker: "executar_rpa_sem_docker.bat".
  Com Docker: "executar_rpa_com_docker.bat"

  A Automação também pode ser iniciada executando o arquivo .bat


### 7.2 - Execução sem Docker

Primeiro baixa as bibliotecas necessárias definidas no requirements.txt

```ssh
pip install -r requirements.txt
```

Após execute o script.

```ssh
py app/main.py
```


### 7.3 - Execução com Docker

Primeiro crie a imagem

```ssh
docker build -t <nome_imagem> .
```

Depois crie e inicie o conteiner

```ssh
docker run <nome_imagem>
```

Para copiar o arquivo de saída e log utilize os comandos

```ssh
docker cp <id_conteiner>:/rpa/app/saida ./app/
docker cp <id_conteiner>:/rpa/app/log ./app/
```

Para visualizar o ID do conteiner utilize

```ssh
docker ps -a
```

Para excluir o conteiner

```ssh
docker rm <id_conteiner>
```

Para excluir a imagem

```ssh
docker rmi <id_imagem>
```
