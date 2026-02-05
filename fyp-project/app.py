# app.py
# UK SME Import Margin Simulator - Main Streamlit Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime

# Core calculation modules
from scripts.margin_model import compute_margin
from scripts.scenario_runner import run_sensitivity_scenarios
from scripts.risk_label import risk_label
from scripts.risk_adjuster import adjust_risk
from scripts.confidence_band import confidence_multiplier

# Page config
st.set_page_config(
    page_title="UK SME Import Margin Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# HS2 chapter descriptions (codes 01-99)
HS2_DESCRIPTIONS = {
    1: "Live animals", 2: "Meat and edible meat offal", 3: "Fish and crustaceans",
    4: "Dairy produce, eggs, honey", 5: "Products of animal origin", 6: "Live trees and plants",
    7: "Edible vegetables", 8: "Edible fruit and nuts", 9: "Coffee, tea, spices",
    10: "Cereals", 11: "Milling products, malt, starches", 12: "Oil seeds, miscellaneous grains",
    13: "Lac, gums, resins", 14: "Vegetable plaiting materials", 15: "Animal or vegetable fats",
    16: "Preparations of meat or fish", 17: "Sugars and sugar confectionery", 18: "Cocoa and cocoa preparations",
    19: "Preparations of cereals", 20: "Preparations of vegetables, fruit", 21: "Miscellaneous edible preparations",
    22: "Beverages, spirits and vinegar", 23: "Food industry residues", 24: "Tobacco and substitutes",
    25: "Salt, sulphur, earth and stone", 26: "Ores, slag and ash", 27: "Mineral fuels, oils",
    28: "Inorganic chemicals", 29: "Organic chemicals", 30: "Pharmaceutical products",
    31: "Fertilisers", 32: "Tanning or dyeing extracts", 33: "Essential oils and perfumery",
    34: "Soap, washing preparations", 35: "Albuminoidal substances, glues", 36: "Explosives, pyrotechnics",
    37: "Photographic goods", 38: "Miscellaneous chemical products", 39: "Plastics and articles",
    40: "Rubber and articles", 41: "Raw hides, skins and leather", 42: "Articles of leather",
    43: "Furskins and artificial fur", 44: "Wood and articles of wood", 45: "Cork and articles",
    46: "Manufactures of straw", 47: "Pulp of wood", 48: "Paper and paperboard",
    49: "Printed books, newspapers", 50: "Silk", 51: "Wool and fine animal hair",
    52: "Cotton", 53: "Other vegetable textile fibres", 54: "Man-made filaments",
    55: "Man-made staple fibres", 56: "Wadding, felt and nonwovens", 57: "Carpets and textile floor coverings",
    58: "Special woven fabrics", 59: "Impregnated textile fabrics", 60: "Knitted or crocheted fabrics",
    61: "Knitted apparel and accessories", 62: "Woven apparel and accessories", 63: "Other made up textile articles",
    64: "Footwear", 65: "Headgear", 66: "Umbrellas, walking sticks",
    67: "Prepared feathers", 68: "Articles of stone, plaster, cement", 69: "Ceramic products",
    70: "Glass and glassware", 71: "Precious stones and metals", 72: "Iron and steel",
    73: "Articles of iron or steel", 74: "Copper and articles", 75: "Nickel and articles",
    76: "Aluminium and articles", 78: "Lead and articles", 79: "Zinc and articles",
    80: "Tin and articles", 81: "Other base metals", 82: "Tools of base metal",
    83: "Miscellaneous articles of base metal", 84: "Nuclear reactors, boilers, machinery", 85: "Electrical machinery",
    86: "Railway locomotives", 87: "Vehicles other than railway", 88: "Aircraft and spacecraft",
    89: "Ships and boats", 90: "Optical and medical instruments", 91: "Clocks and watches",
    92: "Musical instruments", 93: "Arms and ammunition", 94: "Furniture and bedding",
    95: "Toys, games and sports equipment", 96: "Miscellaneous manufactured articles", 97: "Works of art and antiques",
    99: "Special transactions"
}

# Custom CSS styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-card-profit {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .metric-card-loss {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    }
    
    .metric-card-margin {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .metric-card-cost {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .metric-card-revenue {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 2rem;
        font-weight: 600;
        font-size: 1rem;
        margin: 0.25rem;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
        color: #333;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
    }
    
    .coverage-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 1rem;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .coverage-high { background: #d4edda; color: #155724; border: 2px solid #155724; }
    .coverage-partial { background: #fff3cd; color: #856404; border: 2px solid #856404; }
    .coverage-low { background: #f8d7da; color: #721c24; border: 2px solid #721c24; }
    .coverage-none { background: #e2e3e5; color: #383d41; border: 2px solid #383d41; }
    
    .section-header {
        background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .info-box {
        background: #f8f9fa;
        border-left: 4px solid #4facfe;
        padding: 1rem;
        border-radius: 0 0.5rem 0.5rem 0;
        margin: 1rem 0;
    }
    
    .commodity-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .commodity-category {
        font-size: 0.85rem;
        color: #667eea;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .commodity-name {
        font-size: 1rem;
        color: #1a1a2e;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    .coverage-meter {
        background: #e9ecef;
        border-radius: 0.5rem;
        height: 8px;
        margin-top: 0.5rem;
        overflow: hidden;
    }
    
    .coverage-fill {
        height: 100%;
        border-radius: 0.5rem;
    }
    
    .coverage-fill-high { background: linear-gradient(90deg, #51cf66 0%, #40c057 100%); }
    .coverage-fill-partial { background: linear-gradient(90deg, #ffd43b 0%, #fab005 100%); }
    .coverage-fill-low { background: linear-gradient(90deg, #ff6b6b 0%, #fa5252 100%); }
    .coverage-fill-none { background: #adb5bd; }
</style>
""", unsafe_allow_html=True)

# Load ONS coverage data
@st.cache_data
def load_ons_coverage():
    coverage_file = "data/output/ons_coverage_by_commodity_classified.csv"
    if os.path.exists(coverage_file):
        df = pd.read_csv(coverage_file)
        return df
    else:
        st.warning("Coverage data not found. Please run: python scripts/data_merge.py")
        return pd.DataFrame(columns=["commodity", "ons_coverage_pct", "coverage_class", "sitc_category"])

ons_coverage_df = load_ons_coverage()

# Helper functions
def get_coverage_badge(coverage_class):
    badges = {
        "High coverage": ("coverage-high", "HIGH COVERAGE"),
        "Partial coverage": ("coverage-partial", "PARTIAL COVERAGE"),
        "Low coverage": ("coverage-low", "LOW COVERAGE"),
        "No coverage": ("coverage-none", "NO COVERAGE")
    }
    css_class, label = badges.get(coverage_class, ("coverage-none", str(coverage_class)))
    return f'<span class="coverage-badge {css_class}">{label}</span>'

def get_risk_badge(risk_level):
    badges = {
        "HIGH": ("risk-high", "HIGH RISK"),
        "MODERATE": ("risk-moderate", "MODERATE RISK"),
        "LOW": ("risk-low", "LOW RISK")
    }
    css_class, label = badges.get(risk_level, ("risk-moderate", str(risk_level)))
    return f'<span class="risk-badge {css_class}">{label}</span>'

def get_coverage_color(coverage_class):
    colors = {
        "High coverage": "coverage-fill-high",
        "Partial coverage": "coverage-fill-partial",
        "Low coverage": "coverage-fill-low",
        "No coverage": "coverage-fill-none"
    }
    return colors.get(coverage_class, "coverage-fill-none")

def get_commodity_info(hs_code, coverage_df):
    """Get commodity information from coverage data."""
    row = coverage_df[coverage_df["commodity"] == hs_code]
    
    if len(row) > 0:
        row = row.iloc[0]
        return {
            "description": HS2_DESCRIPTIONS.get(hs_code, "Unknown"),
            "sitc_category": row.get("sitc_category", "Unknown"),
            "coverage_class": row.get("coverage_class", "No coverage"),
            "coverage_pct": row.get("ons_coverage_pct", 0),
            "total_years": row.get("total_years", 0),
            "covered_years": row.get("ons_covered_years", 0)
        }
    else:
        return {
            "description": HS2_DESCRIPTIONS.get(hs_code, "Unknown"),
            "sitc_category": "Unknown",
            "coverage_class": "No coverage",
            "coverage_pct": 0,
            "total_years": 0,
            "covered_years": 0
        }

# Header
st.markdown("# UK SME Import Margin Simulator")
st.markdown("*Analyse import profitability under various economic scenarios with risk classification and confidence bands*")

st.markdown("---")

# Sidebar inputs
with st.sidebar:
    st.markdown("## Simulation Parameters")
    st.markdown("---")
    
    st.markdown("### Financial Inputs")
    
    import_value = st.number_input(
        "Import Value (GBP)",
        value=1_000_000,
        step=50_000,
        format="%d",
        help="Total value of goods being imported (HMRC baseline)"
    )
    
    revenue = st.number_input(
        "Expected Revenue (GBP)",
        value=1_350_000,
        step=50_000,
        format="%d",
        help="Projected sales revenue from imported goods"
    )
    
    st.markdown("---")
    
    # Commodity selection
    st.markdown("### Select Your Commodity")
    
    # Get unique SITC categories from coverage data
    if len(ons_coverage_df) > 0 and "sitc_category" in ons_coverage_df.columns:
        sitc_categories = sorted(ons_coverage_df["sitc_category"].dropna().unique())
    else:
        sitc_categories = [
            "0 Food & live animals", "1 Beverages & tobacco", "2 Crude materials",
            "3 Fuels", "5 Chemicals", "6 Manufactured goods",
            "7 Machinery & transport equipment", "8 Miscellaneous manufactures", "9 Other commodities"
        ]
    
    selected_sitc = st.selectbox(
        "Product Category (SITC)",
        options=sitc_categories,
        index=0,
        help="Select the broad SITC category of your import goods"
    )
    
    # Filter HS codes by selected SITC category
    if len(ons_coverage_df) > 0:
        filtered_hs = ons_coverage_df[ons_coverage_df["sitc_category"] == selected_sitc]["commodity"].tolist()
    else:
        filtered_hs = list(range(1, 99))
    
    # Create dropdown options with descriptions
    hs_options = {
        f"HS {hs:02d} - {HS2_DESCRIPTIONS.get(hs, 'Unknown')}": hs 
        for hs in sorted(filtered_hs) if hs in HS2_DESCRIPTIONS
    }
    
    if hs_options:
        selected_hs_label = st.selectbox(
            "Specific Commodity (HS Code)",
            options=list(hs_options.keys()),
            help="Select the specific HS2 chapter for your goods"
        )
        commodity_code = hs_options[selected_hs_label]
    else:
        commodity_code = st.number_input("HS Code", value=1, min_value=1, max_value=99)
    
    # Get commodity info
    commodity_info = get_commodity_info(commodity_code, ons_coverage_df)
    coverage_class = commodity_info["coverage_class"]
    coverage_pct = commodity_info["coverage_pct"]
    
    # Display commodity card
    st.markdown(f"""
    <div class="commodity-card">
        <div class="commodity-category">{commodity_info['sitc_category']}</div>
        <div class="commodity-name">HS {commodity_code:02d}: {commodity_info['description']}</div>
        <div style="margin-top: 0.75rem;">
            {get_coverage_badge(coverage_class)}
        </div>
        <div class="coverage-meter">
            <div class="coverage-fill {get_coverage_color(coverage_class)}" style="width: {coverage_pct}%;"></div>
        </div>
        <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
            ONS Data Coverage: {coverage_pct:.1f}% ({commodity_info['covered_years']}/{commodity_info['total_years']} years)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Cost Assumptions")
    
    fx_shock = st.slider(
        "FX Shock (%)",
        min_value=-20.0,
        max_value=20.0,
        value=0.0,
        step=0.5,
        help="Currency fluctuation impact (+ve = weaker GBP)"
    )
    
    shipping_pct = st.slider(
        "Shipping Cost (%)",
        min_value=0.0,
        max_value=30.0,
        value=5.0,
        step=0.5,
        help="Freight cost as percentage of goods value"
    )
    
    insurance_pct = st.slider(
        "Insurance Cost (%)",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Insurance premium as percentage of goods value"
    )
    
    tariff_pct = st.slider(
        "Tariff Rate (%)",
        min_value=0.0,
        max_value=25.0,
        value=2.0,
        step=0.5,
        help="Import duty as percentage of goods value"
    )
    
    st.markdown("---")
    st.caption("Data sources: HMRC (values), ONS (coverage reliability)")

# Calculate base scenario
base_result = compute_margin(
    import_value_gbp=import_value,
    revenue_gbp=revenue,
    fx_shock_pct=fx_shock / 100,
    shipping_pct=shipping_pct / 100,
    insurance_pct=insurance_pct / 100,
    tariff_pct=tariff_pct / 100,
)

profit = base_result["profit"]
margin_pct = base_result["margin_pct"] if base_result["margin_pct"] is not None else 0.0
landed_cost = base_result["landed_cost"]
goods_cost = base_result["goods_cost"]
shipping_cost = base_result["shipping_cost"]
insurance_cost = base_result["insurance_cost"]
tariff_cost = base_result["tariff_cost"]

# Risk Assessment
base_risk = risk_label(margin_pct)
final_risk = adjust_risk(base_risk, coverage_class)
uncertainty = confidence_multiplier(coverage_class)

# Main dashboard

st.markdown('<div class="section-header">Key Performance Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    profit_color = "metric-card-profit" if profit >= 0 else "metric-card-loss"
    st.markdown(f"""
    <div class="metric-card {profit_color}">
        <div class="metric-label">Net Profit</div>
        <div class="metric-value">GBP {profit:,.0f}</div>
        <div class="metric-label">{"Profitable" if profit >= 0 else "Loss"}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-card-margin">
        <div class="metric-label">Profit Margin</div>
        <div class="metric-value">{margin_pct:.1f}%</div>
        <div class="metric-label">of revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-card-cost">
        <div class="metric-label">Landed Cost</div>
        <div class="metric-value">GBP {landed_cost:,.0f}</div>
        <div class="metric-label">total import cost</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card metric-card-revenue">
        <div class="metric-label">Expected Revenue</div>
        <div class="metric-value">GBP {revenue:,.0f}</div>
        <div class="metric-label">projected sales</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Two column layout for details
left_col, right_col = st.columns([1, 1])

# Cost breakdown chart
with left_col:
    st.markdown('<div class="section-header">Cost Breakdown</div>', unsafe_allow_html=True)
    
    cost_items = ['Import Value', 'FX Impact', 'Shipping', 'Insurance', 'Tariffs', 'Landed Cost']
    cost_values = [
        import_value,
        goods_cost - import_value,
        shipping_cost,
        insurance_cost,
        tariff_cost,
        0
    ]
    
    fig_waterfall = go.Figure(go.Waterfall(
        name="Cost Breakdown",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "total"],
        x=cost_items,
        y=cost_values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#ff6b6b"}},
        decreasing={"marker": {"color": "#51cf66"}},
        totals={"marker": {"color": "#339af0"}},
        text=[f"GBP {v:,.0f}" if i < 5 else f"GBP {landed_cost:,.0f}" for i, v in enumerate(cost_values)],
        textposition="outside"
    ))
    
    fig_waterfall.update_layout(
        title="Cost Build-up to Landed Cost",
        showlegend=False,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_waterfall, use_container_width=True)
    
    # Cost summary table
    cost_data = pd.DataFrame({
        "Component": ["Goods (after FX)", "Shipping", "Insurance", "Tariffs", "Total Landed Cost"],
        "Amount (GBP)": [f"{goods_cost:,.0f}", f"{shipping_cost:,.0f}", f"{insurance_cost:,.0f}", 
                        f"{tariff_cost:,.0f}", f"{landed_cost:,.0f}"],
        "% of Import": [f"{(goods_cost/import_value)*100:.1f}%", f"{(shipping_cost/import_value)*100:.1f}%",
                        f"{(insurance_cost/import_value)*100:.1f}%", f"{(tariff_cost/import_value)*100:.1f}%",
                        f"{(landed_cost/import_value)*100:.1f}%"]
    })
    st.dataframe(cost_data, hide_index=True, use_container_width=True)

# Risk assessment
with right_col:
    st.markdown('<div class="section-header">Risk Assessment</div>', unsafe_allow_html=True)
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.markdown("**Financial Risk**")
        st.markdown("<small>Based on profit margin</small>", unsafe_allow_html=True)
        st.markdown(get_risk_badge(base_risk), unsafe_allow_html=True)
        
    with risk_col2:
        st.markdown("**Adjusted Risk**")
        st.markdown("<small>Accounting for data quality</small>", unsafe_allow_html=True)
        st.markdown(get_risk_badge(final_risk), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quality descriptions
    quality_description = {
        "High coverage": ("excellent", "reliable", "narrow"),
        "Partial coverage": ("moderate", "reasonably reliable", "moderately widened"),
        "Low coverage": ("limited", "less reliable", "significantly widened"),
        "No coverage": ("no", "unreliable", "maximally widened")
    }
    
    qual_level, qual_reliability, qual_bands = quality_description.get(
        coverage_class, ("unknown", "uncertain", "widened")
    )
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Data Quality Assessment</strong><br><br>
        <strong>Commodity:</strong> HS {commodity_code:02d} - {commodity_info['description']}<br>
        <strong>ONS Coverage:</strong> {get_coverage_badge(coverage_class)}<br><br>
        <strong>What this means:</strong><br>
        ONS provides <strong>{qual_level}</strong> statistical coverage for this commodity, 
        meaning historical data is <strong>{qual_reliability}</strong>.<br><br>
        <strong>Confidence Adjustment:</strong> +/- {uncertainty*100:.0f}%<br>
        <small>Profit and margin confidence bands are <strong>{qual_bands}</strong> to reflect data quality.</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Profit gauge
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=margin_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Profit Margin (%)"},
        delta={'reference': 10, 'increasing': {'color': "#51cf66"}, 'decreasing': {'color': "#ff6b6b"}},
        gauge={
            'axis': {'range': [-20, 40], 'tickwidth': 1},
            'bar': {'color': "#339af0"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [-20, 0], 'color': '#ff6b6b'},
                {'range': [0, 5], 'color': '#ffd43b'},
                {'range': [5, 10], 'color': '#ffe066'},
                {'range': [10, 40], 'color': '#8ce99a'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': margin_pct
            }
        }
    ))
    
    fig_gauge.update_layout(
        height=280,
        margin=dict(t=50, b=20, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)

# Scenario analysis
st.markdown('<div class="section-header">Scenario Analysis</div>', unsafe_allow_html=True)

# Run sensitivity scenarios
df = run_sensitivity_scenarios(
    import_value_gbp=import_value,
    revenue_gbp=revenue,
)

# Calculate confidence bands
df["profit_lower"] = df["profit"] - abs(df["profit"]) * uncertainty
df["profit_upper"] = df["profit"] + abs(df["profit"]) * uncertainty
df["margin_lower"] = df["margin_pct"] - abs(df["margin_pct"]) * uncertainty
df["margin_upper"] = df["margin_pct"] + abs(df["margin_pct"]) * uncertainty

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Margin Heatmap", "Sensitivity Charts", "Data Table"])

with tab1:
    pivot_margin = df.pivot_table(
        values='margin_pct', 
        index='fx_shock_pct', 
        columns='shipping_pct',
        aggfunc='mean'
    )
    
    fig_heatmap = px.imshow(
        pivot_margin,
        labels=dict(x="Shipping Cost (%)", y="FX Shock (%)", color="Margin (%)"),
        x=[f"{x:.0f}%" for x in pivot_margin.columns],
        y=[f"{y:.0f}%" for y in pivot_margin.index],
        color_continuous_scale="RdYlGn",
        aspect="auto"
    )
    
    fig_heatmap.update_layout(
        title="Profit Margin by FX Shock and Shipping Cost",
        height=500,
        margin=dict(t=60, b=50, l=80, r=50),
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.caption(f"Confidence bands: +/- {uncertainty*100:.0f}% based on ONS coverage ({coverage_class})")

with tab2:
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        df_fx0 = df[df['fx_shock_pct'] == 0].sort_values('shipping_pct')
        
        fig_shipping = go.Figure()
        
        fig_shipping.add_trace(go.Scatter(
            x=df_fx0['shipping_pct'],
            y=df_fx0['margin_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_shipping.add_trace(go.Scatter(
            x=df_fx0['shipping_pct'],
            y=df_fx0['margin_lower'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(51, 154, 240, 0.2)',
            name=f'Confidence Band (+/- {uncertainty*100:.0f}%)'
        ))
        
        fig_shipping.add_trace(go.Scatter(
            x=df_fx0['shipping_pct'],
            y=df_fx0['margin_pct'],
            mode='lines+markers',
            name='Margin %',
            line=dict(color='#339af0', width=3),
            marker=dict(size=8)
        ))
        
        fig_shipping.add_hline(y=0, line_dash="dash", line_color="red", 
                               annotation_text="Break-even", annotation_position="right")
        
        fig_shipping.update_layout(
            title="Margin vs Shipping Cost (0% FX)",
            xaxis_title="Shipping Cost (%)",
            yaxis_title="Profit Margin (%)",
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_shipping, use_container_width=True)
    
    with trend_col2:
        df_ship5 = df[abs(df['shipping_pct'] - 5) < 1].sort_values('fx_shock_pct')
        
        if df_ship5.empty:
            df_ship5 = df[df['shipping_pct'] == df['shipping_pct'].min()].sort_values('fx_shock_pct')
        
        fig_fx = go.Figure()
        
        fig_fx.add_trace(go.Scatter(
            x=df_ship5['fx_shock_pct'],
            y=df_ship5['margin_upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_fx.add_trace(go.Scatter(
            x=df_ship5['fx_shock_pct'],
            y=df_ship5['margin_lower'],
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 107, 107, 0.2)',
            name=f'Confidence Band (+/- {uncertainty*100:.0f}%)'
        ))
        
        fig_fx.add_trace(go.Scatter(
            x=df_ship5['fx_shock_pct'],
            y=df_ship5['margin_pct'],
            mode='lines+markers',
            name='Margin %',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ))
        
        fig_fx.add_hline(y=0, line_dash="dash", line_color="red",
                         annotation_text="Break-even", annotation_position="right")
        
        fig_fx.update_layout(
            title="Margin vs FX Shock (5% Shipping)",
            xaxis_title="FX Shock (%)",
            yaxis_title="Profit Margin (%)",
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_fx, use_container_width=True)

with tab3:
    st.markdown("#### Full Scenario Data")
    
    display_df = df.copy()
    display_df = display_df.round(2)
    display_df.columns = ['FX Shock (%)', 'Shipping (%)', 'Profit (GBP)', 'Margin (%)', 
                          'Profit Lower (GBP)', 'Profit Upper (GBP)', 'Margin Lower (%)', 'Margin Upper (%)']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download Scenario Data (CSV)",
        data=csv,
        file_name=f"import_scenarios_hs{commodity_code}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **Data Sources**
    - HMRC: Import valuations (baseline)
    - ONS: Coverage reliability metrics
    """)

with footer_col2:
    st.markdown("""
    **Core Model**
    - Landed cost calculation
    - Risk-adjusted margins
    - Confidence bands
    """)

with footer_col3:
    st.markdown("""
    **Disclaimer**
    - Simulations only, not financial advice
    - Results depend on input assumptions
    """)

st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | UK SME Import Margin Simulator v1.0")
