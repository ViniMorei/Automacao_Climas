from botcity.web import WebBot, Browser, By
from botcity.plugins.http import BotHttpPlugin
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def Recuperar(respostaJSON:list):
    # Cria uma lista vazia que irá receber todas as possíveis regiões metropolitanas
    regioesMetropolitanas = []

    # Itera cada região metropolitana da lista
    for itens in respostaJSON:
        municipios = []
        
        # Itera o valor da chave "municipios", que contém nome e id de cada cidade daquela região metropolitana
        for nomes in itens["municipios"]:
            # Armazena os nomes das cidades em uma lista temporária
            municipios.append(nomes["nome"])

        # Para cada região metropolitana, adiciona na lista de regiões
        # metropolitanas seu nome, a qual estado pertence e as cidades
        # que compõem a região metropolitana
        regioesMetropolitanas.append({
            "nome" : itens["nome"],
            "uf" : itens["UF"]["sigla"],
            "municipios" : municipios
        })

    return regioesMetropolitanas

def Pesquisar(bot:WebBot, cidade:str):
    # Input Google
    # //*[@id="APjFqb"]

    # Espera 1 segundo a cada vez que o bot não encontra o input
    while len(bot.find_elements('//*[@id="APjFqb"]', By.XPATH)) < 1:
        print("Carregando...")
        bot.wait(1000)
    
    barraPesquisa = bot.find_element('//*[@id="APjFqb"]', By.XPATH)

    # Limpa o input e envia a pesquisa por clima da cidade
    barraPesquisa.clear()
    barraPesquisa.send_keys(cidade)
    bot.wait(1000)
    bot.enter()
    

def Capturar(bot:WebBot):
    # Clima
    # //*[@id="wob_dc"]
    # //*[@id="wob_dc"]

    # Temperatura
    # //*[@id="wob_tm"]

    # Chuva
    # //*[@id="wob_pp"]

    # Umidade
    # //*[@id="wob_hm"]

    # Vento
    # //*[@id="wob_ws"]

    # Dia da semana
    # //*[@id="wob_dp"]/div[1]/div[1]
    # //*[@id="wob_dp"]/div[2]/div[1]

    # Temperatura
    # //*[@id="wob_dp"]/div[1]/div[3]/div[1]/span[1]
    # //*[@id="wob_dp"]/div[1]/div[3]/div[2]/span[1]

    # Informação extra (não tem em todos)
    # //*[@id="wob_wc"]/div[4]/div[1]
    pass

def Exibir():
    pass

def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()

    try:
        # Recupera o endpoint da API para determinado estado
        # Amazonas: 13, Ceará: 23, São Paulo: 35
        estado = 13
        endpointAPI = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/regioes-metropolitanas'
        # Realiza uma requisição HTTP (GET) para recuperar os dados como JSON
        respostaJSON = BotHttpPlugin(endpointAPI).get_as_json()

        # Itera os itens do JSON e coloca os nomes das cidades das regiões metropolitanas na lista de municípios
        regioesMetropolitanas = Recuperar(respostaJSON)

        # Para cada uma das regiões, realiza a pesquisa e exibição dos dados
        for regiao in regioesMetropolitanas:
            uf = regiao["uf"]
            for municipio in regiao["municipios"]:
                cidade = f'Clima em {municipio}, {uf} hoje'
                print(cidade)
                
                Pesquisar(bot, cidade)



        # Para cada item da lista, pesquisa o clima da semana e exibe os dados
        # for municipio in municipios:
        #     pass



    except Exception as ex:
        print(ex)
        bot.save_screenshot('erro.png')
    
    finally:
        bot.wait(3000)
        bot.stop_browser()


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
