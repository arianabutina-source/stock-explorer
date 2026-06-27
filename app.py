import base64
import time
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
import yfinance as yf

def _svg_b64(name):
    path = Path(__file__).parent / "logos" / f"{name}.svg"
    return base64.b64encode(path.read_bytes()).decode()

def inject_logo_background():
    logos = [
        ("apple",     "20%", "5%",  "120px"),
        ("google",    "20%", "72%", "180px"),
        ("microsoft", "45%", "88%", "100px"),
        ("netflix",   "65%", "3%",  "160px"),
        ("amazon",    "82%", "65%", "170px"),
        ("meta",      "95%", "30%", "150px"),
    ]
    imgs = "".join(
        f'<img src="data:image/svg+xml;base64,{_svg_b64(name)}" '
        f'style="position:fixed;top:{top};left:{left};width:{w};opacity:0.06;pointer-events:none;z-index:0;">'
        for name, top, left, w in logos
    )
    st.markdown(f'<div style="position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:0;">{imgs}</div>',
                unsafe_allow_html=True)

DID_YOU_KNOW = [
    "🍎 Ronald Wayne, Apple's third co-founder, sold his 10% share back for just $800 — twelve days after co-founding the company.",
    "🍎 Steve Wozniak priced the original Apple I at $666.66 because he liked repeating digits, unaware of the coincidental biblical reference.",
    "🍎 Steve Jobs let Xerox view Apple's pre-IPO shares in exchange for a peek at their graphical interface technology — which inspired the Mac.",
    "🍎 Apple's iconic '1984' Super Bowl ad cost $1.5 million to air and is widely considered one of the greatest TV commercials ever made.",
    "🍎 When Apple surpassed Dell's market value in 2006, Jobs emailed employees referencing Dell CEO's earlier advice to 'shut it down and give the money back.'",
    "🪟 Microsoft's 1986 IPO created an estimated 12,000 employee millionaires, with shares jumping from $21 to $27.75 on day one.",
    "🪟 Co-founder Paul Allen left Microsoft in 1983 after being diagnosed with Hodgkin's lymphoma, one of tech's earliest health-driven startup exits.",
    "🪟 In 2001 Steve Ballmer called Linux 'cancer' — yet by 2016 Microsoft had joined the Linux Foundation as a Platinum member.",
    "🪟 Microsoft posted its first-ever quarterly loss in July 2012 solely due to a $6.2 billion writedown from its acquisition of ad firm aQuantive.",
    "🪟 Bill Gates' 1995 'Internet Tidal Wave' memo triggered a full company pivot to the web, helping Microsoft dominate as Netscape and Borland faded.",
    "🔍 Google was nearly called 'BackRub' — and the founders almost sold the company to Yahoo for just $1 million in 1998.",
    "🔍 The name 'Google' came from a misspelling of 'googol' (10¹⁰⁰), reflecting the founders' ambition to index vast amounts of information.",
    "🔍 Google's first office was Susan Wojcicki's garage in Menlo Park, rented for $1,700 a month in 1998.",
    "🔍 Scott Hassan wrote much of the original Google Search code but left before incorporation — he later founded robotics firm Willow Garage.",
    "🔍 'Google' was added to the Merriam-Webster and Oxford English Dictionaries in 2006, cementing its place as an everyday verb.",
    "📦 Amazon was originally called 'Cadabra' and founded in Jeff Bezos's Bellevue garage before being renamed after the river in late 1994.",
    "📦 Bezos registered www.relentless.com while brainstorming names — it still redirects to Amazon's homepage today.",
    "📦 Amazon launched publicly on July 16, 1995, initially sourcing books directly from wholesalers rather than holding any inventory.",
    "📦 Amazon's Seattle HQ was nicknamed 'Rufus 2.0' after a beloved dog who was a fixture of the company in its early days.",
    "📦 A 2006 court awarded Toys 'R' Us $51 million in damages after ruling Amazon violated an exclusive product category agreement.",
    "🎬 When Netflix launched streaming in 2007, it offered only 1,000 films — compared to 70,000 titles available on DVD.",
    "🎬 Netflix delivered its one-billionth DVD in February 2007 — a copy of 'Babel' shipped to a customer in Texas.",
    "🎬 Netflix's 2011 attempt to spin off its DVD service as 'Qwikster' was abandoned after 800,000 customers cancelled subscriptions in protest.",
    "🎬 Netflix's DVD-by-mail service shipped over 5 billion discs across its lifetime before finally shutting down in September 2023.",
    "🎬 Netflix's first-ever acquisition was Millarworld, a comic book publisher, in August 2017 — a major step toward owning its own IP.",
    "👤 Facebook's original motto was 'Move fast and break things' — Zuckerberg replaced it in 2014 with 'Move fast with stable infrastructure.'",
    "👤 Facebook's 2012 IPO raised $16 billion (the third-largest in U.S. history), yet underwriters had to buy shares on day one to stop it falling below the offer price.",
    "👤 Meta spent hundreds of millions on VR content before realising it hadn't caught on, prompting a costly pivot toward the broader metaverse.",
    "👤 Meta rebranded from Facebook in October 2021 partly to distance itself from a major whistleblower leak and growing scrutiny over mental health harms.",
    "👤 In 2022, Zuckerberg laid off 11,000 employees — 13% of Meta's workforce — admitting he had wrongly bet that pandemic e-commerce growth would persist.",
]

