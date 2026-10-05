import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- TEST 1: LOGIN (Criterio: Espera explícita + validación URL/Texto) ---
def test_login_exitoso(driver):
    driver.get("https://www.saucedemo.com/")
    
    # Identificamos elementos (usando IDs que vimos en la clase)
    input_user = driver.find_element(By.ID, "user-name")
    input_pass = driver.find_element(By.ID, "password")
    btn_login = driver.find_element(By.ID, "login-button")
    
    # Acción
    input_user.send_keys("standard_user")
    input_pass.send_keys("secret_sauce")
    btn_login.click()
    
    # Validación con ESPERA EXPLÍCITA (Requisito obligatorio del PDF)
    # Esperamos a que la URL cambie o aparezca el título del inventario
    WebDriverWait(driver, 10).until(
        EC.url_contains("/inventory.html")
    )
    
    # Validaciones
    assert "inventory.html" in driver.current_url
    # Validar texto "Products" o "Swag Labs" (El título real es "Products")
    titulo = driver.find_element(By.CLASS_NAME, "title").text
    assert titulo == "Products"

# --- TEST 2: CATÁLOGO (Criterio: Título, presencia productos, lista 1ro) ---
def test_verificacion_catalogo(driver):
    # Setup: Login rápido para llegar al inventario
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 1. Validar Título
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
    
    # 2. Comprobar presencia de productos (Lista de items)
    # La clase 'inventory_item' agrupa cada producto
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No se encontraron productos"
    
    # 3. Listar nombre y precio del primero
    primer_producto = productos[0]
    nombre = primer_producto.find_element(By.CLASS_NAME, "inventory_item_name").text
    precio = primer_producto.find_element(By.CLASS_NAME, "inventory_item_price").text
    
    print(f"\n--- Producto Verificado ---")
    print(f"Nombre: {nombre}")
    print(f"Precio: {precio}")
    assert nombre != "" and precio != ""

# --- TEST 3: CARRITO (Criterio: Agregar, verificar contador, ver en carrito) ---
def test_agregar_al_carrito(driver):
    # Setup: Login
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 1. Agregar primer producto
    # El botón de agregar tiene id 'add-to-cart-sauce-labs-backpack' (o similar)
    # Usaremos un selector más genérico para el primer botón de add
    btn_add = driver.find_elements(By.CLASS_NAME, "btn_inventory")[0]
    btn_add.click()
    
    # 2. Verificar contador del carrito (Badge)
    # El badge suele tener clase 'shopping_cart_badge'
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1", f"El contador debería ser 1, pero es {badge.text}"
    
    # 3. Navegar al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # 4. Comprobar que el producto está en el carrito
    # En la página del carrito, los items tienen clase 'cart_item'
    items_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items_carrito) > 0, "El carrito está vacío"
    
    # Validar que el nombre coincida con el que agregamos
    nombre_en_carrito = items_carrito[0].find_element(By.CLASS_NAME, "inventory_item_name").text
    assert "Backpack" in nombre_en_carrito # Sabemos que el primero es la mochila