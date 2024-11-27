
---

# **InfraGest**
InfraGest es una aplicación para analizar el comportamiento de la infraestructura inteligente de una ciudad. Proyecto para Base de Datos No Relacionales.

---

## **Configuración Inicial**

### **1. Preparar el Contenedor de MongoDB**
Ejecuta los siguientes comandos en tu terminal:

1. Descargar y ejecutar el contenedor de MongoDB:
   ```bash
   docker run -d --name [name] -p 27017:27017 mongo
   ```
2. Verificar que esté corriendo:
   ```bash
   docker ps
   ```

---

### **2. Configurar el Entorno Virtual**
1. Crear y activar el entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Para Windows
   ```
2. Instalar las dependencias requeridas (incluidas en `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```

---

## **Inserción de Datos de Prueba**

Se definieron las siguientes colecciones en MongoDB:

- **Edificios**
- **Calles**
- **Parques**

Datos de prueba insertados exitosamente. Puedes verificar las colecciones en MongoDB Compass tras ejecutar `insert_data.py`.

---

## **Avances**

- Configuración de MongoDB con Docker.
- Conexión a MongoDB con PyMongo (`db_connection.py`).
- Inserción de datos iniciales en las colecciones.

---

## **Ejecución**

1. Ejecuta el script de conexión para verificar:
   ```bash
   python db_connection.py
   ```
2. Inserta los datos de prueba:
   ```bash
   python insert_data.py
   ```

---

### **Notas**
Asegúrate de que MongoDB esté corriendo antes de ejecutar los scripts. Todos los datos geoespaciales están en formato GeoJSON.
