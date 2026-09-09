from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("Iniciando o Robô...")
driver = webdriver.Chrome()

try:
    print("Acessando a página de ofertas...")
    driver.get("https://www.mercadolivre.com.br/ofertas")

    espera = WebDriverWait(driver, 10)
    
    print("Procurando os produtos na tela...")
    
    cards_produtos = espera.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".poly-card--grid-card"))
    )

    print(f"Encontrei {len(cards_produtos)} produtos na página inicial!")

    # Lendo apenas os 3 primeiros para teste
    for i, card in enumerate(cards_produtos[:3], 1):
        try:
            # 1. Pegando o título e o link normalmente
            titulo = card.find_element(By.CSS_SELECTOR, ".poly-component__title").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

            # 2. Pegando o PREÇO NOVO e limpando as quebras de linha
            preco_novo_bruto = card.find_element(By.CSS_SELECTOR, ".andes-money-amount--cents-superscript").text
            preco_novo = preco_novo_bruto.replace("\n", "") # Transforma 'R$\n900\n,\n60' em 'R$900,60'

            # 3. Pegando o PREÇO ANTIGO com segurança (pode não existir)
            preco_antigo = "Sem preço anterior"
            # Note o 'find_elements' no plural! Retorna uma lista.
            busca_preco_antigo = card.find_elements(By.CSS_SELECTOR, ".andes-money-amount--previous") 
            
            if len(busca_preco_antigo) > 0:
                # Se a lista não for vazia, pegamos o primeiro item e limpamos
                preco_antigo = busca_preco_antigo[0].text.replace("\n", "")

            # Imprimindo de forma amigável no terminal
            print(f"\n--- Produto {i} ---")
            print(f"📦 Título: {titulo}")
            print(f"❌ Preço Antigo: {preco_antigo}")
            print(f"✅ Preço Novo: {preco_novo}")
            print(f"🔗 Link: {link}")

        except Exception as e:
            print(f"\nErro ao ler detalhes do produto {i}: {e}")

except Exception as e:
    print(f"\nErro de execução ou elemento não encontrado: {e}")

finally:
    driver.quit()
    print("\nNavegador fechado.")