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

    # Espera 500 milissegundos a cada vez que o bot não encontra o input
    while len(bot.find_elements('//*[@id="APjFqb"]', By.XPATH)) < 1:
        print("Carregando...")
        bot.wait(500)
    
    barraPesquisa = bot.find_element('//*[@id="APjFqb"]', By.XPATH)

    # Limpa o input e envia a pesquisa por clima da cidade
    barraPesquisa.clear()
    barraPesquisa.send_keys(cidade)
    bot.wait(1000)
    bot.enter()
    

def Capturar(bot:WebBot):
    # Nome da cidade, Estado
    # //*[@id="oFNiHe"]/omnient-visibility-control/div/div/div/div[1]/span[3]

    # Clima                     # Temperatura               # Informação extra (não tem em todos)
    # //*[@id="wob_dc"]         # //*[@id="wob_tm"]         # //*[@id="wob_wc"]/div[4]/div[1]

    # Chuva                     # Vento                     # Umidade
    # //*[@id="wob_pp"]         # //*[@id="wob_ws"]         # //*[@id="wob_hm"]

    # Dia da semana                             # Temperatura
    # //*[@id="wob_dp"]/div[1]/div[1]           # //*[@id="wob_dp"]/div[1]/div[3]/div[1]/span[1]
    # //*[@id="wob_dp"]/div[2]/div[1]           # //*[@id="wob_dp"]/div[1]/div[3]/div[2]/span[1]
    
    xnome = '//*[@id="oFNiHe"]/omnient-visibility-control/div/div/div/div[1]/span[3]'
    xclima = '//*[@id="wob_dc"]'
    xtemperatura = '//*[@id="wob_tm"]'
    xchuva = '//*[@id="wob_pp"]'
    xumidade = '//*[@id="wob_hm"]'
    xvento = '//*[@id="wob_ws"]'
    xextra = '//*[@id="wob_wc"]/div[4]/div[1]'

    if bot.find_element(xextra, By.XPATH):
        infoExtra = bot.find_element(xextra, By.XPATH).text
    else:
        infoExtra = ''

    nome = bot.find_element(xnome, By.XPATH).text
    clima = bot.find_element(xclima, By.XPATH).text
    temperatura = bot.find_element(xtemperatura, By.XPATH).text
    chuva = bot.find_element(xchuva, By.XPATH).text
    umidade = bot.find_element(xumidade, By.XPATH).text
    vento = bot.find_element(xvento, By.XPATH).text

    cont = 0
    dias = []
    while True:
        cont += 1
        xdia = f'//*[@id="wob_dp"]/div[{cont}]/div[1]'
        xmaxima = f'//*[@id="wob_dp"]/div[{cont}]/div[3]/div[1]/span[1]'
        xminima = f'//*[@id="wob_dp"]/div[{cont}]/div[3]/div[2]/span[1]'

        diaDaSemana = bot.find_element(xdia, By.XPATH).text
        diaDaSemana = diaDaSemana.capitalize()
        tempMax = bot.find_element(xmaxima, By.XPATH).text
        tempMin = bot.find_element(xminima, By.XPATH).text
        
        dias.append([diaDaSemana, tempMax, tempMin])
        if cont == 8:
            break
        
    previsao = {
        "nome" : nome,
        "clima" : clima,
        "temperatura" : temperatura,
        "chuva" : chuva,
        "umidade" : umidade,
        "vento" : vento,
        "dias" : dias,
        "extra" : infoExtra
    }

    return previsao

def Exibir(previsao:dict):
    # Manaus, AM hoje:
    # Clima: Nublado | Temperatura: 38° C
    # Chuva: 0% | Umidade: 51% | Vento: 13km/h
    # 
    # Previsão para a semana:
    #    Sáb     |     Dom    |     Seg    |     Ter    |     Qua    |     Qui    |     Sex    |    Sáb     
    # 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27° | 38°↑ ↓ 27°

    dia1 = previsao["dias"][0][0]
    dia2 = previsao["dias"][1][0]
    dia3 = previsao["dias"][2][0]
    dia4 = previsao["dias"][3][0]
    dia5 = previsao["dias"][4][0]
    dia6 = previsao["dias"][5][0]
    dia7 = previsao["dias"][6][0]
    dia8 = previsao["dias"][7][0]

    ma1 = previsao["dias"][0][1] 
    ma2 = previsao["dias"][1][1]
    ma3 = previsao["dias"][2][1] 
    ma4 = previsao["dias"][3][1]
    ma5 = previsao["dias"][4][1] 
    ma6 = previsao["dias"][5][1]
    ma7 = previsao["dias"][6][1] 
    ma8 = previsao["dias"][7][1]
    
    mi1 = previsao["dias"][0][2] 
    mi2 = previsao["dias"][1][2]
    mi3 = previsao["dias"][2][2]
    mi4 = previsao["dias"][3][2]
    mi5 = previsao["dias"][4][2] 
    mi6 = previsao["dias"][5][2]
    mi7 = previsao["dias"][6][2]
    mi8 = previsao["dias"][7][2]

    texto = f"""
{previsao["nome"]} hoje: {previsao["extra"]}
Clima: {previsao["clima"]} | Temperatura: {previsao["temperatura"]}° C
Chuva: {previsao["chuva"]} | Umidade: {previsao["umidade"]} | Vento: {previsao["vento"]}

Previsão para a semana:
   {dia1}     |     {dia2}    |     {dia3}    |     {dia4}    |     {dia5}    |     {dia6}    |     {dia7}    |    {dia8}     
{ma1}°↑ ↓ {mi1}° | {ma2}°↑ ↓ {mi2}° | {ma3}°↑ ↓ {mi3}° | {ma4}°↑ ↓ {mi4}° | {ma5}°↑ ↓ {mi5}° | {ma6}°↑ ↓ {mi6}° | {ma7}°↑ ↓ {mi7}° | {ma8}°↑ ↓ {mi8}°
------------------------------------------------------------------------------------------------------
""" 
    
    print(texto)

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
        bot.browse('https://www.google.com/')
        for regiao in regioesMetropolitanas:
            uf = regiao["uf"]
            nome = regiao["nome"].upper()
            print(f"CLIMA EM {nome}")
            for municipio in regiao["municipios"]:
                cidade = f'Clima em {municipio}, {uf} hoje'
                
                Pesquisar(bot, cidade)
                bot.wait(1000)
                previsao = Capturar(bot)
                Exibir(previsao)


    except Exception as ex:
        print(ex)
        bot.save_screenshot('erro.png')
    
    finally:
        bot.wait(3000)
        bot.stop_browser()
        print("OK")


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
