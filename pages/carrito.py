from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple


class Carrito:
    """
    Clase que maneja las operaciones relacionadas con el carrito de compras.
    """

    # Tiempo de espera predeterminado
    TIMEOUT = 10

    def __init__(self, driver):
        """
        Inicializa la clase Carrito.

        Args:
            driver: Instancia del WebDriver de Selenium
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

        # Localizadores como tuplas de (By, str)
        self._locators = {
            'cart_button': (By.ID, "cart"),
            'view_cart_button': (By.XPATH, "//strong[contains(text(),'View Cart')]"),
            'remove_button': (By.XPATH, "//button[@type='button' and @data-original-title='Remove']"),
            'empty_cart_message': (By.XPATH, "//p[text()='Your shopping cart is empty!']")
        }

    def _click_element(self, locator: Tuple[By, str], error_message: str) -> None:
        """
        Método auxiliar para hacer click en elementos con manejo de errores.

        Args:
            locator: Tupla con el tipo de localizador y el valor
            error_message: Mensaje a mostrar en caso de error

        Raises:
            TimeoutException: Si el elemento no se encuentra o no es clickeable
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"{error_message}: {str(e)}")
            raise

    def ir_a_carrito(self) -> None:
        """Navega al carrito de compras."""
        self._click_element(
            self._locators['cart_button'],
            "No se pudo encontrar el botón del carrito"
        )

    def ver_carrito(self) -> None:
        """Hace click en el botón de ver carrito."""
        self._click_element(
            self._locators['view_cart_button'],
            "No se pudo encontrar el botón de ver carrito"
        )

    def eliminar_producto(self) -> None:
        """
        Elimina un producto del carrito y verifica que se haya eliminado.

        Raises:
            TimeoutException: Si no se puede eliminar el producto o verificar el carrito vacío
        """
        try:
            self._click_element(
                self._locators['remove_button'],
                "No se pudo eliminar el producto del carrito"
            )
            # Verificar que el producto se eliminó esperando el mensaje de carrito vacío
            self.wait.until(
                EC.presence_of_element_located(self._locators['empty_cart_message'])
            )
        except TimeoutException as e:
            print(f"Error al eliminar el producto: {str(e)}")
            raise

    def validar_carrito_vacio(self) -> bool:
        """
        Verifica si el carrito está vacío.

        Returns:
            bool: True si el carrito está vacío, False en caso contrario
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self._locators['empty_cart_message'])
            )
            return True
        except TimeoutException:
            return False

    def get_cantidad_productos(self) -> int:
        """
        Obtiene la cantidad de productos en el carrito.
        Returns:
            int: Número de productos en el carrito
        """
        try:
            productos = self.driver.find_elements(
                By.XPATH, "//table[@class='table table-striped']//tr[contains(@class, 'product')]"
            )
            return len(productos)
        except NoSuchElementException:
            return 0