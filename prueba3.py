import streamlit as st
import pandas as pd
import pandasql as ps
import plotly.express as px

st.set_page_config(page_title="My App", layout="wide")



def primero(df_movimientos, df_saldos):

        st.markdown("## Movimientos")
        st.dataframe(df_movimientos)

        st.markdown("## Débitos y Créditos por Día")
        resumen_diario = df_movimientos.groupby("fecha")[["debitos", "creditos"]].sum().reset_index()
        st.dataframe(resumen_diario)

        fig = px.line(resumen_diario, x="fecha", y=["debitos", "creditos"], markers=True, title="Tendencia de Débitos y Créditos por Día")
        st.plotly_chart(fig)



def segundo(df_movimientos, df_saldos):

        st.header("Saldos")

        # Seleccionar fecha
        opcion_mov_fecha = st.selectbox('Fecha', sorted(df_movimientos['fecha'].unique().tolist()))
        df_filtrado = df_movimientos[df_movimientos['fecha'] == opcion_mov_fecha]

        # Seleccionar negocio
        opcion_mov_negocio = st.selectbox("Negocio", sorted(df_filtrado["negocio"].unique()))
        df_filtrado = df_filtrado[df_filtrado['negocio'] == opcion_mov_negocio]

        # Seleccionar cuenta
        opcion_mov_cuenta = st.selectbox("Cuenta", sorted(df_filtrado["cuenta"].unique()))
        df_filtrado = df_filtrado[df_filtrado['cuenta'] == opcion_mov_cuenta]

        # Seleccionar tercero
        opcion_mov_tercero = st.selectbox("Tercero", sorted(df_filtrado["tercero"].unique()))
        df_filtrado = df_filtrado[df_filtrado['tercero'] == opcion_mov_tercero]

        st.markdown("### Saldos (Tabla movimientos)")

        # Agrupar y sumar débitos y créditos
        agrupado = df_filtrado.groupby(["negocio", "cuenta", "tercero", "fecha"])[["debitos", "creditos"]].sum().reset_index()

        # Calcular el saldo (debitos - creditos)
        agrupado["saldo"] = agrupado["debitos"] - agrupado["creditos"]

        # Ver el resultado
        st.dataframe(agrupado)

        st.markdown("### Saldos (Tabla saldos)")

        df_filtrado2 = df_saldos[
            (df_saldos['fecha'] == opcion_mov_fecha) &
            (df_saldos['negocio'] == opcion_mov_negocio) &
            (df_saldos['cuenta'] == opcion_mov_cuenta) &
            (df_saldos['tercero'] == opcion_mov_tercero)
        ]

        # Agrupar saldos
        agrupado2 = df_filtrado2.groupby(["negocio", "cuenta", "tercero", "fecha"])["saldo"].sum().reset_index()

        # Ver el resultado
        st.dataframe(agrupado2)






def tercero(df_movimientos, df_saldos):

        # Crear DataFrame filtrado por fecha
        opcion_mov_fecha = st.selectbox('Fecha', sorted(df_movimientos['fecha'].unique().tolist()))
        df_filtrado = df_movimientos[df_movimientos['fecha'] == opcion_mov_fecha]

        # Agrupar y transformar
        df_resumen = df_filtrado.groupby("nombre_cuenta")[["debitos", "creditos"]].sum().reset_index()
        df_long = df_resumen.melt(id_vars="nombre_cuenta", value_vars=["debitos", "creditos"],
                                var_name="Tipo", value_name="Valor")
        df_long = df_long.sort_values(by="nombre_cuenta")

        # Función de estilo para resaltar según el tipo
        def resaltar_tipo(row):
            color = "#6AA4CA" if row["Tipo"] == "debitos" else "#405796F4"
            return ['background-color: {}'.format(color)] * len(row)

        # Mostrar con estilo
        st.dataframe(df_long.style.apply(resaltar_tipo, axis=1))


        fig = px.bar(df_long, x="nombre_cuenta", y="Valor", color="Tipo", barmode="group",
                title=f"Débitos y Créditos por Cuenta - {opcion_mov_fecha}")
        
        st.plotly_chart(fig)







