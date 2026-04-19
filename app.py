import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración
st.set_page_config(page_title="Dashboard Abandono Escolar", layout="wide")

st.title("📊 Dashboard de Abandono Escolar")
st.markdown("Análisis interactivo del desempeño académico y deserción estudiantil")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv('data/dataset.csv')

df = load_data()

# Sidebar
st.sidebar.header("Filtros")
target_filter = st.sidebar.multiselect(
    "Estado del estudiante",
    options=df['target'].unique(),
    default=df['target'].unique()
)

df_filtered = df[df['target'].isin(target_filter)]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Estudiantes", len(df_filtered))
col2.metric("Promedio Admission Grade", round(df_filtered['admission_grade'].mean(), 2))
col3.metric("Promedio 1er Semestre", round(df_filtered['first_sem_grade'].mean(), 2))

# Gráficos
st.subheader("📊 Promedio por Estado")
bar_fig = px.bar(
    df_filtered.groupby('target')['admission_grade'].mean().reset_index(),
    x='target',
    y='admission_grade',
    color='target'
)
st.plotly_chart(bar_fig, use_container_width=True)

st.subheader("📉 Correlación")
scatter_fig = px.scatter(
    df_filtered,
    x='admission_grade',
    y='first_sem_grade',
    color='target'
)
st.plotly_chart(scatter_fig, use_container_width=True)

st.subheader("📊 Distribución")
hist_fig = px.histogram(df_filtered, x='admission_grade', nbins=20)
st.plotly_chart(hist_fig, use_container_width=True)

st.subheader("📦 Boxplot")
box_fig = px.box(df_filtered, x='target', y='admission_grade')
st.plotly_chart(box_fig, use_container_width=True)

st.subheader("📈 Tendencia")
df_sorted = df_filtered.sort_values(by='admission_grade')
line_fig = px.line(df_sorted, x='admission_grade', y='first_sem_grade')
st.plotly_chart(line_fig, use_container_width=True)

# Conclusión
st.markdown("## 📌 Conclusiones")
st.write("""
- Existe una relación positiva entre calificación de admisión y desempeño académico.
- Los estudiantes con menor rendimiento inicial presentan mayor riesgo de abandono.
- Se recomienda implementar sistemas de detección temprana.
""")
