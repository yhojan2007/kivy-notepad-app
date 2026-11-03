# 📝 Notepad — Aplicación de Notas con Estructuras de Datos Personalizadas

Aplicación de notas de escritorio con interfaz gráfica desarrollada en **Python** con el framework **Kivy**, que funciona como proyecto académico para practicar **Estructuras de Datos y Algoritmos**.

En lugar de depender de las colecciones de alto nivel de Python o de una base de datos externa pesada para la lógica central, la aplicación implementa **TDA personalizados desde cero**: una **Lista Doblemente Enlazada** para la organización de notas y **Pilas** para el historial de deshacer/rehacer. La persistencia de las notas se realiza con **SQLite**.

## ✨ Características Principales

1. **Organización de Notas (Move-To-Front / `ListaNota`):**
   Las notas se gestionan mediante una Lista Doblemente Enlazada personalizada.
   Al crear o editar una nota, esta se desplaza automáticamente al inicio (`cabeza`) de la lista según su marca de modificación, garantizando que las notas más recientes aparezcan siempre en la parte superior de la interfaz, sin algoritmos de ordenamiento pesados.

2. **Sistema de Deshacer y Rehacer (`NotaEditor` / `PilaHistorial`):**
   El historial de edición de texto se gestiona mediante una pila construida con una Lista Doblemente Enlazada, utilizando los punteros explícitos `fondo` (base) y `tope` (cima).
   Soporta seguimiento en tiempo real del historial con un límite máximo de tamaño (`max_history = 100`) y eliminación automática de las entradas más antiguas cuando la pila se llena.

3. **Persistencia (`NotaRepositorio`):**
   Las notas se guardan en una base de datos **SQLite** (`notas.db`) con título, contenido y fecha de modificación, en la carpeta de datos privada de la aplicación (`user_data_dir`).

4. **Búsqueda por título (`Trie` / `IndiceTitulos`):**
   Se implementa un índice de prefijos (Trie) sobre palabras tokenizadas (minúsculas y sin tildes). La coincidencia por título usa todas las palabras de la consulta y la pantalla de inicio incluye sugerencias de autocompletado (hasta 4 coincidencias).

## 📂 Estructura del Proyecto

```text
Notepad/
├── app/
│   ├── data/
│   │   └── nota_repositorio.py        # Persistencia en SQLite
│   ├── models/
│   │   ├── busqueda_titulos.py        # Trie, tokenización e índice de títulos
│   │   ├── lista_nota.py              # Lista doblemente enlazada (Move-To-Front)
│   │   ├── nodo_nota.py               # Nodo de la lista de notas
│   │   └── nota_editor.py             # Pilas para el historial undo/redo
│   └── screens/
│       ├── home_screen.py             # Lista y buscador de notas
│       └── editor_screen.py           # Editor, historial y menú
├── kv/
│   ├── theme.kv                       # Tema y widgets compartidos
│   ├── home.kv                        # Diseño de la pantalla principal
│   └── editor.kv                      # Diseño del editor
├── assets/
│   └── fonts/
│       └── MaterialIcons-Regular.ttf # Fuente de iconos
├── main.py                            # Punto de entrada de la aplicación
├── buildozer.spec                     # Configuración para Android
├── dockerfile                         # Imagen de Buildozer para compilar el APK
└── requirements.txt
```

## 🚀 Primeros Pasos

### Prerrequisitos

- **Python 3.10 o superior**.
- **pip**.

### Instalación y ejecución

1. Navega hasta la carpeta raíz del proyecto.
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # En Windows (PowerShell/CMD):
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias (Kivy y sus dependencias de plataforma):

   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

## 💻 Uso

1. En la pantalla principal se listan las notas desde la más reciente a la más antigua; se escribe en el buscador para filtrar por título o ver sugerencias de autocompletado.
2. El botón flotante (`+`) crea una nueva nota.
3. En el editor: las flechas de la barra superior accionan deshacer / rehacer; el menú de tres puntos permite guardar o eliminar la nota.
4. Al guardar una nota editada, esta se reordena automáticamente al inicio de la lista.

## 📱 Despliegue

- **Android:** el repositorio incluye `buildozer.spec` y un `dockerfile` basado en la imagen `kivy/buildozer` para compilar el APK. El spec define permisos de `INTERNET`, orientación vertical, SDK 33, versión mínima API 21 y arquitecturas `arm64-v8a` / `armeabi-v7a`.
- **Escritorio:** la app se ejecuta directamente con `python main.py` sobre el entorno virtual.

## 👨‍💻 Propósito Académico

Este proyecto demuestra la aplicación práctica de punteros de memoria a bajo nivel (`anterior` y `siguiente`), Tipos de Datos Abstractos (TDA) personalizados y el manejo de eventos en interfaces gráficas, sin depender de librerías externas o frameworks de bases de datos para la lógica en memoria.

## [COMPLETAR: objetivo de negocio o tema específico de la materia]

---

## Pendientes de documentación

Marcadores `[COMPLETAR]` que faltan por definir o verificar en el repositorio:

- [ ] Objetivo de negocio o pregunta de investigación específica de la asignatura.
- [ ] Autor(es) / equipo y fecha de entrega.
- [ ] Licencia del proyecto (no se encontró archivo `LICENSE`).
- [ ] Capturas de pantalla de la interfaz (no se encontraron en el repo).
- [ ] URL o instrucciones de despliegue demo.
- [ ] Confirmar si `requirements.txt` debe conservarse como lockfile o convertirse a versiones mínimas.
