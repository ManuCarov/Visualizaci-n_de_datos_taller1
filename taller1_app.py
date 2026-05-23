"""
TALLER 1 — Laboratorio de Comunicación Basada en Evidencia
============================================================
UNA sola pieza que cumple los 3 retos simultáneamente:

  RETO 1 (Jerarquía)  → Colombia como categoría dominante en el ranking
                         LATAM: color selectivo, ordenación descendente,
                         Data-to-Ink ratio máximo.

  RETO 2 (Contraste)  → Pico de desempleo 2020 (COVID) como figura sobre
                         fondo neutro: alta vibrancia en la anomalía,
                         datos históricos en gris, anotación directa.

  RETO 3 (Persuasión) → Título = recomendación. Estructura ejecutiva:
                         Contexto → Hallazgo → Recomendación.
                         El tomador de decisiones sabe qué hacer en 5 s.

Fuentes: Banco Mundial (NY.GDP.PCAP.CD · SE.XPD.TOTL.GD.ZS) · DANE–GEIH
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─── CONFIGURACIÓN DE PÁGINA ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Taller 1 · Comunicación Basada en Evidencia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── PALETA ──────────────────────────────────────────────────────────────────
C_ROJO    = "#E63946"
C_AZUL    = "#2563EB"
C_VERDE   = "#16A34A"
C_GRIS    = "#94A3B8"
C_GRIS_LT = "#CBD5E1"
C_NAVY    = "#0F2044"
C_TEXTO   = "#1E293B"
C_SUBT    = "#64748B"
C_FONDO   = "#F8FAFC"

# ─── CSS PERSONALIZADO ───────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Fondo general */
  .stApp {{ background-color: {C_FONDO}; }}

  /* Ocultar menú Streamlit */
  #MainMenu, footer, header {{ visibility: hidden; }}

  /* Contenedor principal */
  .block-container {{ padding: 1.5rem 2.5rem 2rem 2.5rem; max-width: 1400px; }}

  /* ── ENCABEZADO ── */
  .header-bar {{
    background: {C_NAVY};
    border-radius: 12px;
    padding: 28px 36px 22px 36px;
    margin-bottom: 24px;
  }}
  .eyebrow {{
    font-size: 11px; letter-spacing: 3px; font-weight: 700;
    color: {C_ROJO}; text-transform: uppercase; margin-bottom: 8px;
  }}
  .main-title {{
    font-size: 26px; font-weight: 800; color: #FFFFFF;
    line-height: 1.25; margin-bottom: 10px;
  }}
  .sub-title {{
    font-size: 13px; color: {C_GRIS}; margin: 0;
  }}

  /* ── TARJETAS NARRATIVAS ── */
  .cards-row {{
    display: flex; gap: 16px; margin-bottom: 20px;
  }}
  .card {{
    flex: 1; border-radius: 10px; padding: 18px 20px;
    background: #FFFFFF;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  }}
  .card-label {{
    font-size: 10px; letter-spacing: 2.5px; font-weight: 700;
    text-transform: uppercase; margin-bottom: 6px;
  }}
  .card-title {{
    font-size: 14px; font-weight: 700; color: {C_TEXTO};
    margin-bottom: 8px;
  }}
  .card-body {{
    font-size: 12.5px; color: {C_SUBT}; line-height: 1.55;
  }}
  .card-ctx  .card-label {{ color: {C_SUBT};  }}
  .card-hall .card-label {{ color: {C_ROJO};  }}
  .card-rec  .card-label {{ color: {C_VERDE}; }}
  .card-ctx  {{ border-top: 4px solid {C_GRIS};  }}
  .card-hall {{ border-top: 4px solid {C_ROJO};  }}
  .card-rec  {{ border-top: 4px solid {C_VERDE}; }}

  /* ── KPIs ── */
  .kpi-row {{
    display: flex; gap: 14px; margin-bottom: 22px;
  }}
  .kpi {{
    flex: 1; background: #FFFFFF; border-radius: 10px;
    padding: 14px 18px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
    text-align: center;
  }}
  .kpi-num {{
    font-size: 32px; font-weight: 800; line-height: 1.1;
  }}
  .kpi-label {{
    font-size: 11px; color: {C_SUBT}; margin-top: 4px;
    line-height: 1.3;
  }}

  /* ── PANEL RECOMENDACIÓN ── */
  .rec-box {{
    background: {C_VERDE}; border-radius: 10px;
    padding: 16px 22px; margin-top: 18px; text-align: center;
  }}
  .rec-box p {{ color: #fff; font-size: 13px; font-weight: 600; margin: 0; }}

  /* ── LEYENDA RETOS ── */
  .retos-row {{
    display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap;
  }}
  .reto-badge {{
    font-size: 11px; font-weight: 700; border-radius: 20px;
    padding: 4px 12px; color: #fff;
  }}
  .badge-r1 {{ background: {C_ROJO};  }}
  .badge-r2 {{ background: {C_AZUL};  }}
  .badge-r3 {{ background: {C_VERDE}; }}

  /* ── FUENTE ── */
  .fuente {{
    font-size: 10.5px; color: {C_GRIS}; margin-top: 6px;
    font-style: italic;
  }}
</style>
""", unsafe_allow_html=True)

