def extract_copom_minutes():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import re
    from datetime import datetime

    # Configurando as opções do webdriver
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')

    # Inicializando o webdriver ( Modificar de acordo com o webdriver utilizado )
    driver = webdriver.Chrome(options=webdriver_options)

    # Acessando o site
    driver.get('https://www.bcb.gov.br/en/publications/copomminutes/cronologicos')

    # Aguardando carregar o conteúdo da página
    time.sleep(5)

    # Encontrando todos os links na página que contêm 'Meeting'
    meeting_links = driver.find_elements(By.XPATH, '//a[contains(text(), "Meeting")]')

    # O link mais recente será o primeiro na lista
    latest_meeting_link = meeting_links[0]

    # Clicando no link para acessar a ata mais recente
    ActionChains(driver).move_to_element(latest_meeting_link).click(latest_meeting_link).perform()

    # Aguardando a nova página carregar
    time.sleep(5)

    # Extraindo o conteúdo de texto da ata
    meeting_text = driver.find_element(By.TAG_NAME, 'body').text

    # Fechando o navegador
    driver.quit()

    # As primeiras 50 linhas do meeting_text
    first_50_lines = '\n'.join(meeting_text.split('\n')[:50])

    # A expressão regular para uma data no formato "Mes dd-dd, yyyy" que vem após "Meeting"
    date_pattern = r'Meeting - (\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}-\d{1,2}, \d{4}\b)'

    # Procurando pela data nas primeiras 50 linhas
    match = re.search(date_pattern, first_50_lines)

    if match:
        # A data da ata
        ata_date = match.group(1)

        # Pegando apenas a primeira parte da data (ignorando os dias)
        month, day, year = ata_date.split(' ')[0], ata_date.split(' ')[1].split('-')[0], ata_date.split(' ')[2]

        # Convertendo a data para o formato desejado
        date_object = datetime.strptime(f'{day} {month} {year}', '%d %B %Y')
        formatted_date = date_object.strftime('%d-%m-%Y')

        print(formatted_date)

        # Dividindo o texto em seções
        sections = meeting_text.split('content_copy')

        # Pegando a seção que vem depois de 'content_copy'
        content_after_content_copy = sections[1]

        # Dividindo essa seção em subseções
        subsections = content_after_content_copy.split('Footnotes')

        # Pegando a subseção que vem antes de 'Footnotes'
        content_before_footnotes = subsections[0]

        print(content_before_footnotes)
        
        # Modificar de acordo com o diretorio que deseja que o arquivo de texto contando a ata seja salvo
        with open(f'C:/Users/pedro/OneDrive/ECONOMIA/Python/copom_extractor/txts_copom_minutes/ata_copom_{formatted_date}.txt', 'w', encoding='utf-8') as f:
            f.write(content_before_footnotes)
        
        return content_before_footnotes

copom_minutes_text = extract_copom_minutes()