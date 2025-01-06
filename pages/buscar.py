from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Tuple, Optional


class BuscarProducto:
    """
    Clase para manejar la búsqueda y selección de productos en la tienda.
    """

    TIMEOUT = 10  # Tiempo máximo de espera en segundos

    def __init__(self, driver):
        """
        Inicializa la clase BuscarProducto.

        Args:
            driver: Instancia del WebDriver de Selenium
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.TIMEOUT)

        # Localizadores
        self._locators = {
            'search_box': (By.NAME, "search"),
            'first_product': (By.XPATH, "//div[@class='product-thumb'][1]//a"),
            'search_results': (By.CLASS_NAME, "product-thumb"),
            'product_title': (By.TAG_NAME, "h1"),
            'search_button': (By.CLASS_NAME, "btn-default")
        }

    def _find_and_wait(self, locator: Tuple[By, str], wait_type: str = "presence") -> Optional[object]:
        """
        Espera y encuentra un elemento con manejo de errores.

        Args:
            locator: Tupla con el tipo de localizador y el valor
            wait_type: Tipo de espera ('presence', 'clickable', 'visible')

        Returns:
            El elemento web encontrado o None si no se encuentra

        Raises:
            TimeoutException: Si el elemento no se encuentra en el tiempo especificado
        """
        try:
            if wait_type == "clickable":
                return self.wait.until(EC.element_to_be_clickable(locator))
            elif wait_type == "visible":
                return self.wait.until(EC.visibility_of_element_located(locator))
            else:
                return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None

    def buscar_producto(self, producto: str) -> bool:
        """
        Busca un producto en la tienda.

        Args:
            producto: Nombre del producto a buscar

        Returns:
            bool: True si se encontraron resultados, False en caso contrario

        Raises:
            TimeoutException: Si no se puede acceder al campo de búsqueda
        """
        try:
            # Encontrar y limpiar el campo de búsqueda
            search_input = self._find_and_wait(self._locators['search_box'], "clickable")
            if not search_input:
                raise TimeoutException("No se pudo encontrar el campo de búsqueda")

            search_input.clear()
            search_input.send_keys(producto)

            # Presionar enter o hacer click en el botón de búsqueda
            search_button = self._find_and_wait(self._locators['search_button'], "clickable")
            if search_button:
                search_button.click()
            else:
                search_input.send_keys(Keys.RETURN)

            # Esperar a que aparezcan resultados
            return self._esperar_resultados_busqueda()

        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error durante la búsqueda: {str(e)}")
            return False

    def _esperar_resultados_busqueda(self) -> bool:
        """
        Espera a que los resultados de búsqueda aparezcan.

        Returns:
            bool: True si se encontraron resultados, False en caso contrario
        """
        try:
            results = self.wait.until(
                EC.presence_of_all_elements_located(self._locators['search_results'])
            )
            return len(results) > 0
        except TimeoutException:
            return False

    def seleccionar_primer_producto(self) -> str:
        """
        Selecciona el primer producto de los resultados de búsqueda.

        Returns:
            str: Título del producto seleccionado

        Raises:
            TimeoutException: Si no se puede seleccionar el producto
        """
        try:
            # Encontrar y hacer click en el primer producto
            primer_producto = self._find_and_wait(self._locators['first_product'], "clickable")
            if not primer_producto:
                raise TimeoutException("No se encontró el primer producto")

            # Guardar el título del producto antes de hacer click
            titulo_producto = primer_producto.text

            primer_producto.click()

            # Esperar a que cargue la página del producto y verificar el título
            self.wait.until(
                EC.presence_of_element_located(self._locators['product_title'])
            )

            return titulo_producto

        except TimeoutException as e:
            print(f"Error al seleccionar el producto: {str(e)}")
            raise

    def get_cantidad_resultados(self) -> int:
        """
        Obtiene la cantidad de productos encontrados en la búsqueda.

        Returns:
            int: Número de productos encontrados
        """
        try:
            resultados = self.driver.find_elements(*self._locators['search_results'])
            return len(resultados)
        except NoSuchElementException:
            return 0