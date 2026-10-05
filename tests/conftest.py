import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    # Configuración para que no se abra la ventana (opcional, útil para CI/CD)
    # options = Options()
    # options.add_argument("--headless") 
    
    # Inicializar driver con webdriver-manager (resuelve problemas de versión)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.implicitly_wait(5) # Espera implícita global
    driver.maximize_window()
    
    yield driver # Aquí se ejecuta el test
    
    driver.quit() # Cerrar navegador al finalizar