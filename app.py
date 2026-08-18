import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="EDA Bank Marketing App", page_icon="📊", layout="wide"
)


# ==========================================
# CLASE POO: PROGRAMACIÓN ORIENTADA A OBJETOS
# ==========================================
class AnalizadorDatos:
    """Clase encargada de encapsular el procesamiento y análisis descriptivo del dataset."""

    def __init__(self, df):
        self.df = df

    def clasificar_variables(self):
        """Función personalizada para clasificar columnas en numéricas y categóricas."""
        numericas = self.df.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()
        categoricas = self.df.select_dtypes(
            include=['object', 'category']
        ).columns.tolist()
        return numericas, categoricas

    def obtener_resumen_nulos(self):
        """Genera una tabla con la información de tipos de datos y nulos."""
        resumen = pd.DataFrame({
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores Nulos': self.df.isnull().sum(),
            'Porcentaje Nulos (%)': (self.df.isnull().sum() / len(self.df))
            * 100,
        })
        return resumen

    def obtener_estadisticas_numericas(self):
        """Devuelve las estadísticas descriptivas de las variables cuantitativas."""
        return self.df.describe()


# ==========================================
# MENÚ NAVEGABLE EN LA BARRA LATERAL (SIDEBAR)
# ==========================================
st.sidebar.image("logo_dmc.png")
st.sidebar.title("Menú de Navegación 📌")
opcion_menu = st.sidebar.radio(
    "Seleccione un módulo:",
    ["1. Home", "2. Carga de Datos", "3. Análisis EDA", "4. Conclusiones"],
)

# Inicializar st.session_state para mantener los datos cargados entre páginas
if "data" not in st.session_state:
    st.session_state["data"] = None

# ==========================================
# MÓDULO 1: HOME (PRESENTACIÓN)
# ==========================================
if opcion_menu == "1. Home":

    col_img, col_txt = st.columns([1, 4], vertical_alignment="center")
    
    with col_img:
        st.image("logo_python.png")
        
    with col_txt:
        st.markdown(
                "<h1 style='margin: 0; padding: 0;'>Proyecto: Análisis Exploratorio"
                " de Datos - Bank Marketing</h1>",
                unsafe_allow_html=True,
            )
    
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🎯 Objetivo del Análisis")
        st.write(
            "El propósito de esta herramienta interactiva es realizar un Análisis Exploratorio de Datos (EDA) "
            "sobre la última campaña de marketing telefónico de la institución financiera. "
            "El enfoque está orientado a identificar patrones de comportamiento comercial y factores clave que "
            "influyen en la conversión de clientes, apoyando la toma de decisiones estratégicas sin recurrir a modelos predictivos."
        )

        st.subheader("📖 Sobre el Dataset")
        st.write(
            "El dataset contiene información de clientes abordados en campañas directas. "
            "Incluye variables sociodemográficas, financieras, de contacto comercial y macroeconómicas, "
            "siendo la variable objetivo **'y'** (aceptación del producto: *yes* / *no*)."
        )

    with col2:
        st.info("👨‍💻 **Datos del Autor**")
        st.write("**Estudiante:** Reyes Marcial Tiburcio Totos")
        st.write("**Curso:** Especialización en Python for Analytics")
        st.write("**Año:** 2026")

        st.success("🛠️ **Tecnologías Utilizadas**")
        st.markdown("""
        - Python
        - Streamlit
        - Pandas & NumPy
        - Matplotlib & Seaborn
        """)

# ==========================================
# MÓDULO 2: CARGA DEL DATASET
# ==========================================
elif opcion_menu == "2. Carga de Datos":
    st.title("📁 Módulo de Carga del Dataset")
    st.markdown("---")

    archivo_cargado = st.file_uploader(
        "Cargue el archivo CSV de Bank Marketing (ej. BankMarketing.csv o delimitado por ';'):",
        type=["csv"],
    )

    if archivo_cargado is not None:
        try:
            # Intento de lectura considerando posibles separadores habituales en este dataset
            try:
                df = pd.read_csv(archivo_cargado, sep=";")
                if len(df.columns) <= 1:
                    archivo_cargado.seek(0)
                    df = pd.read_csv(archivo_cargado, sep=",")
            except Exception:
                archivo_cargado.seek(0)
                df = pd.read_csv(archivo_cargado, sep=",")

            st.session_state["data"] = df
            st.success("✅ Archivo cargado correctamente.")

            st.subheader("📊 Vista Previa del Dataset")
            st.dataframe(df.head(10))

            col_filas, col_cols = st.columns(2)
            col_filas.metric(
                label="Número total de filas", value=f"{df.shape[0]:,}"
            )
            col_cols.metric(
                label="Número total de columnas", value=df.shape[1]
            )

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        st.warning("⚠️ Por favor, cargue un archivo CSV para continuar.")
        if st.session_state["data"] is not None:
            st.info(
                "Ya existe un dataset cargado en la sesión activa. Puede proceder al Módulo de Análisis."
            )

