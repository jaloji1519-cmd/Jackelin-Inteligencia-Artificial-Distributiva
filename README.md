# JACKELIN — Inteligencia Artificial Distribuida (Python)

Proyecto educativo en Python para abrir en Visual Studio Code, ejecutar localmente y subir a GitHub. Reproduce el módulo de **IA distributiva** de JACKELIN: un coordinador que reparte el trabajo entre agentes especializados de texto, voz, imagen y semaforización, junto con el panel de semaforización nacional y el reporte de arquitectura.

## Alcance y procedencia

Esta es una implementación nueva en Python inspirada en el diseño de la aplicación JACKELIN (chat multimodal, semaforización nacional y arquitectura de IA distribuida). No es una exportación ni una conversión automática del código de la aplicación web, y no incluye sus datos, usuarios, integraciones ni credenciales.

La aplicación usa modelos ya entrenados de un proveedor externo. **No entrena un modelo desde cero, no incluye pesos de modelo y no funciona sin internet.**

La semaforización y su actualización automática son una **demostración local**: los estados se generan con reglas y azar dentro del programa. No existe conexión con entidades oficiales, sensores reales ni datos nacionales en vivo, y el panel no debe usarse para decisiones reales.

Esta entrega se centra en la IA distributiva. No incluye la exportación a PDF ni los demás módulos. La aplicación web actual no se modifica.

El código fue preparado con asistencia de IA. Revísalo, pruébalo y compréndelo antes de presentarlo académicamente.

## 1. Requisitos

- Python 3.10 o superior.
- Visual Studio Code con la extensión Python.
- Internet.
- Una clave API de OpenAI con saldo y acceso a los modelos elegidos. Las llamadas pueden generar cargos; una suscripción de chat no sustituye el saldo de API.
- Git, si vas a subir el proyecto desde la terminal.

No necesitas Node.js, npm, Lovable ni una clave LOVABLE_API_KEY para esta versión.

## 2. Abrir el proyecto en VS Code

1. Descomprime el ZIP.
2. Abre la carpeta JACKELIN_IAD_Python desde Archivo → Abrir carpeta.
3. Abre Terminal → Nueva terminal. La terminal debe estar dentro de esa carpeta.

### Windows: PowerShell

    py -m venv .venv
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    Copy-Item .env.example .env

Estos comandos usan directamente el intérprete del entorno virtual: no necesitan modificar la política de ejecución de PowerShell.

### macOS o Linux

    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt
    cp .env.example .env

## 3. Configurar la clave

Obtén tu propia clave desde https://platform.openai.com/api-keys y configura la facturación y los permisos de tu cuenta si el proveedor lo requiere.

Abre el archivo .env, completa OPENAI_API_KEY y guarda. No incluyas comillas adicionales ni espacios al copiar tu clave. También puedes escribirla en el campo de contraseña de la barra lateral al abrir la aplicación.

**Nunca subas .env, una clave real ni capturas que muestren credenciales.** .gitignore excluye .env; .env.example está vacío y sí se comparte.

Modelos configurados por defecto:

| Agente | Modelo | Función |
| --- | --- | --- |
| Texto | gpt-4o-mini | Conversación y descripción opcional de una ilustración |
| Voz | tts-1, voz nova | Síntesis de la respuesta en MP3 |
| Imagen | gpt-image-1 | Imagen PNG de 1024 × 1024, calidad baja |

La disponibilidad depende de tu cuenta y puede cambiar. Puedes editar los nombres en .env; el modelo de texto debe admitir Chat Completions y salidas JSON Schema, el de voz debe admitir síntesis MP3 y el de imagen debe ser compatible con los parámetros de agentes.py. El acceso a imágenes puede requerir verificación de tu organización.

## 4. Ejecutar

Windows:

    .venv\Scripts\python.exe -m streamlit run app.py

macOS o Linux:

    .venv/bin/python -m streamlit run app.py

Abre http://localhost:8501 en tu computador. Esa es una dirección local, no una publicación pública.

Para depurar con F5: en VS Code ejecuta Python: Select Interpreter, selecciona el intérprete de .venv y después usa la configuración JACKELIN IAD · Python + Streamlit.

## 5. Cómo usar la aplicación

**Pestaña IA Distributiva**

1. Configura la clave API.
2. Escribe una consulta y espera la respuesta del agente de texto.
3. Activa el Agente de voz para generar audio junto con las siguientes respuestas; pulsa reproducir en el control de audio.
4. En cualquier respuesta anterior puedes pulsar 🔊 Generar la voz de esta respuesta para sintetizarla sin repetir la consulta.
5. Con el Agente de imagen activo, pide explícitamente un dibujo o una ilustración: el agente de texto propondrá una descripción y el agente de imagen la dibujará.
6. Bajo cada respuesta aparece qué agentes intervinieron.
7. Pulsa Nueva conversación para vaciar el historial local de la sesión.

**Pestaña Semaforización Nacional**

- Muestra cuántos territorios están estables, en observación o críticos.
- Simular actualización cambia los estados con una regla ponderada de demostración.
- Puedes pulsar cualquier territorio para recorrer manualmente verde → amarillo → rojo.
- Reiniciar todo devuelve todos los territorios a estable.

**Pestaña Arquitectura IAD**

- Resume topología, agentes, comunicación, privacidad, latencia y alcance.
- Incluye el diagrama por capas en texto, útil para copiarlo en el informe.

Ejemplos de consulta:

- ¿Cómo está el monitoreo nacional y qué recomendaciones darías?
- Explica qué es la inteligencia artificial distribuida con un ejemplo cotidiano.
- Dibuja una ilustración de una red de semáforos coordinados por IA.

