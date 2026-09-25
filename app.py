from flask import Flask, request

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import mysql.connector

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression


app = Flask(__name__, static_folder="graficos", static_url_path="/graficos")

# ==========================================
# MODELO DE INTELIGENCIA ARTIFICIAL
# ==========================================

modelo_ia = DecisionTreeClassifier(random_state=42)

datos_entrenamiento = np.array([
    [50000, 30000, 500],
    [60000, 35000, 700],
    [45000, 25000, 400],
    [30000, 27000, 300],
    [40000, 38000, 350],
    [35000, 32000, 250],
    [25000, 28000, 200],
    [20000, 24000, 150],
    [70000, 30000, 800],
    [80000, 40000, 1000]
])

resultados_entrenamiento = np.array([
    "Favorable",
    "Favorable",
    "Favorable",
    "Regular",
    "Regular",
    "Regular",
    "Requiere atención",
    "Requiere atención",
    "Favorable",
    "Favorable"
])

modelo_ia.fit(datos_entrenamiento, resultados_entrenamiento)


@app.route("/evaluar", methods=["POST"])
def evaluar():

    # ==========================================
    # RECIBIR DATOS DEL FORMULARIO
    # ==========================================

    nombre = request.form.get("nombre")
    empresa = request.form.get("empresa")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    sector = request.form.get("sector")
    ventas = request.form.get("ventas")
    gastos = request.form.get("gastos")
    clientes = request.form.get("clientes")
    problema = request.form.get("problema")


    # ==========================================
    # VERIFICAR DATOS RECIBIDOS
    # ==========================================

    if not ventas or not gastos or not clientes:
        return """
        <h2>Error en el formulario</h2>
        <p>No se recibieron correctamente los datos de ventas, gastos o clientes.</p>
        <a href="http://localhost/Asesoria-26-08/evaluacion.html">
            Volver al formulario
        </a>
        """


    # ==========================================
    # CONVERTIR DATOS NUMÉRICOS
    # ==========================================

    ventas = float(ventas)
    gastos = float(gastos)
    clientes = int(clientes)

    print("VENTAS:", ventas)
    print("GASTOS:", gastos)
    print("CLIENTES:", clientes)
    print("FORMULARIO COMPLETO:", request.form)


    # ==========================================
    # CALCULAR RESULTADOS
    # ==========================================

    ganancia = ventas - gastos


    # ==========================================
    # PREDICCIÓN MEDIANTE INTELIGENCIA ARTIFICIAL
    # ==========================================

    datos_empresa_ia = np.array([[ventas, gastos, clientes]])

    prediccion_ia = modelo_ia.predict(datos_empresa_ia)[0]

    if prediccion_ia == "Favorable":
        explicacion_ia = (
            "Tus números muestran un buen punto de partida. "
            "Las ventas, los gastos y tus clientes mantienen una relación positiva."
        )
    elif prediccion_ia == "Regular":
        explicacion_ia = (
            "Tu negocio tiene oportunidades para crecer. "
            "Pequeños ajustes en ventas, gastos o clientes pueden marcar la diferencia."
        )
    else:
        explicacion_ia = (
            "Encontramos algunos aspectos que conviene revisar. "
            "Analizar tus ventas, gastos y clientes puede ayudarte a encontrar nuevas oportunidades."
        )

    print("----- INTELIGENCIA ARTIFICIAL -----")
    print("Predicción del modelo:", prediccion_ia)


    # ==========================================
    # GUARDAR DATOS EN LA BASE DE DATOS
    # ==========================================
    conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    
    database="asesoria_bd"
)

    cursor = conexion.cursor()

    sql = """
        INSERT INTO evaluaciones
        (nombre, empresa, correo, telefono, sector, ventas, gastos, clientes, problema, ganancia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        nombre,
        empresa,
        correo,
        telefono,
        sector,
        ventas,
        gastos,
        clientes,
        problema,
        ganancia
    )

    cursor.execute(sql, valores)
    conexion.commit()
    cursor.close()


    # ==========================================
    # CALCULAR MARGEN
    # ==========================================

    if ventas > 0:
        margen = (ganancia / ventas) * 100
    else:
        margen = 0


    # ==========================================
    # ANÁLISIS ESTADÍSTICO
    # ==========================================

    promedio_ventas = ventas
    promedio_gastos = gastos
    promedio_ganancia = ganancia

    maximo_ventas = ventas
    minimo_ventas = ventas

    maximo_gastos = gastos
    minimo_gastos = gastos

    print("----- ANÁLISIS ESTADÍSTICO -----")
    print("Promedio de ventas:", round(promedio_ventas, 2))
    print("Promedio de gastos:", round(promedio_gastos, 2))
    print("Promedio de ganancia:", round(promedio_ganancia, 2))
    print("Venta máxima:", round(maximo_ventas, 2))
    print("Venta mínima:", round(minimo_ventas, 2))
    print("Gasto máximo:", round(maximo_gastos, 2))
    print("Gasto mínimo:", round(minimo_gastos, 2))
    print("Cantidad de clientes:", clientes)


    # ==========================================
    # ANALIZAR SITUACIÓN DE LA EMPRESA
    # ==========================================

    if margen >= 30:

        estado = "Favorable"

        recomendacion = (
            "La empresa presenta un margen de ganancia saludable."
        )

    elif margen >= 10:

        estado = "Regular"

        recomendacion = (
            "La empresa obtiene ganancias, pero existen oportunidades de mejora."
        )

    else:

        estado = "Requiere atención"

        recomendacion = (
            "El margen de ganancia es bajo. Se recomienda revisar "
            "los gastos y buscar oportunidades para mejorar las ventas."
        )


    # ==========================================
    # ANALIZAR PROBLEMA PRINCIPAL
    # ==========================================

    if problema == "ventas":

        recomendacion_problema = (
            "Se recomienda revisar las estrategias comerciales, "
            "precios y canales de venta."
        )

    elif problema == "gastos":

        recomendacion_problema = (
            "Se recomienda revisar los gastos y detectar costos "
            "que puedan reducirse."
        )

    elif problema == "organizacion":

        recomendacion_problema = (
            "Se recomienda mejorar la distribución de tareas "
            "y los procesos internos."
        )

    elif problema == "clientes":

        recomendacion_problema = (
            "Se recomienda trabajar en captación, fidelización "
            "y satisfacción de clientes."
        )

    elif problema == "rentabilidad":

        recomendacion_problema = (
            "Se recomienda revisar la relación entre ventas, "
            "gastos y margen de ganancia."
        )

    elif problema == "otro":

        recomendacion_problema = (
            "Se recomienda realizar una evaluación más detallada "
            "de la empresa."
        )

    else:

        recomendacion_problema = (
            "Se recomienda realizar una evaluación más detallada "
            "de la empresa."
        )


    # ==========================================
    # REGRESIÓN LINEAL
    # CLIENTES VS. GANANCIA
    # ==========================================

    datos_regresion = {

        "ventas": [
            8000, 9500, 12000, 15000, 11000,
            18000, 22000, 14000, 25000, 30000,
            17000, 21000, 27000, 32000, 19000
        ],

        "gastos": [
            6000, 7000, 8500, 10000, 8000,
            12000, 14500, 9500, 16000, 19000,
            11000, 13500, 17500, 20500, 12000
        ],

        "clientes": [
            25, 30, 40, 50, 35,
            60, 75, 45, 85, 100,
            55, 70, 90, 110, 65
        ]
    }

    df_regresion = pd.DataFrame(datos_regresion)

    df_regresion["ganancia"] = (
        df_regresion["ventas"] - df_regresion["gastos"]
    )


    # Variables del modelo

    X = df_regresion[["clientes"]]
    y = df_regresion["ganancia"]


    # Crear y entrenar modelo

    modelo = LinearRegression()
    modelo.fit(X, y)


    # Estimación para los clientes ingresados

    ganancia_estimada = modelo.predict(
        [[clientes]]
    )[0]


    # ==========================================
    # GRÁFICO 1: VENTAS VS. GASTOS
    # ==========================================

    plt.figure(figsize=(6, 4))

    datos = {
        "Concepto": ["Ventas", "Gastos"],
        "Monto": [ventas, gastos]
    }

    sns.barplot(
        x="Concepto",
        y="Monto",
        data=datos
    )

    plt.title("Ventas vs. Gastos")
    plt.ylabel("Monto (S/.)")
    plt.xlabel("")

    plt.tight_layout()

    ruta_grafico = os.path.join(
        os.path.dirname(__file__),
        "graficos",
        "ventas_gastos.png"
    )

    plt.savefig(ruta_grafico)
    plt.close()


    # ==========================================
    # GRÁFICO 2: MARGEN DE GANANCIA
    # ==========================================

    plt.figure(figsize=(6, 4))

    sns.barplot(
        x=["Margen de ganancia"],
        y=[margen]
    )

    plt.title("Margen de Ganancia")
    plt.ylabel("Porcentaje (%)")
    plt.xlabel("")

    plt.ylim(0, 100)

    plt.tight_layout()

    ruta_margen = os.path.join(
        os.path.dirname(__file__),
        "graficos",
        "margen_ganancia.png"
    )

    plt.savefig(ruta_margen)
    plt.close()


    # ==========================================
    # GRÁFICO 3: CANTIDAD DE CLIENTES
    # ==========================================

    plt.figure(figsize=(6, 4))

    sns.barplot(
        x=["Clientes"],
        y=[clientes]
    )

    plt.title("Cantidad de Clientes")
    plt.ylabel("Número de clientes")
    plt.xlabel("")

    plt.tight_layout()

    ruta_clientes = os.path.join(
        os.path.dirname(__file__),
        "graficos",
        "clientes.png"
    )

    plt.savefig(ruta_clientes)
    plt.close()


    # ==========================================
    # GRÁFICO 4: REGRESIÓN LINEAL
    # ==========================================

    clientes_linea = pd.DataFrame({
        "clientes": np.linspace(
            df_regresion["clientes"].min(),
            df_regresion["clientes"].max(),
            100
        )
    })

    ganancias_linea = modelo.predict(clientes_linea)

    plt.figure(figsize=(7, 5))

    sns.scatterplot(
        data=df_regresion,
        x="clientes",
        y="ganancia",
        s=100
    )

    plt.plot(
        clientes_linea["clientes"],
        ganancias_linea,
        linewidth=2
    )

    plt.scatter(
        clientes,
        ganancia,
        s=150,
        marker="X",
        label="Empresa evaluada"
    )

    plt.title("Regresión lineal: Clientes vs. Ganancia")
    plt.xlabel("Número de clientes")
    plt.ylabel("Ganancia (S/.)")
    plt.legend()
    plt.tight_layout()

    ruta_regresion = os.path.join(
        os.path.dirname(__file__),
        "graficos",
        "regresion_clientes_ganancias.png"
    )

    plt.savefig(ruta_regresion)
    plt.close()


    # ==========================================
    # MOSTRAR ANÁLISIS EN LA TERMINAL
    # ==========================================

    print("----- ANÁLISIS DE LA EMPRESA -----")
    print("Empresa:", empresa)
    print("Ventas:", ventas)
    print("Gastos:", gastos)
    print("Clientes:", clientes)
    print("Problema principal:", problema)
    print("Ganancia aproximada:", ganancia)
    print("Margen aproximado:", round(margen, 2), "%")
    print("Estado:", estado)

    if problema == "ventas":
        grafico_principal = "ventas_gastos.png"
        titulo_grafico = "Ventas y gastos de tu negocio"
        descripcion_grafico = "Observa la relación entre las ventas y los gastos registrados."

    elif problema == "gastos":
        grafico_principal = "ventas_gastos.png"
        titulo_grafico = "Ventas y gastos de tu negocio"
        descripcion_grafico = "Observa la relación entre tus ingresos y gastos."

    elif problema == "clientes":
        grafico_principal = "regresion_clientes_ganancias.png"
        titulo_grafico = "Clientes y ganancia"
        descripcion_grafico = "Observa la relación estimada entre tus clientes y la ganancia."

    elif problema == "rentabilidad":
        grafico_principal = "margen_ganancia.png"
        titulo_grafico = "Margen de ganancia"
        descripcion_grafico = "Observa el porcentaje de ganancia obtenido respecto a tus ventas."

    else:
        grafico_principal = "ventas_gastos.png"
        titulo_grafico = "Resumen de ventas y gastos"
        descripcion_grafico = "Vista general de los principales indicadores financieros."

    # ==========================================
    # RESULTADO EN EL NAVEGADOR
    # ==========================================

    return f"""
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Resultado de la evaluación</title>

    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #f4f7fb;
            color: #1f2937;
        }}

        .encabezado {{
            background-color: #1f2937;
            color: white;
            text-align: center;
            padding: 35px 20px;
        }}

        .encabezado h1 {{
            margin: 0 0 10px;
            font-size: 30px;
        }}

        .encabezado p {{
            margin: 0;
            color: #d1d5db;
        }}

        .contenedor {{
            max-width: 950px;
            margin: 30px auto;
            padding: 0 20px;
        }}

        .seccion {{
            background-color: white;
            padding: 28px;
            margin-bottom: 22px;
            border-radius: 14px;
            box-shadow: 0 5px 18px rgba(0,0,0,0.06);
        }}

        .seccion h2 {{
            margin-top: 0;
            margin-bottom: 20px;
            font-size: 22px;
        }}

        /* RESULTADO IA */

        .resultado-ia {{
            text-align: center;
            padding: 35px 25px;
        }}

        .ia-icono {{
            font-size: 42px;
            margin-bottom: 8px;
        }}

        .resultado-ia h2 {{
            margin-bottom: 8px;
        }}

        .ia-intro {{
            color: #6b7280;
            margin-bottom: 22px;
        }}

        .ia-resultado {{
            max-width: 520px;
            margin: auto;
            padding: 25px;
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
        }}

        .ia-etiqueta {{
            display: block;
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .ia-estado {{
            display: block;
            font-size: 30px;
            color: #2563eb;
            margin-bottom: 10px;
        }}

        .ia-resultado p {{
            margin: 0;
            color: #4b5563;
            line-height: 1.5;
        }}

        /* RESUMEN */

        .tarjetas {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }}

        .tarjeta {{
            padding: 20px 12px;
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            text-align: center;
        }}

        .tarjeta-titulo {{
            display: block;
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .tarjeta-valor {{
            font-size: 20px;
            font-weight: bold;
        }}

        .clientes {{
            margin-top: 15px;
            padding: 14px;
            text-align: center;
            background-color: #f8fafc;
            border-radius: 10px;
            color: #4b5563;
        }}

        .clientes strong {{
            color: #1f2937;
        }}

        /* GRÁFICOS */

        .graficos {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .grafico {{
            text-align: center;
            background-color: #f8fafc;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }}

        .grafico h3 {{
            margin-top: 0;
            font-size: 18px;
        }}

        .grafico img {{
            max-width: 100%;
            width: 100%;
            border-radius: 8px;
        }}

        .grafico p {{
            color: #6b7280;
            font-size: 14px;
            line-height: 1.5;
        }}

        /* RECOMENDACIÓN */

        .recomendacion {{
            background-color: #f8fafc;
            border-left: 4px solid #2563eb;
            padding: 20px;
            border-radius: 8px;
            line-height: 1.6;
            color: #4b5563;
        }}

        /* CONTACTO */

        .cta {{
            text-align: center;
            padding: 35px 25px;
        }}

        .cta h2 {{
            margin-bottom: 10px;
        }}

        .cta p {{
            color: #6b7280;
            margin-bottom: 22px;
        }}

        .boton-principal {{
            display: inline-block;
            padding: 13px 25px;
            background-color: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s;
        }}

        .boton-principal:hover {{
            background-color: #1d4ed8;
            transform: translateY(-2px);
        }}

        .boton-secundario {{
            display: block;
            margin-top: 16px;
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
        }}

        .boton-secundario:hover {{
            color: #2563eb;
        }}

        @media (max-width: 700px) {{

            .tarjetas {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .graficos {{
                grid-template-columns: 1fr;
            }}

        }}

        @media (max-width: 450px) {{

            .seccion {{
                padding: 20px;
            }}

            .tarjetas {{
                grid-template-columns: 1fr 1fr;
            }}

            .ia-estado {{
                font-size: 26px;
            }}

        }}

    </style>

</head>


<body>

    <header class="encabezado">

        <h1>¡Tu evaluación está lista!</h1>

        <p>Conoce rápidamente los resultados de tu empresa</p>

    </header>


    <main class="contenedor">


        <!-- RESULTADO DE IA -->

        <section class="seccion resultado-ia">

            <div class="ia-icono">🧠</div>

            <h2>Análisis de {empresa}</h2>

            <p class="ia-intro">
                Hola, {nombre}. Analizamos los datos que ingresaste
                para conocer la situación actual de tu negocio. 
            </p>

            <div class="ia-resultado">

                <span class="ia-etiqueta">
                    ¿Cómo está tu negocio?
                </span>

                <strong class="ia-estado">
                    {prediccion_ia}
                </strong>

                <p>
                    {explicacion_ia}
                </p>
            </div>
        </section>


        <!-- RESUMEN -->

        <section class="seccion">

            <h2>💰 Resumen de tu empresa</h2>

            <div class="tarjetas">

                <div class="tarjeta">

                    <span class="tarjeta-titulo">
                        Ventas
                    </span>

                    <span class="tarjeta-valor">
                        S/ {ventas:,.2f}
                    </span>

                </div>


                <div class="tarjeta">

                    <span class="tarjeta-titulo">
                        Gastos
                    </span>

                    <span class="tarjeta-valor">
                        S/ {gastos:,.2f}
                    </span>

                </div>


                <div class="tarjeta">

                    <span class="tarjeta-titulo">
                        Ganancia
                    </span>

                    <span class="tarjeta-valor">
                        S/ {ganancia:,.2f}
                    </span>

                </div>


                <div class="tarjeta">

                    <span class="tarjeta-titulo">
                        Margen
                    </span>

                    <span class="tarjeta-valor">
                        {margen:.2f}%
                    </span>

                </div>

            </div>


            <div class="clientes">

                Clientes aproximados:
                <strong>{clientes}</strong>

            </div>

        </section>


        <!-- ANÁLISIS -->

        <section class="seccion">

            <h2>📊 Análisis de tu empresa</h2>
            <p class="ia-intro">
                    Revisamos tus datos y seleccionamos información relacionada
                    con lo que quieres mejorar.
            </p>

            <div class="graficos">

                <div class="grafico">
                    <h3>{titulo_grafico}</h3>

                    <img
                        src="/graficos/{grafico_principal}"
                        alt="{titulo_grafico}"
                    >

                    <p>
                        {descripcion_grafico}
                    </p>
                </div>


                <div class="grafico">

                    <h3>Clientes vs. Ganancia</h3>

                    <img
                        src="/graficos/regresion_clientes_ganancias.png"
                        alt="Regresión entre clientes y ganancia"
                    >

                    <p>
                        Descubre cómo tus clientes pueden influir en la ganancia de tu negocio.
                    </p>

                </div>
            </div>

        </section>


        <!-- RECOMENDACIÓN -->

        <section class="seccion">

            <h2>💡 Recomendación para tu negocio</h2>

            <div class="recomendacion">

                {recomendacion}

                <br><br>

                {recomendacion_problema}

            </div>

        </section>


        <!-- CONTACTO -->

        <section class="seccion cta">

            <h2>🚀 ¿Quieres mejorar los resultados de tu empresa?</h2>

            <p>
                 Da el siguiente paso y recibe orientación para encontrar 
                 oportunidades de mejora en tu negocio.
            </p>

            <a
                href="http://localhost/Asesoria-26-08/contacto.php"
                class="boton-principal"
            >
                Solicitar asesoría →
            </a>

            <a
                href="http://localhost/Asesoria-26-08/evaluacion.html"
                class="boton-secundario"
            >
                Realizar otra evaluación
            </a>

        </section>


    </main>

</body>

</html>
"""

if __name__ == "__main__":
    app.run(debug=True)