# ==========================================
# MÓDULO 3: ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# ==========================================
elif opcion_menu == "3. Análisis EDA":
    st.title("🔬 Módulo 3: Análisis Exploratorio de Datos (EDA)")
    st.markdown("---")

    if st.session_state["data"] is None:
        st.error(
            "🛑 Debe cargar primero un archivo en el módulo '2. Carga de Datos'."
        )
    else:
        df = st.session_state["data"]
        analizador = AnalizadorDatos(df)
        num_vars, cat_vars = analizador.clasificar_variables()

        # Organización mediante pestañas (st.tabs)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Info General & Tipos",
            "📊 Estadística & Nulos",
            "📈 Distribuciones",
            "🔍 Análisis Bivariado",
            "⚙️ Dinámico & Hallazgos",
        ])

        # TAB 1: ITEMS 1 Y 2
        with tab1:
            st.subheader("Ítem 1: Información General del Dataset")
            resumen_df = analizador.obtener_resumen_nulos()
            st.dataframe(resumen_df, use_container_width=True)

            st.markdown("---")
            st.subheader("Ítem 2: Clasificación de Variables (Uso de POO)")
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Variables Numéricas ({len(num_vars)}):**")
                st.write(num_vars)
            with c2:
                st.write(f"**Variables Categóricas ({len(cat_vars)}):**")
                st.write(cat_vars)

        # TAB 2: ITEMS 3 Y 4
        with tab2:
            st.subheader("Ítem 3: Estadísticas Descriptivas")
            st.dataframe(
                analizador.obtener_estadisticas_numericas(),
                use_container_width=True,
            )
            st.info(
                "💡 **Interpretación:** Permite observar la dispersión, promedios y percentiles. "
                "Atención especial a 'duration', 'age' y variables macroeconómicas."
            )

            st.markdown("---")
            st.subheader("Ítem 4: Análisis de Valores Faltantes")
            nulos_totales = df.isnull().sum().sum()
            st.write(
                f"**Cantidad de valores nulos explícitos (NaN):** {nulos_totales}"
            )

            # Verificación de categoría 'unknown' en categóricas
            unknown_counts = {
                col: (df[col] == "unknown").sum()
                for col in cat_vars
                if "unknown" in df[col].values
            }
            if unknown_counts:
                st.warning(
                    "Se identificaron registros con etiquetas **'unknown'** en variables categóricas:"
                )
                df_unknown = pd.DataFrame.from_dict(
                    unknown_counts, orient="index", columns=["Conteo Unknown"]
                )
                st.table(df_unknown)

        # TAB 3: ITEMS 5 Y 6
        with tab3:
            st.subheader("Ítem 5: Distribución de Variables Numéricas")
            var_num_sel = st.selectbox(
                "Seleccione una variable numérica:", num_vars, key="sb_num"
            )
            bins_num = st.slider(
                "Seleccione cantidad de Bins (intervalos):", 5, 50, 20
            )

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df[var_num_sel], bins=bins_num, kde=True, ax=ax)
            ax.set_title(f"Distribución de {var_num_sel}")
            st.pyplot(fig)

            st.markdown("---")
            st.subheader("Ítem 6: Análisis de Variables Categóricas")
            var_cat_sel = st.selectbox(
                "Seleccione una variable categórica:", cat_vars, key="sb_cat"
            )
            ver_porcentaje = st.checkbox(
                "Mostrar proporciones en porcentaje (%)"
            )

            col_graf, col_tab = st.columns([2, 1])

            with col_tab:
                conteo = df[var_cat_sel].value_counts()
                if ver_porcentaje:
                    tabla_cat = pd.DataFrame({
                        "Frecuencia": conteo,
                        "Porcentaje (%)": (conteo / len(df)) * 100,
                    })
                else:
                    tabla_cat = pd.DataFrame({"Frecuencia": conteo})
                st.dataframe(tabla_cat)

            with col_graf:
                fig, ax = plt.subplots(figsize=(7, 4))
                sns.countplot(
                    data=df,
                    y=var_cat_sel,
                    order=conteo.index,
                    palette="viridis",
                    ax=ax,
                )
                ax.set_title(f"Frecuencia de {var_cat_sel}")
                st.pyplot(fig)

        # TAB 4: ITEMS 7 Y 8
        with tab4:
            st.subheader("Ítem 7: Bivariado (Numérico vs Categórico Target)")
            var_biv_num = st.selectbox(
                "Seleccione variable numérica a comparar con 'y':",
                num_vars,
                key="biv_num",
            )

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(data=df, x="y", y=var_biv_num, palette="Set2", ax=ax)
            ax.set_title(f"Comparación de {var_biv_num} según Aceptación ('y')")
            st.pyplot(fig)

            st.markdown("---")
            st.subheader(
                "Ítem 8: Bivariado (Categórico vs Categórico Target)"
            )
            var_biv_cat = st.selectbox(
                "Seleccione variable categórica a comparar con 'y':",
                [c for c in cat_vars if c != "y"],
                key="biv_cat",
            )

            ct = pd.crosstab(df[var_biv_cat], df["y"], normalize="index") * 100
            fig, ax = plt.subplots(figsize=(9, 4))
            ct.plot(kind="bar", stacked=True, ax=ax, colormap="tab10")
            ax.set_ylabel("Porcentaje (%)")
            ax.set_title(f"Tasa de Respuesta en {var_biv_cat}")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)

        # TAB 5: ITEMS 9 Y 10
        with tab5:
            st.subheader(
                "Ítem 9: Análisis Basado en Parámetros Seleccionados"
            )
            columnas_mult = st.multiselect(
                "Seleccione columnas numéricas para ver correlación:",
                num_vars,
                default=num_vars[:4] if len(num_vars) >= 4 else num_vars,
            )

            if len(columnas_mult) >= 2:
                fig, ax = plt.subplots(figsize=(7, 4))
                sns.heatmap(
                    df[columnas_mult].corr(),
                    annot=True,
                    fmt=".2f",
                    cmap="coolwarm",
                    ax=ax,
                )
                st.pyplot(fig)
            else:
                st.info("Seleccione al menos 2 columnas para calcular la matriz.")

            st.markdown("---")
            st.subheader("Ítem 10: Hallazgos Clave")
            kpi1, kpi2, kpi3 = st.columns(3)
            tasa_conv = (df["y"].value_counts(normalize=True).get("yes", 0)) * 100
            kpi1.metric("Tasa Global de Aceptación", f"{tasa_conv:.2f}%")
            kpi2.metric("Duración Promedio (Aceptaron)", f"{df[df['y']=='yes']['duration'].mean():.1f} s")
            kpi3.metric("Duración Promedio (Rechazaron)", f"{df[df['y']=='no']['duration'].mean():.1f} s")

            st.write(
                "📌 **Resumen de Insights:** La duración de las llamadas es el factor determinante primario de conversión. "
                "Asimismo, variables macroeconómicas (como `euribor3m`) reflejan una alta sensibilidad al contexto de mercado."
            )

