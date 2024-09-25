# Automação de Climas

Esta automação consulta uma _API_ governamental para recuperar dados das cidades de diferentes regiões metropolitanas do Brasil, para em seguida realizar um _web scraping_ e exibir no terminal a previsão do tempo para a semana em todas as cidades.

## Início

Estas instruções detalham o fluxo que deve ser seguido para poder executar esta automação.

### Pré-requisitos
- Ter o _Python_ instalado na máquina.
- Ter o _Anaconda Navigator_ instalado para gerenciamento de ambientes e dependências.


### Execução

* Criar um ambiente _Conda_. Dentro da pasta do projeto, rodar esse código

    ```
    conda create --name API_Clima_Amazonas python=3.10
    conda activate API_Clima_Amazonas
    ```

* Testar (saída esperada: _Python_ 3.10.4)

    ```
    (API_Clima_Amazonas) python --version
    >>> Python 3.10.4
    ```


* Instalar as dependências

    ```
    python -m pip install -r requirements.txt
    ```

* Executar o _bot_

    ```
    python bot.py
    ```
