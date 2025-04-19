# Calculadora de Pagos de Contratos

Esta aplicación web permite calcular la distribución de pagos para contratos con valor mensual fijo, siguiendo las siguientes reglas:

1. Meses completos: valor mensual exacto
2. Meses parciales: prorrateo diario exacto
3. Último pago: valor base o saldo restante (lo que sea menor)

## Características

- Interfaz fácil de usar y moderna
- Cálculo automático de pagos mensuales
- Visualización clara de la distribución de pagos
- Formato de moneda colombiana (COP)
- Selector de fechas intuitivo
- Diseño responsive para móviles y escritorio

## Requisitos

- Python 3.7+
- Flask
- Pandas
- Python-dateutil

## Instalación

1. Clona este repositorio:

```
git clone https://github.com/tu-usuario/calculadora-pagos-contratos.git
cd calculadora-pagos-contratos
```

2. Crea un entorno virtual (opcional pero recomendado):

```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:

```
pip install -r requirements.txt
```

## Uso

1. Inicia la aplicación:

```
python app.py
```

2. Abre tu navegador y visita:

```
http://localhost:5000
```

3. Introduce los siguientes datos en el formulario:

   - Valor total del contrato (en COP)
   - Fecha de inicio del contrato (DD/MM/YYYY)
   - Fecha de finalización del contrato (DD/MM/YYYY)
   - Valor mensual fijo establecido en el contrato (en COP)

4. Haz clic en "Calcular Pagos" para ver los resultados.

## Personalización

Si deseas personalizar la apariencia de la aplicación, puedes modificar los archivos en:

- `static/css/styles.css` para cambiar los estilos
- `templates/index.html` para modificar la estructura HTML
- `static/js/script.js` para ajustar la lógica del frontend

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