# ==========================================
# MÓDULO 4: CONCLUSIONES FINALES
# ==========================================
elif opcion_menu == "4. Conclusiones":
    st.title("💡 Conclusiones Finales y Recomendaciones")
    st.markdown("---")

    st.markdown("""
    ### 📌 5 Conclusiones Clave para la Toma de Decisiones:

    1. **Impacto Crítico del Tiempo de Contacto (`duration`):**
       Los clientes que aceptaron el producto registraron llamadas significativamente más largas en promedio. Se debe capacitar al equipo comercial para mantener conversaciones de valor y retener la atención del cliente durante los primeros minutos.

    2. **Optimizaciones por Canal de Comunicación (`contact`):**
       Los contactos realizados mediante teléfono móvil presentan mejores tasas de conversión que las líneas fijas. Se recomienda priorizar la gestión telefónica móvil en la estrategia de contacto.

    3. **Influencia del Historial de Campañas (`poutcome`):**
       Los clientes cuyo resultado en campañas previas fue exitoso (*success*) muestran la mayor probabilidad de volver a contratar. Se sugiere implementar un flujo preferencial de fidelización para este segmento.

    4. **Saturación por Exceso de Contactos (`campaign`):**
       Superar los 3 o 4 contactos en la misma campaña no incrementa la tasa de conversión y genera desgaste en el cliente. Se aconseja establecer un límite estricto de reintentos comerciales.

    5. **Sensibilidad al Entorno Económico (`euribor3m` / `emp.var.rate`):**
       En periodos con tasas de interés elevadas, la disposición al depósito a plazo disminuye. Las campañas comerciales deben sincronizarse con coyunturas de mercado propicias para maximizar el retorno de inversión.
    """)
