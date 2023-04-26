import os
import csv
import time
import schedule
from selenium import webdriver        # Libreria per l'automazione di browser web
from selenium.webdriver.chrome.service import Service    # Classe per la configurazione del driver Chrome
from webdriver_manager.chrome import ChromeDriverManager   # Classe per la gestione dell'installazione del driver Chrome

# Percorso della cartella del progetto
project_dir = os.path.dirname(os.path.abspath(__file__))

# Definizione della directory annunci come una sotto-cartella della cartella del progetto
annunci_dir = os.path.join(project_dir, 'annunci')

# Configurazione del driver di Chrome utilizzando la classe Service e ChromeDriverManager
service = Service(executable_path=ChromeDriverManager().install())     # Installazione automatica del driver Chrome
driver = webdriver.Chrome(service=service)

# Funzione che cerca gli annunci di lavoro su Subito.it e li salva in un file CSV
def search_jobs():
    # Apertura della pagina di ricerca di lavoro su Subito.it
    driver.get('https://www.subito.it/annunci-campania/vendita/offerte-lavoro/caserta/?q=assistente%20anziani')
    
    # Inserimento di una query di ricerca specifica ("Python Developer")
    search_box = driver.find_element_by_name('text')
    search_box.send_keys('Python Developer')
    search_box.submit()
    
    # Ottenere tutti gli annunci trovati
    results = driver.find_elements_by_class_name('items___oNLFe')
    
    # Verifica se ci sono nuovi annunci rispetto alla precedente ricerca
    global last_results
    if last_results != results:
        print(f"Nuovi annunci trovati: {len(results)}")
        last_results = results
        
        # Salva gli annunci in un file CSV nella cartella "annunci"
        with open(os.path.join(annunci_dir, 'annunci.csv'), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Titolo', 'Descrizione', 'Prezzo'])
            for result in results:
                title = result.find_element_by_class_name('title___2UVFn').text
                description = result.find_element_by_class_name('description___2_tDE').text
                price = result.find_element_by_class_name('price___3KIAO').text
                writer.writerow([title, description, price])
                
        print("Annunci salvati correttamente")
    else:
        print("Nessun nuovo annuncio trovato")

# Definire il tempo di ricerca (ogni giorno alle 9:00)
schedule.every().day.at("09:00").do(search_jobs)

# Definire l'ultimo risultato
last_results = None

# Ciclo principale per eseguire la ricerca ogni volta che scatta l'orario impostato
while True:
    schedule.run_pending()      # Controllare se è il momento di eseguire la funzione search_jobs()
    time.sleep(1)              # Attendere 1 secondo prima di controllare di nuovo