Si un agente opcional falla, la respuesta escrita se conserva y aparece una advertencia. No se sustituyen las salidas fallidas por demostraciones falsas.

## 6. Los agentes y cómo se distribuyen

    Fase 1   Consulta -> Agente de texto (respuesta escrita + descripción visual)
             El Agente de semaforización aporta el estado nacional como contexto.
    Fase 2   En paralelo: Agente de voz -> MP3      Agente de imagen -> PNG
    Fan-in   El coordinador combina las salidas y las muestra en la conversación

- **Fan-out**: el coordinador reparte el trabajo; cada agente hace una sola tarea.
- **Fan-in**: los resultados se reúnen en un único mensaje con texto, audio e imagen.
- **Degradación elegante**: un fallo de voz o de imagen no borra la respuesta escrita.
- **Contrato JSON**: los agentes intercambian datos estructurados, fáciles de verificar.

Aquí todos los agentes se ejecutan en el mismo proceso de Python para que el proyecto sea sencillo de ejecutar. La separación por módulos permite, más adelante, mover cada agente a su propio servicio.

## 7. Organización del proyecto

    JACKELIN_IAD_Python/
      app.py                      Interfaz, barra lateral y pestañas
      agentes.py                  Agentes y coordinador de la IAD
      semaforizacion.py           Territorios, estados, simulación y resumen
      arquitectura.py             Texto y diagrama del reporte de arquitectura
      vista_chat.py               Pestaña de IA distributiva
      vista_semaforizacion.py     Pestaña de semaforización nacional
      vista_arquitectura.py       Pestaña del reporte de arquitectura
      requirements.txt            Dependencias Python
      .env.example                Configuración sin secretos
      .gitignore                  Exclusiones para Git
      .streamlit/config.toml      Tema oscuro y servidor local
      .vscode/launch.json         Configuración para F5
      .vscode/extensions.json     Extensiones recomendadas
      README.md                   Instalación, arquitectura y entrega

## 8. Arquitectura para explicar al profesor

    Navegador / interfaz Streamlit (servidor Python local)
            |
            v
    CoordinadorIAD: reparte el trabajo y combina resultados
      |-- Agente de texto ---> modelo de lenguaje (texto + descripción visual)
      |-- Agente de voz -----> modelo de voz (MP3 de la respuesta)
      |-- Agente de imagen --> modelo de imagen (PNG de la descripción)
      |-- Agente de semaforización -> estado nacional de demostración
            |
            v
    Sesión local: historial, estados y resultados

El coordinador ejecuta primero el agente de texto porque los demás dependen de su salida; después lanza voz e imagen en paralelo con hilos. El estado de conversación vive en la sesión de Streamlit: no hay base de datos, sistema de usuarios ni guardado permanente. Reiniciar el servidor o perder la sesión borra el historial.

## 9. Subir a GitHub

1. Crea un repositorio nuevo vacío en tu cuenta de GitHub. No añadas un README remoto si vas a usar los comandos siguientes.
2. En la terminal del proyecto ejecuta:

    git init -b main
    git add .
    git status
    git commit -m "Entrega JACKELIN: IA distributiva en Python"
    git remote add origin URL_DE_TU_REPOSITORIO
    git push -u origin main

Reemplaza URL_DE_TU_REPOSITORIO por la dirección real de tu repositorio; no uses ese texto literalmente. Git puede pedirte iniciar sesión en tu propia cuenta. Si aún no configuraste tu identidad de Git, configura tu nombre y correo antes del primer commit.

Antes del commit verifica con git status que NO aparezcan .env ni .venv. Si una clave se publica por accidente, revócala en el proveedor; borrar el archivo del último commit no la elimina del historial.

GitHub aloja el código. GitHub Pages no ejecuta el servidor Python. Para esta entrega, tu profesor puede descargar el repositorio o el ZIP y ejecutarlo localmente siguiendo este README, con su propia clave.

## 10. Entrega académica

- Comparte el ZIP original sin .env o el enlace real de tu repositorio.
- Completa tus datos: estudiante, asignatura, profesor y fecha, según las indicaciones de tu institución.
- Explica el reparto de trabajo entre agentes, el papel del coordinador y qué modelos externos se usan.
- Aclara que la semaforización es una demostración local y que no hay datos oficiales.
- Si se exige entrenamiento propio o funcionamiento completamente local, esta solución basada en API no cumple ese requisito sin cambios adicionales.

## 11. Límites y problemas comunes

- Clave no válida: revisa OPENAI_API_KEY; no se usa LOVABLE_API_KEY.
- Sin saldo o límite de uso: revisa facturación y límites de la API.
- Imagen bloqueada: revisa permisos, verificación de organización y acceso al modelo.
- Conexión fallida: revisa internet, cortafuegos y disponibilidad del proveedor.
- Puerto ocupado: ejecuta el comando de Streamlit añadiendo --server.port 8502.
- Módulo no encontrado: instala requirements.txt usando el mismo intérprete con el que ejecutas la app.
- La voz admite hasta 4096 caracteres por respuesta; la interfaz avisa cuando el audio es parcial.
- Las respuestas pueden ser incorrectas: verifica los datos antes de usarlos.
- Los mensajes, las respuestas para voz y las descripciones de imagen se envían al proveedor. No ingreses información sensible.

Este paquete contiene código fuente y configuración sin credenciales; no contiene dependencias instaladas. Las llamadas reales requieren la configuración descrita y no se han ejecutado con una clave propia dentro de esta entrega.
