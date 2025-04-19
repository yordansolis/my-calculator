from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import json

app = Flask(__name__)

def calcular_pagos_contrato(contract_value, start_date, end_date, monthly_value):
    """
    Calcula la distribución de pagos con las siguientes reglas:
    1. Meses completos: valor mensual exacto
    2. Meses parciales: prorrateo diario exacto
    3. Último pago: valor base o saldo restante (lo que sea menor)
    """
    meses = []
    fecha_actual = start_date
    while fecha_actual <= end_date:
        meses.append((fecha_actual.year, fecha_actual.month))
        siguiente_mes = fecha_actual.replace(day=28) + datetime.timedelta(days=4)
        fecha_actual = siguiente_mes.replace(day=1)
    
    datos_mes = []
    pago_acumulado = 0
    porcentaje_acumulado = 0
    
    for i, (year, month) in enumerate(meses):
        # Determinar período
        inicio_mes = start_date if i == 0 else datetime.datetime(year, month, 1)
        fin_mes = end_date if i == len(meses)-1 else datetime.datetime(year, month, calendar.monthrange(year, month)[1])
        
        dias_mes = (fin_mes - inicio_mes).days + 1
        dias_mes_completo = calendar.monthrange(year, month)[1]
        
        # Cálculo del pago
        if i == len(meses)-1:  # ÚLTIMO PAGO
            pago_mes = min(monthly_value, contract_value - pago_acumulado)
        else:
            if inicio_mes.day == 1 and fin_mes.day == dias_mes_completo:
                pago_mes = monthly_value  # Mes completo
            else:
                pago_mes = round((monthly_value / dias_mes_completo) * dias_mes)  # Prorrateo
        
        # Calcular porcentajes
        porcentaje_mes = (pago_mes / contract_value) * 100
        pago_acumulado += pago_mes
        porcentaje_acumulado += porcentaje_mes
        
        saldo_restante = max(0, contract_value - pago_acumulado)  # No negativo
        
        datos_mes.append({
            'Mes': f'MES {i+1}',
            'Pago': f'PAGO {i+1}',
            'Fecha_Inicio': inicio_mes.strftime("%d/%m/%Y"),
            'Fecha_Fin': fin_mes.strftime("%d/%m/%Y"),
            'Dias': dias_mes,
            'Dias_del_mes': dias_mes_completo,
            'Valor_Base': monthly_value if i == len(meses)-1 else None,  # Solo para último pago
            'Valor_Pago': pago_mes,
            'Valor_Acumulado': pago_acumulado,
            'Porcentaje': round(porcentaje_mes, 2),
            'Porcentaje_Acumulado': round(porcentaje_acumulado, 2),
            'Saldo_Restante': saldo_restante
        })
    
    return datos_mes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    
    try:
        valor_contrato = float(data.get('valor_contrato').replace('.', '').replace(',', '.'))
        fecha_inicio = datetime.datetime.strptime(data.get('fecha_inicio'), "%d/%m/%Y")
        fecha_fin = datetime.datetime.strptime(data.get('fecha_fin'), "%d/%m/%Y")
        valor_mensual = float(data.get('valor_mensual').replace('.', '').replace(',', '.'))
        
        if fecha_fin <= fecha_inicio:
            return jsonify({'error': 'La fecha de finalización debe ser posterior a la fecha de inicio.'}), 400
        
        pagos = calcular_pagos_contrato(valor_contrato, fecha_inicio, fecha_fin, valor_mensual)
        
        # Convertir los resultados a formato JSON seguro
        for item in pagos:
            for key, value in item.items():
                if isinstance(value, float):
                    item[key] = round(value, 2)
        
        # Calcular resumen
        total_pagos = sum(item['Valor_Pago'] for item in pagos)
        diferencia = valor_contrato - total_pagos
        
        resumen = {
            'total_pagos': total_pagos,
            'valor_contrato': valor_contrato,
            'diferencia': diferencia,
            'duracion_dias': (fecha_fin - fecha_inicio).days + 1,
            'valor_diario': round(valor_mensual / 30, 2)
        }
        
        return jsonify({
            'pagos': pagos,
            'resumen': resumen
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 