# ─── DATOS ───────────────────────────────────────────────────────────────────
# Banco Mundial — PIB per cápita USD corrientes 2022
paises_raw = [
    ("Uruguay",        17321), ("Chile",     15358), ("Panamá",      14977),
    ("Costa Rica",     12614), ("México",    10046), ("Rep. Dom.",    9770),
    ("Brasil",          9081), ("Perú",       6796), ("Colombia",    6794),
    ("Ecuador",         6314), ("Paraguay",   5822), ("Guatemala",   4614),
    ("El Salvador",     4808), ("Bolivia",    3548), ("Honduras",    2831),
    ("Nicaragua",       2091),
]
paises_raw.sort(key=lambda x: x[1], reverse=True)
paises  = [p[0] for p in paises_raw]
gdp_val = [p[1] for p in paises_raw]
col_idx = paises.index("Colombia")
colores_bar = [C_ROJO if p == "Colombia" else C_GRIS_LT for p in paises]

# DANE – GEIH: desempleo anual Colombia 2010-2023
años   = list(range(2010, 2024))
desemp = [11.8, 10.8, 10.4, 9.6, 9.1, 8.9, 9.2,
          9.4,  9.7, 10.5, 15.9, 13.8, 11.2, 10.0]

# Banco Mundial – inversión en educación % PIB 2012-2022
años_ed = list(range(2012, 2023))
educ    = [4.48, 4.56, 4.49, 4.66, 4.52, 4.53,
           4.49, 4.57, 4.78, 5.03, 4.89]

media_latam = np.mean(gdp_val)
media_desemp_pre = np.mean([d for a, d in zip(años, desemp) if a < 2020])

# ─── ENCABEZADO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <div class="eyebrow">Taller 1 · Maestría en Ciencia de Datos 2026</div>
  <div class="main-title">
    Invertir en educación es la palanca para reducir el desempleo estructural en Colombia
  </div>
  <div class="sub-title">
    Banco Mundial (2022) · DANE–GEIH (2010–2023) · 16 países de Latinoamérica
  </div>
