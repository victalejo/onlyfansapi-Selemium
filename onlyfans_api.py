from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class OnlyFansAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.logged_in = False

    def login(self):
        try:
            self.driver.get("https://onlyfans.com")
            wait = WebDriverWait(self.driver, 20)
            username_input = wait.until(EC.element_to_be_clickable((By.ID, 'input-15')))
            password_input = wait.until(EC.element_to_be_clickable((By.ID, 'input-18')))
            username_input.click()
            username_input.send_keys(self.username)
            password_input.click()
            password_input.send_keys(self.password)
            self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div/div/div[2]/div/form/button[1]').click()
            sleep(10)  # Esperar a que se complete el inicio de sesión
            self.logged_in = True
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if not self.logged_in:
                self.driver.quit()

    def navigate_to_messages(self):
        if self.logged_in:
            try:
                mensajes_link = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-name='Chats']"))
                )
                mensajes_link.click()
            except Exception as e:
                print(f"Error al hacer click en Mensajes: {e}")

    def fetch_all_messages(self):
        self.scroll_to_top()
        return self.fetch_messages()

    def fetch_latest_messages(self, last_message_time=5):
        sleep(last_message_time)  # Esperar unos segundos para que se carguen los últimos mensajes
        return self.fetch_messages(latest=True)

    def fetch_messages(self, latest=False):
        chat_container = self.driver.find_element(By.CLASS_NAME, 'b-chats__conversations-content')
        messages = chat_container.find_elements(By.XPATH, ".//div[contains(@class, 'b-chat__message')]")
        
        processed_texts = set()  # Almacenar los textos ya procesados para evitar duplicados
        output_messages = []
        for message in messages[-5:] if latest else messages:
            text_elements = message.find_elements(By.CLASS_NAME, 'b-chat__message__text')
            if not text_elements:
                continue
            message_text = ' '.join([element.text for element in text_elements if element.text.strip() != ''])
            if message_text in processed_texts:
                continue
            processed_texts.add(message_text)
            
            sender = "mí" if 'm-from-me' in message.get_attribute('class') else "la otra persona"
            output_messages.append(f"Mensaje enviado por {sender}: {message_text}")
        
        return output_messages

    def scroll_to_top(self):
        sleep(2)  # Esperar a que se cargue el scroll
        scrollable_chat_window = self.driver.find_element(By.CLASS_NAME, 'b-chats__scrollbar')
        last_height = self.driver.execute_script("return arguments[0].scrollTop", scrollable_chat_window)
        while True:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - 400", scrollable_chat_window)
            sleep(1)  # Ajustar según la velocidad de carga de la página
            new_height = self.driver.execute_script("return arguments[0].scrollTop", scrollable_chat_window)
            if new_height == last_height:
                break
            last_height = new_height

    def wait_for_new_message(self):
        while True:
            try:
                nuevo_mensaje = self.driver.find_element(By.CLASS_NAME, 'b-chats__item__uread-count')
                nuevo_mensaje.click()
                print("Se ha encontrado un nuevo mensaje y se ha hecho clic en él.")
                break  # Salir del bucle si se encuentra un nuevo mensaje
            except:
                print("No se encontraron nuevos mensajes. Volviendo a buscar...")
                sleep(5)

    def send_message(self, message):
        try:
            message_input = self.driver.find_element(By.XPATH, '//*[@id="new_post_text_input"]')
            message_input.send_keys(message)
            self.driver.find_element(By.XPATH, '//*[@id="make_post_form"]/div[2]/button').click()
        except Exception as e:
            print(f"An error occurred when sending message: {e}")


    def close(self):
        self.driver.quit()