def cuarto(df_movimientos, df_saldos):

        opcion_mov_nombreCuenta = st.selectbox('Nombre cuenta', sorted(df_movimientos['nombre_cuenta'].unique().tolist()))
        df_filtrado = df_movimientos[df_movimientos['nombre_cuenta'] == opcion_mov_nombreCuenta]

        resumen = pd.DataFrame({
            "Tipo": ["Débito", "Crédito"],
            "Cantidad de movimientos": [(df_filtrado["debitos"] > 0).sum(), (df_filtrado["creditos"] > 0).sum()],
            "Total acumulado": [df_filtrado["debitos"].sum(), df_filtrado["creditos"].sum()]
        })
        
        st.dataframe(resumen)

        col1, col2 = st.columns(2)
        col1.metric(label="Numero de Debitos", value=f'{resumen.iat[0, 1]}')
        col2.metric(label="Valor total Debitos", value=f'${resumen.iat[0, 2]:,.2f}')
        col1.metric(label="Numero de Creditos", value=f'{resumen.iat[1, 1]}')
        col2.metric(label="Valor total Creditos", value=f'${resumen.iat[1, 2]:,.2f}')



        # Filtrar débitos y créditos
        df_debitos = df_filtrado[df_filtrado["debitos"] > 0]
        df_creditos = df_filtrado[df_filtrado["creditos"] > 0]

        # Agrupar por fecha
        debitos_por_dia = df_debitos.groupby(df_debitos["fecha"].dt.date).size().reset_index(name="débitos")
        creditos_por_dia = df_creditos.groupby(df_creditos["fecha"].dt.date).size().reset_index(name="créditos")

        # Unir débitos y créditos por fecha
        df_merged = pd.merge(debitos_por_dia, creditos_por_dia, on="fecha", how="outer").fillna(0)

        # Convertir a formato largo (long) para plotly
        df_long = df_merged.melt(id_vars="fecha", value_vars=["débitos", "créditos"], 
                                var_name="tipo", value_name="cantidad")

        # Graficar con plotly
        fig = px.bar(df_long, x="fecha", y="cantidad", color="tipo", barmode="group",
                    title=f"Débitos y Créditos diarios - {opcion_mov_nombreCuenta}",
                    labels={"fecha": "Fecha", "cantidad": "Cantidad de movimientos", "tipo": "Tipo"})

        st.plotly_chart(fig)

def quinto(df_movimientos, df_saldos):

        df_debitos = df_movimientos[df_movimientos["debitos"] > 0].copy()

        # Calcular cuartiles y rango intercuartílico
        q1 = df_debitos["debitos"].quantile(0.25)
        q3 = df_debitos["debitos"].quantile(0.75)
        iqr = q3 - q1

        # Limpiar outliers extremos
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        anomalías = df_debitos[
            (df_debitos["debitos"] < limite_inferior) |
            (df_debitos["debitos"] > limite_superior)
        ]

        # Función de estilo para marcar valores fuera de los límites
        def resaltar_anomalias(val):
            if val > limite_superior:
                return 'background-color: #8B0000; color: white'  # Rojo oscuro
            elif val < limite_inferior:
                return 'background-color: #1E90FF; color: white'  # Azul brillante
            else:
                return ''

        # Aplicar el estilo solo a la columna "debitos"
        styled_anomalias = anomalías.style.applymap(resaltar_anomalias, subset=["debitos"])

        # Mostrar tabla estilizada en Streamlit
        st.subheader("Débitos anómalos detectados (outliers)")
        st.dataframe(styled_anomalias)

        df_debitos = df_movimientos[df_movimientos["creditos"] > 0].copy()

        # Calcular cuartiles y rango intercuartílico
        q1 = df_debitos["creditos"].quantile(0.25)
        q3 = df_debitos["creditos"].quantile(0.75)
        iqr = q3 - q1

        # Limpiar outliers extremos
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        anomalías = df_debitos[
            (df_debitos["creditos"] < limite_inferior) |
            (df_debitos["creditos"] > limite_superior)
        ]

        # Función de estilo para marcar valores fuera de los límites
        def resaltar_anomalias(val):
            if val > limite_superior:
                return 'background-color: #8B0000; color: white'  # Rojo oscuro
            elif val < limite_inferior:
                return 'background-color: #1E90FF; color: white'  # Azul brillante
            else:
                return ''

        # Aplicar el estilo solo a la columna "creditos"
        styled_anomalias = anomalías.style.applymap(resaltar_anomalias, subset=["creditos"])

        # Mostrar tabla estilizada en Streamlit
        st.subheader("Creditos anómalos detectados (outliers)")
        st.dataframe(styled_anomalias)

        movimientos_por_dia = df_movimientos.groupby(df_movimientos["fecha"].dt.date).size()
        umbral_alto = movimientos_por_dia.mean() + 2 * movimientos_por_dia.std()

        fechas_con_picos = movimientos_por_dia[movimientos_por_dia > umbral_alto]
        st.subheader("Fecha con el mayor pico de movimiento")


        # Convertir Series a DataFrame para obtener filas y columnas
        fechas_con_picos_df = fechas_con_picos.reset_index(name="cantidad_movimientos")

        # Mostrar en Streamlit
        st.dataframe(fechas_con_picos_df)

        # Usar valores del DataFrame convertido
        col1, col2 = st.columns(2)
        col1.metric(label="Fecha", value=f'{fechas_con_picos_df.iat[0,0]}')
        col2.metric(label="Número de Débitos", value=f'{fechas_con_picos_df.iat[0,1]}')

        resumen = df_movimientos.groupby("nombre_cuenta")[["debitos", "creditos"]].sum()
        solo_debito = resumen[(resumen["creditos"] == 0) & (resumen["debitos"] > 0)]
        solo_credito = resumen[(resumen["debitos"] == 0) & (resumen["creditos"] > 0)]

        st.subheader("Cuentas que solo tienen débitos")
        st.dataframe(solo_debito)

        st.subheader("Cuentas que solo tienen créditos")
        st.dataframe(solo_credito)

        df_debitos_dia = df_movimientos.groupby(df_movimientos["fecha"].dt.date)["debitos"].sum().reset_index()
        media = df_debitos_dia["debitos"].mean()
        umbral = media + 2 * df_debitos_dia["debitos"].std()

        fig = px.line(df_debitos_dia, x="fecha", y="debitos", title="Tendencia de débitos diarios")
        fig.add_hline(y=umbral, line_dash="dash", line_color="red", annotation_text="Umbral alto")
        st.plotly_chart(fig)

    

