import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.nutrition_model import search_foods, get_nutrition_data
import plotly.graph_objects as go

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 11 · USDA Nutrition Database</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            NUTRITION FOOD ANALYSER
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Search and analyse nutritional content of foods from the USDA database
        </div>
    </div>
    """, unsafe_allow_html=True)

    info = get_nutrition_data()

    if info["real_data"]:
        st.markdown(f"""
        <div style="background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.2);
                    border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem;">
            <span style="color:#00ffe7; font-size:0.8rem;">
                ✅ Using <b>USDA Food Nutrition Dataset</b> — {info['n_samples']:,} food items loaded
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,202,40,0.05); border:1px solid rgba(255,202,40,0.2);
                    border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem;">
            <span style="color:#ffca28; font-size:0.8rem;">
                ⚙️ Using built-in nutrition table. Add <b>food.csv</b> to <b>data/</b> folder for full USDA database.
                Dataset: <a style="color:#ffca28;" href="https://www.kaggle.com/datasets/thedevastator/usda-nutrition-database" target="_blank">Kaggle Link</a>
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Search
    query = st.text_input("🔍  Search food", placeholder="e.g. chicken, rice, egg, paneer...")
    foods_df, real, n = search_foods(query, top_n=10)

    st.markdown("""
    <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin:1rem 0 0.8rem;">
        Search Results
    </div>
    """, unsafe_allow_html=True)

    colors = ["#00ffe7","#00b8ff","#9b59b6","#ff6b35","#00e676",
              "#ffca28","#ff5252","#00ffe7","#00b8ff","#9b59b6"]

    for i, (_, row) in enumerate(foods_df.iterrows()):
        color = colors[i % len(colors)]
        prot  = round(float(row["protein"]), 1)
        cal   = round(float(row["calories"]), 1)
        carbs = round(float(row["carbs"]), 1) if "carbs" in row else 0
        fat   = round(float(row["fat"]), 1)   if "fat"   in row else 0

        st.markdown(f"""
        <div style="background:#0d1526; border-left:3px solid {color};
                    border-radius:0 8px 8px 0; padding:0.8rem 1.2rem;
                    margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="color:white; font-size:0.85rem; font-weight:500;">{row['name']}</div>
            </div>
            <div style="display:flex; gap:1.5rem; text-align:center;">
                <div>
                    <div style="color:#ff6b35; font-family:'Orbitron',monospace; font-size:0.85rem;">{cal}</div>
                    <div style="color:#5a7a99; font-size:0.65rem; text-transform:uppercase;">kcal</div>
                </div>
                <div>
                    <div style="color:#00ffe7; font-family:'Orbitron',monospace; font-size:0.85rem;">{prot}g</div>
                    <div style="color:#5a7a99; font-size:0.65rem; text-transform:uppercase;">protein</div>
                </div>
                <div>
                    <div style="color:#00b8ff; font-family:'Orbitron',monospace; font-size:0.85rem;">{carbs}g</div>
                    <div style="color:#5a7a99; font-size:0.65rem; text-transform:uppercase;">carbs</div>
                </div>
                <div>
                    <div style="color:#9b59b6; font-family:'Orbitron',monospace; font-size:0.85rem;">{fat}g</div>
                    <div style="color:#5a7a99; font-size:0.65rem; text-transform:uppercase;">fat</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Macro comparison chart for top 5
    if len(foods_df) >= 3:
        st.markdown("<br>", unsafe_allow_html=True)
        names  = [r["name"][:20] for _, r in foods_df.head(5).iterrows()]
        prots  = [round(float(r["protein"]), 1) for _, r in foods_df.head(5).iterrows()]
        carbs_ = [round(float(r.get("carbs", 0)), 1) for _, r in foods_df.head(5).iterrows()]
        fats_  = [round(float(r.get("fat", 0)), 1) for _, r in foods_df.head(5).iterrows()]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Protein", x=names, y=prots,
                             marker_color="#00ffe7"))
        fig.add_trace(go.Bar(name="Carbs", x=names, y=carbs_,
                             marker_color="#00b8ff"))
        fig.add_trace(go.Bar(name="Fat", x=names, y=fats_,
                             marker_color="#ff6b35"))
        fig.update_layout(
            barmode="group",
            title=dict(text="Macro Comparison (Top 5 Results)", font=dict(family="Orbitron", color="white", size=12)),
            paper_bgcolor="#070b14", plot_bgcolor="#0d1526",
            font=dict(color="#5a7a99"),
            xaxis=dict(tickfont=dict(color="#5a7a99", size=9), gridcolor="#1a2a45"),
            yaxis=dict(title="grams", gridcolor="#1a2a45", tickfont=dict(color="#5a7a99")),
            legend=dict(font=dict(color="#c8d8f0"), bgcolor="rgba(0,0,0,0)"),
            height=300, margin=dict(t=40, b=30, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)
