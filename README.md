# 📝 Aplicación de Notas - Estructuras de Datos Personalizadas (Python & Kivy)

Una aplicación de bloc de notas de escritorio desarrollada como proyecto académico para practicar **Estructuras de Datos y Algoritmos** utilizando Python y el framework **Kivy**. En lugar de depender de colecciones de alto nivel predeterminadas o bases de datos externas pesadas para la lógica central, esta aplicación implementa **Listas Doblemente Enlazadas** personalizadas desde cero para gestionar el historial de notas, el ordenamiento dinámico y el control de estados.

## ✨ Características Principales

1. **Organización de Notas (Move-To-Front / `ListaNota`):**
   * Las notas se gestionan mediante una Lista Doblemente Enlazada personalizada.
   * Cada vez que se crea o edita una nota, esta se desplaza automáticamente al inicio (`cabeza`) de la lista según su marca de tiempo de modificación, garantizando que las notas más recientes aparezcan siempre en la parte superior de la interfaz sin necesidad de algoritmos de ordenamiento pesados.

2. **Sistema de Deshacer y Rehacer (`NotaEditor` / `PilaHistorial`):**
   * El historial de edición de texto se gestiona mediante estructuras de Pila independientes construidas con Listas Doblemente Enlazadas, utilizando los punteros explícitos `fondo` (base) y `tope` (cima).
   * Soporta seguimiento en tiempo real del historial con un límite máximo de tamaño (`max_size`) y eliminación automática de las entradas más antiguas cuando la pila se llena.

3. **Interfaz Gráfica de Usuario (Kivy):**
   * Diseño moderno implementado a través de Pantallas de Kivy (`HomeScreen` y `EditorScreen`) combinadas con archivos modulares de diseño `.kv`.

## 📂 Estructura del Proyecto

```text
Notepad/
├── app/
│   ├── models/
│   │   ├── nodo_nota.py         # Estructura de nodo para las notas
│   │   ├── lista_nota.py        # Lista doblemente enlazada para notas (Move-To-Front)
│   │   └── nota_editor.py       # Estructura de pila para el historial Undo/Redo
│   └── screens/
│       ├── home_screen.py       # Controlador de vista principal
│       └── editor_screen.py     # Controlador de vista de edición
├── kv/
│   ├── home.kv                  # Diseño de interfaz para la pantalla principal
│   └── editor.kv                # Diseño de interfaz para la pantalla del editor
├── main.py                      # Punto de entrada de la aplicación
└── README.md                    # Documentación del proyecto
```

## 🚀 Primeros Pasos

### Prerrequisitos
Asegúrate de tener instalado **Python 3.8+** en tu sistema.

### Instalación y Ejecución
1. Navega hasta la carpeta raíz de tu proyecto.
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows (PowerShell/CMD):
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. Instala el framework Kivy:
   ```bash
   pip install kivy
   ```
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## 👨‍💻 Propósito Académico
Este proyecto demuestra la aplicación práctica de punteros de memoria a bajo nivel (`anterior` y `siguiente`), Tipos de Datos Abstractos (TDA) personalizados y el manejo de eventos en interfaces gráficas, sin depender de librerías externas o frameworks de bases de datos para la persistencia en memoria.