def sexto(df_movimientos, df_saldos):

        st.write("Elige una columna pala eje X")
        eje_x = st.selectbox("Eje X", df_movimientos.columns)

        st.write("Elige una columna pala eje Y")
        eje_y = st.selectbox("Eje Y", df_movimientos.columns)

        if st.button("Crear Grafico"):
            fig = px.bar(df_movimientos, x=eje_x, y=eje_y)
            st.plotly_chart(fig)


def septimo():


    
        try:
            df_movimientos =  pd.read_excel("data_prueba.xlsx", sheet_name="movimientos", dtype={"cuenta": str})
            df_saldos =  pd.read_excel("data_prueba.xlsx", sheet_name="saldos", dtype={"cuenta": str})
            st.success("Los archivos se leyeron correctamente")

        except Exception as e:
            st.error("Error al leer el archivo "+ {str(e)})


        st.markdown("## movimientos")
        st.write(df_movimientos)

        st.markdown("## movimientos_ajustados")
        consulta = "SELECT * FROM df_movimientos WHERE NOT (documento = '98' AND debitos > 0)"
        movimientos_ajustados = ps.sqldf(consulta)
        consulta = '''
        SELECT *,
            CASE 
                WHEN comentario like '%INVE%' AND fecha <= 20241215 THEN debitos * 50 
                WHEN documento IN ('PRO','TCEP','RU') AND fecha > 20241215 THEN debitos / 100 
                ELSE debitos
            END AS debitos_ajustado
        FROM movimientos_ajustados
        '''
        movimientos_ajustados = ps.sqldf(consulta)
        consulta = '''
        SELECT *,
            CASE 
                WHEN CAST(cuenta AS TEXT) like '1%' THEN creditos * 500
                WHEN CAST(cuenta AS TEXT) like '8%' THEN creditos / 800 
                ELSE creditos
            END AS creditos_ajustado
        FROM movimientos_ajustados
        '''
        movimientos_ajustados = ps.sqldf(consulta)
        st.write(movimientos_ajustados)




        st.markdown("## Promedios")
        promedio1=movimientos_ajustados["debitos_ajustado"].mean()
        promedio2=movimientos_ajustados["creditos_ajustado"].mean()
        st.markdown(f'**Promedio debitos_ajustado:** ${promedio1:,.2f}')
        st.markdown(f'**Promedio creditos_ajustado:** ${promedio2:,.2f}')




        st.markdown("## movimientos_agrupados")
        consulta = '''
        SELECT negocio, cuenta, tercero , fecha, SUM(debitos) AS debitos_totales, SUM(creditos) AS créditos_totales  FROM movimientos_ajustados
        GROUP BY negocio, cuenta, tercero , fecha
        '''
        movimientos_agrupados = ps.sqldf(consulta)
        st.write(movimientos_agrupados)

        st.markdown("## movimientos_agrupados_uno")
        consulta = '''
        SELECT * FROM movimientos_agrupados WHERE negocio = 14155 AND cuenta ='130205007323' AND tercero = 2006278 AND fecha = 20241203
        '''
        movimientos_agrupados_uno = ps.sqldf(consulta)
        st.write(movimientos_agrupados_uno)


        
        
        st.markdown("## Acumulado debitos y creditos totales")
        movimientos_agrupados = movimientos_agrupados.sort_values(by=["negocio", "cuenta", "tercero", "fecha"])
        # Calcular acumulados por grupo
        movimientos_agrupados["debitos_acumulados"] = movimientos_agrupados.groupby(["negocio", "cuenta", "tercero"])["debitos_totales"].cumsum()
        movimientos_agrupados["creditos_acumulados"] = movimientos_agrupados.groupby(["negocio", "cuenta", "tercero"])["créditos_totales"].cumsum()
        st.write(movimientos_agrupados)




        st.markdown("## Valor maximo")
        valor_maximo = movimientos_agrupados["creditos_acumulados"].max()
        st.markdown(f'El valor más alto de créditos acumulados es: ${valor_maximo:,.2f}')
        fila_maxima = movimientos_agrupados[movimientos_agrupados["creditos_acumulados"] == valor_maximo]
        st.write(fila_maxima)




        st.markdown("## Cruce de tablas")
        cruce_tablas = pd.merge(movimientos_agrupados, df_saldos,  on=["negocio", "cuenta", "tercero","fecha"],    how="inner")
        st.write(cruce_tablas)




        registros_14155 = cruce_tablas[cruce_tablas["negocio"] == 14155]
        cantidad = len(registros_14155)
        st.markdown(f'Cantidad de registros para negocio 14155 son {cantidad}')




    


