st.set_page_config(page_title="Stock Explorer", layout="wide")
inject_logo_background()

st.markdown("""
<style>
/* ── Mobile-first responsive tweaks ── */
@media (max-width: 768px) {
    /* Tighten main padding */
    .block-container { padding: 1rem 0.75rem !important; }

    /* Title */
    h1 { font-size: 1.4rem !important; }

    /* Metric cards: wrap into a 3-column grid */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 28% !important;
        min-width: 90px !important;
    }
    [data-testid="stMetric"] { font-size: 0.75rem !important; }
    [data-testid="stMetricValue"] { font-size: 1rem !important; }

    /* Multiselect full width */
    [data-testid="stMultiSelect"] { width: 100% !important; }

    /* Shrink logo watermarks on mobile */
    div[style*="position:fixed"] img {
        width: 70px !important;
        opacity: 0.04 !important;
    }

    /* Banners */
    [data-testid="stAlert"] { font-size: 0.85rem !important; }

    /* Range slider smaller */
    .js-plotly-plot { font-size: 0.75rem !important; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;font-family:cursive;'>Stock Price Explorer</h1>", unsafe_allow_html=True)

TICKERS = {"AAPL": "Apple", "MSFT": "Microsoft", "GOOG": "Google", "AMZN": "Amazon", "NFLX": "Netflix", "META": "Meta", "SP500": "S&P 500", "DJI": "Dow Jones", "NASDAQ": "Nasdaq", "TQQQ": "TQQQ"}

@st.cache_data
def load_data():
    symbols = ["AAPL", "MSFT", "GOOG", "AMZN", "NFLX", "META", "^GSPC", "^DJI", "^IXIC", "TQQQ"]
    raw = yf.download(symbols, start="2018-01-01", end="2026-06-27", auto_adjust=True)["Close"]
    raw = raw.rename(columns={"^GSPC": "SP500", "^DJI": "DJI", "^IXIC": "NASDAQ"})
    raw = raw.dropna()
    df = raw / raw.iloc[0]
    df.index.name = "date"
    df = df.reset_index()
    return df

df = load_data()
tickers = list(TICKERS.keys())

chosen = st.multiselect("Choose stocks", tickers, default=tickers)
if not chosen:
    st.warning("Pick at least one stock.")
    st.stop()

dff = df.copy()
for t in tickers:
    dff[t] = dff[t] / dff[t].iloc[0]

st.caption("Prices re-indexed to 1.00 on Jan 2018, showing growth to Jun 2026.")

# Compact stock chips — click to reveal metrics
n_cols = min(len(chosen), 5)
rows = [chosen[i:i+n_cols] for i in range(0, len(chosen), n_cols)]
for row in rows:
    cols = st.columns(len(row))
    for col, t in zip(cols, row):
        with col:
            with st.popover(t, use_container_width=True):
                growth = (dff[t].iloc[-1] - 1) * 100
                st.metric(t, f"{dff[t].iloc[-1]:.2f}x", f"{growth:+.1f}%")

# Top and bottom performer banners
top = max(chosen, key=lambda t: dff[t].iloc[-1])
top_growth = (dff[top].iloc[-1] - 1) * 100
st.success(f"Top performer: **{top}** — grew {top_growth:+.1f}% in the selected period")

bottom = min(chosen, key=lambda t: dff[t].iloc[-1])
bottom_growth = (dff[bottom].iloc[-1] - 1) * 100
st.warning(f"Least growth: **{bottom}** — grew {bottom_growth:+.1f}% in the selected period")

# Line chart comparing the chosen stocks over selected timeframe
dff["Average"] = dff[tickers].mean(axis=1)
fig = px.line(dff, x="date", y=chosen, title="Normalized price over time")
fig.add_scatter(x=dff["date"], y=dff["Average"], mode="lines", name="Average",
                line=dict(color="black", width=3))
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig, width='stretch')

@st.fragment(run_every=30)
def did_you_know():
    idx = int(time.time() // 30) % len(DID_YOU_KNOW)
    st.info(f"💡 Did you know? {DID_YOU_KNOW[idx]}")

did_you_know()
