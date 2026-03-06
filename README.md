# 📊 Aplicación de Análisis de Movimientos con Streamlit

Esta es una aplicación interactiva desarrollada con **Streamlit** y **Pandas** que permite analizar movimientos financieros a partir de dos archivos Excel (`.xlsx`). La interfaz permite visualizar filtros por fechas, cuentas, detectar anomalías (outliers), y generar gráficas de débitos y créditos diarios.

---

## 📁 Estructura del Proyecto
```pgsql
📦 tu_proyecto/
├── prueba3.py # Archivo principal de la app Streamlit
│ ├── data.xlsx # Primer archivo Excel
│ └── data_prueba.xlsx # Segundo archivo Excel
├── README.md # Este archivo
```
yaml
Copy
Edit

---

## 🚀 Cómo ejecutar la aplicación

### 1. Crear un entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows
```
2. Instalar dependencias
bash
Copy
Edit
pip install streamlit pandas openpyxl
Se necesita openpyxl para leer archivos .xlsx.

3. Colocar tus archivos Excel
Guarda los archivos en la carpeta data/:

bash
Copy
Edit
data/movimientos.xlsx
data/cuentas.xlsx
Asegúrate de que el código en app.py acceda a ellos correctamente.

4. Ejecutar la aplicación
bash
Copy
Edit
streamlit run app.py
Esto abrirá la app en tu navegador por defecto: http://localhost:8501

🧰 Herramientas utilizadas
* Streamlit

* Pandas

* Openpyxl

📝 Notas
Verifica que tus archivos Excel tengan las columnas esperadas (fecha, debitos, creditos, etc.).

Si ocurre un error, revisa el archivo app.py y el formato de los archivos Excel.