import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.buscar import BuscarProducto
from pages.carrito import Carrito


def test_agregar_y_eliminar_producto():
    """
    Prueba el flujo de agregar y eliminar un producto del carrito en OpenCart
    """
    try:
        # Inicializar WebDriver con bloque de contexto
        driver = webdriver.Chrome()
        driver.maximize_window()  # Maximizar ventana para mejor visibilidad
        driver.get("http://opencart.abstracta.us/")

        # Paso 1: Buscar el producto "iPhone"
        buscar = BuscarProducto(driver)
        buscar.buscar_producto("iPhone")

        # Paso 2: Seleccionar el primer producto
        buscar.seleccionar_primer_producto()

        # Paso 3: Agregar el producto al carrito
        # Reemplazar sleep por espera explícita
        wait = WebDriverWait(driver, 10)
        agregar_al_carrito = wait.until(
            EC.element_to_be_clickable((By.ID, "button-cart"))
        )
        agregar_al_carrito.click()

        # Esperar mensaje de confirmación en lugar de sleep
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )

        # Paso 4 y 5: Ir al carrito y verificar
        carrito = Carrito(driver)
        carrito.ir_a_carrito()
        carrito.ver_carrito()

        # Validación: Verificar producto en carrito
        try:
            price_element = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//td[@class='text-right' and contains(text(), '123.20')]")
                )
            )
            print("El producto (iPhone) está en el carrito.")
        except TimeoutException:
            raise AssertionError("El producto (iPhone) NO está en el carrito.")

        # Paso 6: Eliminar el producto
        carrito.eliminar_producto()

        # Paso 7: Verificar carrito vacío
        assert carrito.validar_carrito_vacio(), "El carrito no está vacío"

    finally:
        # Asegurar que el navegador se cierre incluso si hay errores
        driver.quit()


if __name__ == "__main__":
    test_agregar_y_eliminar_producto()