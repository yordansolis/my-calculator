import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import calendar

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
            'Fecha Inicio': inicio_mes.strftime("%d/%m/%Y"),
            'Fecha Fin': fin_mes.strftime("%d/%m/%Y"),
            'Días': dias_mes,
            'Días del mes': dias_mes_completo,
            'Valor Base': monthly_value if i == len(meses)-1 else '',  # Solo para último pago
            'Valor Pago': pago_mes,
            'Valor Acumulado': pago_acumulado,
            'Porcentaje': round(porcentaje_mes, 2),
            'Porcentaje Acumulado': round(porcentaje_acumulado, 2),
            'Saldo Restante': saldo_restante
        })
    
    return pd.DataFrame(datos_mes)

def main():
    print("SISTEMA DE CÁLCULO DE PAGOS DE CONTRATOS")
    print("(Método de valor mensual fijo con saldo final separado)")
    print("----------------------------------------")
    
    # Obtener valor del contrato
    while True:
        try:
            valor_contrato = float(input("Ingrese el valor total del contrato (en COP, sin puntos ni comas): ").replace('.','').replace(',','.'))
            if valor_contrato <= 0:
                print("El valor del contrato debe ser mayor que cero.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Obtener fechas de inicio y fin
    while True:
        try:
            fecha_inicio_str = input("Ingrese la fecha de inicio del contrato (DD/MM/YYYY): ")
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Formato de fecha incorrecto. Use DD/MM/YYYY.")
    
    while True:
        try:
            fecha_fin_str = input("Ingrese la fecha de finalización del contrato (DD/MM/YYYY): ")
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%d/%m/%Y")
            if fecha_fin <= fecha_inicio:
                print("La fecha de finalización debe ser posterior a la fecha de inicio.")
                continue
            break
        except ValueError:
            print("Formato de fecha incorrecto. Use DD/MM/YYYY.")
    
    # Obtener valor mensual fijo
    while True:
        try:
            valor_mensual = float(input("Ingrese el valor mensual fijo establecido en el contrato (en COP, sin puntos ni comas): ").replace('.','').replace(',','.'))
            if valor_mensual <= 0:
                print("El valor mensual debe ser mayor que cero.")
                continue
            break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Calcular distribución de pagos
    print("\nCalculando distribución de pagos...")
    df_pagos = calcular_pagos_contrato(valor_contrato, fecha_inicio, fecha_fin, valor_mensual)
    
    # Mostrar resultados
    print("\nRESULTADOS:")
    print(f"Valor del contrato: ${valor_contrato:,.0f} COP".replace(',', '.'))
    print(f"Duración: {(fecha_fin - fecha_inicio).days + 1} días")
    print(f"Valor mensual fijo: ${valor_mensual:,.0f} COP".replace(',', '.'))
    print(f"Valor diario de referencia: ${round(valor_mensual / 30, 2):,.2f} COP\n".replace(',', '.'))
    
    print(df_pagos.to_string(index=False))
    
    # Mostrar resumen final
    print("\nRESUMEN FINAL:")
    print(f"Total pagos programados: ${df_pagos['Valor Pago'].sum():,.0f} COP".replace(',', '.'))
    print(f"Valor del contrato: ${valor_contrato:,.0f} COP".replace(',', '.'))
    print(f"Diferencia: ${valor_contrato - df_pagos['Valor Pago'].sum():,.0f} COP".replace(',', '.'))

if __name__ == "__main__":
    main()