### OnlyFansAPI

Esta clase proporciona métodos para interactuar con la plataforma OnlyFans. Permite automatizar acciones como el inicio de sesión, navegación a través de mensajes y envío de respuestas.

#### Métodos

**`__init__(self, username, password)`**

Constructor de la clase que inicializa la API con las credenciales del usuario.

- **Parámetros:**
  - `username`: String. Nombre de usuario de OnlyFans.
  - `password`: String. Contraseña de OnlyFans.

**`login(self)`**

Inicia sesión en OnlyFans utilizando las credenciales proporcionadas en el constructor.

- **Excepciones:**
  - Lanza una excepción si ocurre un error durante el inicio de sesión.

**`close(self)`**

Cierra la sesión y el navegador para liberar recursos.

**`navigate_to_messages(self)`**

Navega a la sección de mensajes de OnlyFans tras iniciar sesión.

- **Excepciones:**
  - Lanza una excepción si no se puede acceder a la sección de mensajes.

**`wait_for_new_message(self)`**

Espera hasta que llegue un nuevo mensaje y lo procesa automáticamente.

- **Descripción:**
  - Permanece en espera activa hasta que detecta un nuevo mensaje entrante.

**`fetch_all_messages(self)`**

Recupera todos los mensajes del chat actual.

- **Retorno:**
  - List of String: Lista de mensajes del chat.

**`fetch_latest_messages(self)`**

Espera un breve periodo y recupera los últimos mensajes enviados o recibidos.

- **Parámetros:**
  - `last_message_time`: Int (opcional). Número de segundos a esperar antes de recopilar los mensajes. Por defecto es 5 segundos.

- **Retorno:**
  - List of String: Lista de los últimos mensajes del chat.

**`send_message(self, message)`**

Envía un mensaje al chat actual.

- **Parámetros:**
  - `message`: String. El mensaje a enviar.

### Ejemplo de Uso

```python
def main():
    # Configura tus credenciales
    username = 'tu_usuario'
    password = 'tu_contraseña'

    # Instancia la API
    api = OnlyFansAPI(username, password)

    # Iniciar sesión
    api.login()

    # Esperar y navegar a los mensajes
    api.navigate_to_messages()

    # Esperar a que llegue un nuevo mensaje
    api.wait_for_new_message()

    # Obtener todos los mensajes
    all_messages = api.fetch_all_messages()
    print("Todos los mensajes:")
    for message in all_messages:
        print(message)

    # Obtener los últimos mensajes
    latest_messages = api.fetch_latest_messages()
    print("\nÚltimos mensajes:")
    for message in latest_messages:
        print(message)

    # Cerrar la sesión
    api.close()

if __name__ == "__main__":
    main()
```