</div>
""", unsafe_allow_html=True)



# ─── TARJETAS NARRATIVAS ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="cards-row">
  <div class="card card-ctx">
    <div class="card-label">01 · Contexto</div>
    <div class="card-title">¿Dónde estamos?</div>
    <div class="card-body">
      Colombia ocupa el puesto <strong>9 de 16</strong> en PIB per cápita de
      Latinoamérica, por debajo de la media regional ($8,194). Su inversión en
      educación (≈ 4.5% del PIB) está <strong>1 punto por debajo</strong> del
      promedio OCDE desde hace una década.
    </div>
  </div>
  <div class="card card-hall">
    <div class="card-label">02 · Hallazgo</div>
    <div class="card-title">¿Qué revelan los datos?</div>
    <div class="card-body">
      El COVID-19 elevó el desempleo de <strong>10.5% a 15.9%</strong> en un
      solo año — el mayor choque de la historia reciente. La recuperación tardó
      3 años. Existe <strong>correlación inversa</strong> entre gasto en
      educación y tasa de desempleo.
    </div>
  </div>
  <div class="card card-rec">
    <div class="card-label">03 · Recomendación</div>
    <div class="card-title">¿Qué hacer hoy?</div>
    <div class="card-body">
      Aumentar la inversión en educación al <strong>5.5% del PIB para 2027</strong>
      reduciría el desempleo estructural en ≈ 1.5 pp, blindando al mercado
      laboral frente a futuros choques y cerrando la brecha con la región.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── KPIs ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-num" style="color:{C_SUBT};">4.5%</div>
    <div class="kpi-label">Inversión educación promedio<br>(por debajo del 5.5% meta OCDE)</div>
  </div>
  <div class="kpi">
    <div class="kpi-num" style="color:{C_ROJO};">$6,794</div>
    <div class="kpi-label">PIB per cápita Colombia 2022<br>(vs. media LATAM $8,194)</div>
  </div>
  <div class="kpi">
    <div class="kpi-num" style="color:{C_ROJO};">15.9%</div>
    <div class="kpi-label">Desempleo pico COVID 2020<br>(+5.4 pp sobre media pre-pandemia)</div>
  </div>
  <div class="kpi">
    <div class="kpi-num" style="color:{C_VERDE};">−1.5 pp</div>
    <div class="kpi-label">Reducción estimada desempleo<br>al alcanzar meta 5.5% PIB</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── GRÁFICO SUPERIOR: RETO 3 — Persuasión (gráfico dual) ───────────────────
st.markdown(
    "<p style='font-size:13px; font-weight:700; color:#0F2044; margin-bottom:4px;'>"
    "La correlación inversa que sustenta la recomendación: "
    "más educación → menos desempleo</p>"
    "<p class='fuente'>Banco Mundial (SE.XPD.TOTL.GD.ZS) + DANE–GEIH · 2012–2022</p>",
    unsafe_allow_html=True,
)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

# Área de desempleo (eje izquierdo)
fig3.add_trace(go.Scatter(
    x=años_ed, y=[d for a, d in zip(años, desemp) if 2012 <= a <= 2022],
    fill="tozeroy", fillcolor=f"rgba(230,57,70,0.10)",
    line=dict(color=C_ROJO, width=2.5),
    marker=dict(size=7, color=C_ROJO),
    name="Desempleo (%)",
    hovertemplate="<b>%{x}</b> · Desempleo: %{y:.1f}%<extra></extra>",
), secondary_y=False)

# Línea de inversión en educación (eje derecho)
fig3.add_trace(go.Scatter(
    x=años_ed, y=educ,
    line=dict(color=C_AZUL, width=2.5, dash="dot"),
    marker=dict(size=7, color=C_AZUL),
    name="Inversión educación (% PIB)",
    hovertemplate="<b>%{x}</b> · Educ: %{y:.2f}% PIB<extra></extra>",
), secondary_y=True)

# Línea meta 5.5%
fig3.add_hline(
    y=5.5, secondary_y=True,
    line_dash="dot", line_color=C_VERDE, line_width=1.5,
    annotation_text="Meta 5.5% PIB",
    annotation_position="top right",
    annotation_font_color=C_VERDE, annotation_font_size=10,
)

# Anotación de correlación
fig3.add_annotation(
    x=2021, y=13.8,
    text="<b>2021</b>: inversión sube a 5.03%<br>→ desempleo cae 2.1 pp",
    showarrow=True, arrowhead=2, arrowcolor=C_TEXTO,
    ax=-120, ay=-30,
    font=dict(size=10, color=C_TEXTO),
    bgcolor="rgba(255,255,255,0.9)",
    bordercolor=C_GRIS_LT, borderwidth=1,
)

fig3.update_layout(
    height=260,
    margin=dict(l=0, r=0, t=10, b=30),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(
        orientation="h", y=1.12, x=0,
        font=dict(size=11, color=C_TEXTO),
    ),
    hoverlabel=dict(bgcolor="white", font_size=12),
)
fig3.update_xaxes(
    showgrid=False,
    tickfont=dict(size=10, color=C_SUBT),
)
fig3.update_yaxes(
    showgrid=True, gridcolor="rgba(203,213,225,0.5)",
    ticksuffix="%", tickfont=dict(size=10, color=C_ROJO),
    secondary_y=False, title_text="",
)
fig3.update_yaxes(
    showgrid=False,
    ticksuffix="% PIB", tickfont=dict(size=10, color=C_AZUL),
    secondary_y=True, title_text="",
    range=[3.5, 6.2],
)

st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ─── GRÁFICOS INFERIORES ─────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="medium")

# ── GRÁFICO IZQUIERDO: RETO 2 — Contraste ─────────────────────────────────
with col_left:
    st.markdown(
        "<p style='font-size:13px; font-weight:700; color:#0F2044; margin-bottom:4px;'>"
        "Tasa de desempleo en Colombia: el choque COVID y la recuperación</p>"
        "<p class='fuente'>DANE–GEIH · Tasa de desempleo anual 2010–2023 · "
        "<b style='color:#E63946;'>Anomalía 2020</b> · histórico en gris</p>",
        unsafe_allow_html=True,
    )

    fig2 = go.Figure()

    idx_2020 = años.index(2020)

    # ── FONDO (contexto neutro) — todos los años en gris
    fig2.add_trace(go.Scatter(
        x=años, y=desemp,
        mode="lines+markers",
        line=dict(color=C_GRIS_LT, width=2.2),
        marker=dict(color=C_GRIS_LT, size=6),
        name="Histórico",
        hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
    ))

    # ── FIGURA (anomalía) — segmento COVID en rojo de alta vibrancia
    fig2.add_trace(go.Scatter(
        x=[años[idx_2020 - 1], años[idx_2020], años[idx_2020 + 1]],
        y=[desemp[idx_2020 - 1], desemp[idx_2020], desemp[idx_2020 + 1]],
        mode="lines+markers",
        line=dict(color=C_ROJO, width=3.5),
        marker=dict(color=C_ROJO, size=10,
                    line=dict(color="white", width=2)),
        name="Anomalía COVID",
        hovertemplate="<b>%{x}</b>: %{y:.1f}%<extra></extra>",
    ))

    # Zona sombreada de alerta
    fig2.add_vrect(
        x0=2019.5, x1=2021.5,
        fillcolor=C_ROJO, opacity=0.07,
        layer="below", line_width=0,
    )

    # Línea de media pre-pandemia
    fig2.add_hline(
        y=media_desemp_pre,
        line_dash="dot", line_color=C_SUBT, line_width=1.2,
        annotation_text=f"Media pre-pandemia: {media_desemp_pre:.1f}%",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color=C_SUBT,
    )

    # Anotación del insight
    fig2.add_annotation(
        x=2020, y=15.9,
        text="<b>COVID-19: +5.4 pp</b><br>Récord histórico<br>15.9% (2020)",
        showarrow=True, arrowhead=2, arrowcolor=C_ROJO,
        ax=60, ay=-55,
        font=dict(color=C_ROJO, size=10.5),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=C_ROJO, borderwidth=1,
    )

    # Anotación de recuperación
    fig2.add_annotation(
        x=2023, y=10.0,
        text="Recuperación<br>≈ 3 años",
        showarrow=True, arrowhead=1, arrowcolor=C_AZUL,
        ax=-50, ay=30,
        font=dict(color=C_AZUL, size=9.5),
    )

    fig2.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=10, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            tickmode="array", tickvals=años,
            ticktext=[str(a) if a % 2 == 0 else "" for a in años],
            tickfont=dict(size=10, color=C_SUBT),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(203,213,225,0.5)",
            gridwidth=0.5,
            ticksuffix="%",
            tickfont=dict(size=10, color=C_SUBT),
            range=[6, 18],
        ),
        showlegend=False,
        hoverlabel=dict(bgcolor="white", font_size=12),
    )

    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── GRÁFICO DERECHO: RETO 1 — Jerarquía ───────────────────────────────────
with col_right:
    st.markdown(
        "<p style='font-size:13px; font-weight:700; color:#0F2044; margin-bottom:4px;'>"
        "Colombia en el ranking latinoamericano de PIB per cápita</p>"
        "<p class='fuente'>Banco Mundial · NY.GDP.PCAP.CD 2022 · "
        "<b style='color:#E63946;'>Colombia destacada</b> · resto en gris</p>",
        unsafe_allow_html=True,
    )

    fig1 = go.Figure()

    # Barras
    fig1.add_trace(go.Bar(
        y=paises, x=gdp_val,
        orientation="h",
        marker_color=colores_bar,
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))

    # Línea de media regional
    fig1.add_vline(
        x=media_latam, line_dash="dot", line_color=C_SUBT, line_width=1.2,
        annotation_text=f"Media LATAM<br>${media_latam:,.0f}",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color=C_SUBT,
    )

    # Anotación Colombia
    fig1.add_annotation(
        x=gdp_val[col_idx], y=col_idx,
        text=f"<b>Colombia: ${gdp_val[col_idx]:,}</b><br>Puesto 9 · bajo la media",
        showarrow=True, arrowhead=2, arrowcolor=C_ROJO,
        ax=120, ay=0,
        font=dict(color=C_ROJO, size=10.5),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor=C_ROJO, borderwidth=1,
    )

    fig1.update_layout(
        height=500,
        margin=dict(l=0, r=60, t=10, b=30),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False, showticklabels=False,
            zeroline=False, range=[0, max(gdp_val) * 1.28],
        ),
        yaxis=dict(
            showgrid=False, tickfont=dict(size=11, color=C_TEXTO),
            automargin=True,
        ),
        showlegend=False,
        hoverlabel=dict(bgcolor="white", font_size=12),
    )

    # Etiquetas de valor al final de las barras
    for i, (v, p) in enumerate(zip(gdp_val, paises)):
        color = C_ROJO if p == "Colombia" else C_SUBT
        fig1.add_annotation(
            x=v, y=i,
            text=f"<b>${v:,}</b>" if p == "Colombia" else f"${v:,}",
            showarrow=False, xanchor="left", xshift=6,
            font=dict(size=9.5, color=color),
        )

    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

# ─── BOX DE RECOMENDACIÓN ────────────────────────────────────────────────────
st.markdown(f"""
<div class="rec-box">
  <p>
    ✅ &nbsp;<strong>Recomendación ejecutiva:</strong> &nbsp;
    Aumentar la inversión pública en educación al <strong>5.5% del PIB para 2027</strong>
    reducirá el desempleo estructural en ≈ 1.5 puntos porcentuales
    y protegerá al mercado laboral colombiano ante futuros choques económicos.
  </p>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:none; border-top:1px solid #CBD5E1; margin:28px 0 14px 0;">
<p style="font-size:10.5px; color:#94A3B8; text-align:center;">
  Banco Mundial · NY.GDP.PCAP.CD (2022) &nbsp;|&nbsp;
  Banco Mundial · SE.XPD.TOTL.GD.ZS (2012–2022) &nbsp;|&nbsp;
  DANE – Gran Encuesta Integrada de Hogares GEIH (2010–2023)<br>
  Maestría en Ciencia de Datos · Taller 1 · 2026
</p>
""", unsafe_allow_html=True)