def main():
    
    menu = ["Datos","Saldos","Dia (Debitos y Creditos)","Cuenta (Debitos y Creditos)","Anomalias y Tendencias","Graficas","Prueba Tecnica"]
    eleccion = st.sidebar.selectbox("Menu", menu)

    try:
        df_movimientos = pd.read_excel("data.xlsx", "movimientos", index_col=None, na_values=["NA"])
        df_saldos = pd.read_excel("data.xlsx", "saldos", index_col=None, na_values=["NA"])

        df_movimientos['fecha'] = pd.to_datetime(df_movimientos['fecha'], format='%Y%m%d')
        df_saldos['fecha'] = pd.to_datetime(df_saldos['fecha'], format='%Y%m%d')

        st.success("Los archivos se leyeron correctamente")

    except Exception as e:
        st.error("Error al leer el archivo "+ {str(e)})
    
    
    if eleccion == "Datos":
        st.title("Analisis de los Movimientos")
        primero(df_movimientos, df_saldos)



    if eleccion == "Saldos":
        st.title("Analisis de los saldos")
        segundo(df_movimientos, df_saldos)



    if eleccion == "Dia (Debitos y Creditos)":
        st.title("Dia (Debitos y Creditos)")
        tercero(df_movimientos,df_saldos)



    if eleccion == "Cuenta (Debitos y Creditos)":
        st.title("Cuenta (Debitos y Creditos)")
        cuarto(df_movimientos,df_saldos)
        
        

    if eleccion == "Anomalias y Tendencias":
        st.title("Anomalias y Tendencias")
        quinto(df_movimientos,df_saldos)
        


    if eleccion == "Graficas":

        st.title("Graficas")
        sexto(df_movimientos,df_saldos)
        
    
    
    if eleccion == "Prueba Tecnica":
        st.title("Prueba Tecnica")
        septimo()







if __name__ == '__main__':
    main()