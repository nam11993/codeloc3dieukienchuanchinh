import streamlit as st#!/usr/bin/env python3#!/usr/bin/env python3

import os

from scanner_core import Scanner""""""



# Streamlit web application for code scanningVietnamese Stock Scanner Web App - Simple VersionStock Scanner Web App - Streamlit Interface

st.title("Code Location Scanner")

st.write("Scan directories and analyze code structure")Webapp đơn giản để quét cổ phiếu Việt Nam (không có chart)Web version của Telegram bot với 2 bộ lọc: MUA 1 và MUA SỊN



# Initialize scanner""""""

scanner = Scanner()

import streamlit as stimport streamlit as st

# Sidebar for configuration

st.sidebar.header("Configuration")import pandas as pdimport pandas as pd

directory_path = st.sidebar.text_input("Directory Path", value=".")

import jsonimport datetime

# Main content

if st.button("Scan Directory"):import timeimport time

    if os.path.exists(directory_path):

        st.write(f"Scanning: {directory_path}")from datetime import datetimeimport requests

        

        results = scanner.scan_directory(directory_path)import plotly.graph_objects as go

        

        if results:# Import từ app.py gốcfrom plotly.subplots import make_subplots

            st.success(f"Found {len(results)} files")

            from app import (import streamlit.components.v1 as components

            # Display results in a table

            st.subheader("Scan Results")    fetch_all_symbols, fetch_symbol_bundle, apply_filters, apply_filters_sin,from scanner_core import fetch_all_symbols, scan_symbols, get_chart_data

            for result in results[:20]:  # Limit to first 20 results

                st.write(f"📁 {result['name']} - {result['size']} bytes")    scan_symbols, scan_symbols_sin

                

            if len(results) > 20:)# =====================

                st.info(f"Showing first 20 of {len(results)} files")

        else:# Streamlit Config

            st.warning("No files found")

    else:# =====================

        st.error("Directory does not exist")# Page Config

# =====================

# Display scanner infost.set_page_config(

st.sidebar.info(scanner.get_info())    page_title="Lọc Cổ Phiếu VN",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# Helper Functions
# =====================

# Custom CSS

# =====================def get_cafef_data(symbol, days=60):

st.markdown("""    """

<style>    Lấy dữ liệu từ CafeF API làm backup

    .main-header {    """

        font-size: 2.5rem;    try:

        font-weight: bold;        # Tính ngày bắt đầu và kết thúc

        color: #1f77b4;        end_date = datetime.datetime.now()

        text-align: center;        start_date = end_date - datetime.timedelta(days=days)

        margin-bottom: 1rem;        

    }        # Format dates cho CafeF API (MM/dd/yyyy)

    .metric-container {        start_str = start_date.strftime("%m/%d/%Y")

        background-color: #f0f2f6;        end_str = end_date.strftime("%m/%d/%Y")

        padding: 1rem;        

        border-radius: 0.5rem;        # CafeF API URL

        margin: 0.5rem 0;        url = f"https://s.cafef.vn/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={symbol}&StartDate={start_str}&EndDate={end_str}&PageIndex=0&PageSize={days*2}"

    }        

    .signal-positive {        response = requests.get(url, timeout=15)

        background-color: #d4edda;        

        color: #155724;        if response.status_code == 200:

        padding: 0.5rem;            data = response.json()

        border-radius: 0.25rem;            

        margin: 0.25rem 0;            if data.get('Success') and data.get('Data') and data['Data'].get('Data'):

    }                records = data['Data']['Data']

    .signal-negative {                

        background-color: #f8d7da;                # Parse dữ liệu

        color: #721c24;                parsed_data = []

        padding: 0.5rem;                for record in records:

        border-radius: 0.25rem;                    try:

        margin: 0.25rem 0;                        # Parse date - CafeF trả về format dd/mm/yyyy hoặc mm/dd/yyyy

    }                        date_str = record['Ngay']

</style>                        try:

""", unsafe_allow_html=True)                            date_obj = datetime.datetime.strptime(date_str, "%m/%d/%Y")

                        except ValueError:

# =====================                            date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")

# Helper Functions                        

# =====================                        parsed_data.append({

@st.cache_data(ttl=300)  # Cache 5 phút                            'date': date_obj,

def load_symbols():                            'open': record['GiaMoCua'],

    """Load danh sách cổ phiếu"""                            'high': record['GiaCaoNhat'], 

    try:                            'low': record['GiaThapNhat'],

        symbols = fetch_all_symbols()                            'close': record['GiaDieuChinh'],

        return symbols                            'volume': record['KhoiLuongKhopLenh']

    except Exception as e:                        })

        st.error(f"Lỗi load symbols: {e}")                    except Exception:

        return []                        continue

                

def format_signal_result(result):                if parsed_data:

    """Format kết quả signal để hiển thị"""                    # Tạo DataFrame và sort theo date

    if not result:                    df = pd.DataFrame(parsed_data)

        return "❌ Không có tín hiệu"                    df = df.sort_values('date').reset_index(drop=True)

                        

    formatted = []                    # Tính toán indicators cơ bản

    for key, value in result.items():                    df['ma20'] = df['close'].rolling(20).mean()

        if isinstance(value, bool):                    df['ma30'] = df['close'].rolling(30).mean()

            emoji = "✅" if value else "❌"                    

            formatted.append(f"{emoji} {key}")                    # Format output giống scanner_core

        else:                    result = {

            formatted.append(f"📊 {key}: {value}")                        'symbol': symbol,

                            'dates': df['date'].dt.strftime('%Y-%m-%d').tolist(),

    return " | ".join(formatted)                        'open': df['open'].tolist(),

                        'high': df['high'].tolist(),

def run_scanner(filter_type, max_symbols=50):                        'low': df['low'].tolist(),

    """Chạy scanner với loại filter được chọn"""                        'close': df['close'].tolist(),

                            'volume': df['volume'].tolist(),

    # Load symbols                        'ma20': df['ma20'].fillna(0).tolist(),

    symbols = load_symbols()                        'ma30': df['ma30'].fillna(0).tolist(),

    if not symbols:                        'latest_price': float(df['close'].iloc[-1]),

        st.error("Không thể load danh sách cổ phiếu")                        'latest_change': float((df['close'].iloc[-1] / df['close'].iloc[-2] - 1) * 100) if len(df) >= 2 else 0

        return []                    }

                        

    # Giới hạn số lượng để tránh timeout                    return result

    symbols = symbols[:max_symbols]        

    symbol_codes = [s.code if hasattr(s, 'code') else s['code'] for s in symbols]        return {'error': f'CafeF API không thể lấy dữ liệu cho {symbol}'}

                

    # Progress bar    except Exception as e:

    progress_bar = st.progress(0)        return {'error': f'Lỗi CafeF API: {e}'}

    status_text = st.empty()

    def format_price(price):

    results = []    """Format giá cổ phiếu"""

    total_symbols = len(symbol_codes)    return f"{price:,.1f}₫"

    

    try:def format_percent(pct):

        if filter_type == "MUA 1":    """Format phần trăm với màu sắc"""

            status_text.text("🔍 Đang quét với bộ lọc MUA 1...")    if pct > 2:

            results = scan_symbols(symbol_codes)        return f"🟢 **+{pct:.2f}%**"

        elif filter_type == "MUA SỊN":    elif pct > 0:

            status_text.text("🔍 Đang quét với bộ lọc MUA SỊN...")        return f"🟡 **+{pct:.2f}%**"

            results = scan_symbols_sin(symbol_codes)    elif pct > -2:

                return f"🟠 **{pct:.2f}%**"

        progress_bar.progress(1.0)    else:

        status_text.text(f"✅ Hoàn thành quét {total_symbols} mã")        return f"🔴 **{pct:.2f}%**"

        

    except Exception as e:def create_results_dataframe(results, filter_type):

        st.error(f"Lỗi khi quét: {e}")    """Tạo DataFrame để hiển thị kết quả"""

        results = []    if not results:

            return pd.DataFrame()

    return results    

    data = []

# =====================    for r in results:

# Main App        signals = []

# =====================        

def main():        if filter_type == "mua1":

    # Header            if r["BuyBreak"]:

    st.markdown('<div class="main-header">📈 Lọc Cổ Phiếu Việt Nam</div>', unsafe_allow_html=True)                signals.append("🚀 Mua Break")

                if r["BuyNormal"]:

    # Sidebar                signals.append("📈 Mua Thường")

    with st.sidebar:            if r["Sell"]:

        st.header("⚙️ Cài đặt")                signals.append("📉 Bán")

                    if r["Short"]:

        # Chọn loại filter                signals.append("🔻 Short")

        filter_type = st.selectbox(            if r["Cover"]:

            "Chọn bộ lọc:",                signals.append("📈 Cover")

            ["MUA 1", "MUA SỊN"],            if r["Sideway"]:

            help="MUA 1: Bộ lọc chuẩn\nMUA SỊN: Bộ lọc nghiêm ngặt"                signals.append("↔️ Sideway")

        )        else:  # muasin

                    if r["BuySin"]:

        # Số lượng mã quét                signals.append("🔥 Mua Sịn")

        max_symbols = st.slider(        

            "Số mã quét tối đa:",        data.append({

            min_value=10,            "Mã": r["symbol"],

            max_value=200,            "Giá": f"{r['price']:,.1f}",

            value=50,            "Thay đổi (%)": f"{r['pct']:+.2f}%",

            step=10,            "Tín hiệu": " • ".join(signals) if signals else "❓"

            help="Giới hạn số mã để tránh timeout"        })

        )    

            return pd.DataFrame(data)

        # Button quét

        scan_button = st.button("🚀 Bắt đầu quét", type="primary")def create_stock_chart(symbol: str):

            """Tạo chart cho một mã cổ phiếu với Plotly - có fallback từ CafeF"""

        # Thông tin    with st.spinner(f"📊 Đang tải chart {symbol}..."):

        st.info("""        # Thử VNDIRECT trước (primary)

        **Hướng dẫn:**        chart_data = get_chart_data(symbol, days=60)

        1. Chọn loại bộ lọc        data_source = "VNDIRECT"

        2. Điều chỉnh số mã quét        

        3. Nhấn "Bắt đầu quét"        # Nếu VNDIRECT failed, thử CafeF (fallback)

                if "error" in chart_data:

        **Bộ lọc:**            st.warning(f"⚠️ VNDIRECT API lỗi, đang thử CafeF...")

        - **MUA 1**: Tín hiệu mua chuẩn            chart_data = get_cafef_data(symbol, days=60)

        - **MUA SỊN**: Tín hiệu mua nghiêm ngặt            data_source = "CafeF"

        """)            

                if "error" in chart_data:

    # Main content                st.error(f"❌ Không thể tải chart cho mã **{symbol}**")

    col1, col2 = st.columns([2, 1])                st.warning(f"⚠️ VNDIRECT: Lỗi API")

                    st.warning(f"⚠️ CafeF: {chart_data['error']}")

    with col2:                st.info("💡 **Gợi ý**: Hãy thử với mã cổ phiếu khác (VD: VCB, VIC, HPG, MSN)")

        st.subheader("📊 Thống kê")                return

                

        # Hiển thị thời gian cập nhật        # Hiển thị thông tin nguồn dữ liệu

        st.metric(        st.success(f"✅ Dữ liệu từ **{data_source}** - {len(chart_data['dates'])} ngày")

            label="Thời gian cập nhật",        

            value=datetime.now().strftime("%H:%M:%S")        # Tạo subplot với 2 hàng: Price + Volume, RSI

        )        fig = make_subplots(

                    rows=3, cols=1,

        # Load symbols để hiển thị thống kê            subplot_titles=(f'{symbol} - Giá & Chỉ báo', 'Volume', 'RSI'),

        symbols = load_symbols()            vertical_spacing=0.05,

        st.metric(            row_heights=[0.6, 0.2, 0.2],

            label="Tổng số mã",            specs=[[{"secondary_y": False}],

            value=len(symbols) if symbols else 0                   [{"secondary_y": False}], 

        )                   [{"secondary_y": False}]]

            )

    with col1:        

        st.subheader(f"🎯 Kết quả quét - {filter_type}")        # 1. Candlestick chart

                fig.add_trace(

        # Nếu nhấn button quét            go.Candlestick(

        if scan_button:                x=chart_data["dates"],

            with st.spinner(f"Đang quét với bộ lọc {filter_type}..."):                open=chart_data["open"],

                results = run_scanner(filter_type, max_symbols)                high=chart_data["high"],

                            low=chart_data["low"],

            # Hiển thị kết quả                close=chart_data["close"],

            if results:                name="OHLC",

                st.success(f"🎉 Tìm thấy {len(results)} tín hiệu!")                showlegend=False

                            ),

                # Tạo DataFrame để hiển thị            row=1, col=1

                df_results = []        )

                for result in results:        

                    if isinstance(result, dict):        # 2. Moving Averages

                        symbol = result.get('symbol', 'N/A')        fig.add_trace(

                        signals = {k: v for k, v in result.items() if k != 'symbol'}            go.Scatter(

                        df_results.append({                x=chart_data["dates"],

                            'Mã CK': symbol,                y=chart_data["ma20"],

                            'Tín hiệu': format_signal_result(signals)                name="MA20",

                        })                line=dict(color="orange", width=1),

                    else:                opacity=0.8

                        # Nếu result chỉ là string symbol            ),

                        df_results.append({            row=1, col=1

                            'Mã CK': result,        )

                            'Tín hiệu': '✅ Đạt điều kiện'        

                        })        fig.add_trace(

                            go.Scatter(

                if df_results:                x=chart_data["dates"],

                    df = pd.DataFrame(df_results)                y=chart_data["ma30"],

                    st.dataframe(                name="MA30",

                        df,                line=dict(color="blue", width=1),

                        use_container_width=True,                opacity=0.8

                        hide_index=True            ),

                    )            row=1, col=1

                            )

                    # Download button        

                    csv = df.to_csv(index=False, encoding='utf-8-sig')        fig.add_trace(

                    st.download_button(            go.Scatter(

                        label="📥 Tải xuống CSV",                x=chart_data["dates"],

                        data=csv,                y=chart_data["ema34"],

                        file_name=f"ket_qua_loc_{filter_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",                name="EMA34",

                        mime="text/csv"                line=dict(color="red", width=2),

                    )                opacity=0.9

            else:            ),

                st.warning("❌ Không tìm thấy tín hiệu nào thỏa mãn điều kiện")            row=1, col=1

                )

        else:        

            # Hiển thị placeholder khi chưa quét        # 3. Volume

            st.info("👆 Nhấn 'Bắt đầu quét' để tìm tín hiệu cổ phiếu")        colors = ['red' if close < open else 'green' for close, open in zip(chart_data["close"], chart_data["open"])]

                    fig.add_trace(

            # Hiển thị thông tin về bộ lọc đã chọn            go.Bar(

            if filter_type == "MUA 1":                x=chart_data["dates"],

                st.markdown("""                y=chart_data["volume"],

                **Bộ lọc MUA 1:**                name="Volume",

                - Giá tăng 4 ngày liên tiếp                marker_color=colors,

                - Giá trên MA30                opacity=0.6,

                - Không tăng quá 4% ngày trước                showlegend=False

                - Có breakout hoặc không breakout            ),

                """)            row=2, col=1

            else:        )

                st.markdown("""        

                **Bộ lọc MUA SỊN:**        # Volume MA20

                - High >= High[-4] × 99%        fig.add_trace(

                - Giá tăng hôm nay            go.Scatter(

                - Nến đỏ hôm qua                x=chart_data["dates"],

                - Giảm tối đa 2% hôm qua                y=chart_data["vol_ma20"],

                - Volume thấp hôm qua                name="Vol MA20",

                - Trên EMA34                line=dict(color="purple", width=1),

                """)                opacity=0.8

            ),

if __name__ == "__main__":            row=2, col=1

    main()        )
        
        # 4. RSI
        fig.add_trace(
            go.Scatter(
                x=chart_data["dates"],
                y=chart_data["rsi"],
                name="RSI",
                line=dict(color="purple", width=2),
                showlegend=False
            ),
            row=3, col=1
        )
        
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="gray", opacity=0.3, row=3, col=1)
        
        # Layout
        fig.update_layout(
            title=f"📊 {symbol} - Giá: {chart_data['latest_price']:,.1f}₫ ({chart_data['latest_change']:+.2f}%)",
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True,
            legend=dict(x=0, y=1, bgcolor="rgba(255,255,255,0.8)")
        )
        
        # Y-axis labels
        fig.update_yaxes(title_text="Giá (₫)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1, range=[0, 100])
        
        # X-axis
        fig.update_xaxes(title_text="Ngày", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Thông tin chi tiết
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Giá hiện tại", f"{chart_data['latest_price']:,.1f}₫")
        with col2:
            st.metric("Thay đổi", f"{chart_data['latest_change']:+.2f}%")
        with col3:
            st.metric("RSI", f"{chart_data['rsi'][-1]:.1f}")
        with col4:
            ma30_pos = "Trên" if chart_data['latest_price'] > chart_data['ma30'][-1] else "Dưới"
            st.metric("Vị trí vs MA30", ma30_pos)

def create_working_chart(symbol):
    """Tạo chart thực sự hoạt động - sử dụng Plotly với dual-source"""
    st.markdown(f"**📊 Chart - {symbol}**")
    
    # Sử dụng create_stock_chart đã có dual-source fallback
    create_stock_chart(symbol)
        
        # Sử dụng TradingView lightweight chart
        tv_widget = f"""
        <div id="tradingview_chart_{symbol}" style="height:500px; width:100%; background:white; border:1px solid #ddd;">
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                new TradingView.widget({{
                    "autosize": true,
                    "symbol": "HOSE:{symbol}",
                    "interval": "D",
                    "timezone": "Asia/Ho_Chi_Minh",
                    "theme": "light",
                    "style": "1",
                    "locale": "vi",
                    "toolbar_bg": "#f1f3f6",
                    "enable_publishing": false,
                    "hide_top_toolbar": false,
                    "hide_legend": false,
                    "save_image": false,
                    "container_id": "tradingview_chart_{symbol}",
                    "height": 500,
                    "width": "100%"
                }});
            </script>
        </div>
        """
        
        components.html(tv_widget, height=520)
        st.success("✅ Chart loaded successfully!")
        return True
        
    except Exception as e:
        st.warning(f"⚠️ TradingView failed: {e}")
    
    # Method 2: Try CafeF (Vietnamese source)
    try:
        st.markdown("**� Đang thử CafeF chart...**")
        
        cafef_widget = f"""
        <div style="height:500px; width:100%; background:white; border:1px solid #ddd;">
            <iframe 
                src="https://s.cafef.vn/bieu-do.chn?symbol={symbol}&bgColor=FFFFFF&chartType=candle&scale=D"
                width="100%"
                height="100%"
                frameborder="0"
                scrolling="no"
                allowfullscreen>
            </iframe>
        </div>
        """
        
        components.html(cafef_widget, height=520)
        st.success("✅ CafeF chart loaded!")
        return True
        
    except Exception as e:
        st.warning(f"⚠️ CafeF failed: {e}")
    
    # Method 3: Try simple Yahoo Finance embed
    try:
        st.markdown("**🔄 Đang thử Yahoo Finance...**")
        
        yahoo_widget = f"""
        <div style="height:500px; width:100%; background:white; border:1px solid #ddd;">
            <iframe 
                src="https://finance.yahoo.com/quote/{symbol}.VN/chart"
                width="100%"
                height="100%"
                frameborder="0"
                scrolling="no">
            </iframe>
        </div>
        """
        
        components.html(yahoo_widget, height=520)
        st.success("✅ Yahoo Finance chart loaded!")
        return True
        
    except Exception as e:
        st.warning(f"⚠️ Yahoo Finance failed: {e}")
    
    # Method 4: Sử dụng Plotly chart (luôn hoạt động)
    try:
        st.markdown("**📊 Sử dụng chart chuyên nghiệp...**")
        create_stock_chart(symbol)
        st.success("✅ Chart hiển thị thành công!")
        return True
        
    except Exception as e:
        st.error(f"❌ Chart failed: {e}")
        return False

def create_tradingview_widget(symbol):
    """Tạo TradingView widget cho mã cổ phiếu Việt Nam"""
    
    # Mapping mã VN sang TradingView format  
    tv_symbol = f"HOSE:{symbol}" if symbol not in ["VN30", "VN100"] else f"INDEX:{symbol}"
    
    st.markdown(f"**Đang tải TradingView chart cho {symbol}...**")
    
    # Method 1: Try TradingView Widget
    try:
        widget_html = f"""
        <div class="tradingview-widget-container" style="height:600px;width:100%;">
          <div id="tradingview_{symbol}" style="height:100%;width:100%;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
          {{
            "symbols": [
              [
                "{tv_symbol}",
                "{symbol}|1D"
              ]
            ],
            "chartOnly": false,
            "width": "100%",
            "height": "600",
            "locale": "vi",
            "colorTheme": "light",
            "autosize": true,
            "showVolume": true,
            "showMA": true,
            "hideDateRanges": false,
            "hideMarketStatus": false,
            "hideSymbolLogo": false,
            "scalePosition": "right",
            "scaleMode": "Normal",
            "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
            "fontSize": "10",
            "noTimeScale": false,
            "valuesTracking": "1",
            "changeMode": "price-and-percent",
            "chartType": "area",
            "container_id": "tradingview_{symbol}"
          }}
          </script>
        </div>
        """
        
        components.html(widget_html, height=650)
        st.success("✅ TradingView chart loaded successfully!")
        
    except Exception as e:
        st.warning(f"⚠️ TradingView widget failed: {e}")
        st.markdown("**Đang thử phương pháp iframe...**")
        
        # Method 2: Fallback to iframe
        try:
            iframe_url = f"https://www.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=HOSE%3A{symbol}&interval=D&hidesidetoolbar=0&hidetoptoolbar=0&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&hideideas=1&theme=Light&style=1&timezone=Asia%2FHo_Chi_Minh&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=vi"
            
            iframe_html = f"""
            <iframe 
                src="{iframe_url}"
                width="100%"
                height="600"
                frameborder="0"
                allowtransparency="true"
                scrolling="no">
            </iframe>
            """
            
            components.html(iframe_html, height=650)
            st.info("📊 TradingView chart loaded via iframe")
            
        except Exception as e2:
            st.error(f"❌ Both TradingView methods failed: {e2}")
    
    # Thêm link mở TradingView trực tiếp
    tradingview_url = f"https://www.tradingview.com/chart/?symbol=HOSE%3A{symbol}"
    st.markdown(f"[🔗 Mở {symbol} trên TradingView]({tradingview_url})")
    """Tạo TradingView widget cho mã cổ phiếu Việt Nam"""
    
    # Mapping mã VN sang TradingView format  
    tv_symbol = f"HOSE:{symbol}" if symbol not in ["VN30", "VN100"] else f"INDEX:{symbol}"
    
    st.markdown(f"**Đang tải TradingView chart cho {symbol}...**")
    
    # Method 1: Try TradingView Widget
    try:
        widget_html = f"""
        <div class="tradingview-widget-container" style="height:600px;width:100%;">
          <div id="tradingview_{symbol}" style="height:100%;width:100%;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
          {{
            "symbols": [
              [
                "{tv_symbol}",
                "{symbol}|1D"
              ]
            ],
            "chartOnly": false,
            "width": "100%",
            "height": "600",
            "locale": "vi",
            "colorTheme": "light",
            "autosize": true,
            "showVolume": true,
            "showMA": true,
            "hideDateRanges": false,
            "hideMarketStatus": false,
            "hideSymbolLogo": false,
            "scalePosition": "right",
            "scaleMode": "Normal",
            "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
            "fontSize": "10",
            "noTimeScale": false,
            "valuesTracking": "1",
            "changeMode": "price-and-percent",
            "chartType": "area",
            "container_id": "tradingview_{symbol}"
          }}
          </script>
        </div>
        """
        
        components.html(widget_html, height=650)
        st.success("✅ TradingView chart loaded successfully!")
        
    except Exception as e:
        st.warning(f"⚠️ TradingView widget failed: {e}")
        st.markdown("**Đang thử phương pháp iframe...**")
        
        # Method 2: Fallback to iframe
        try:
            iframe_url = f"https://www.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=HOSE%3A{symbol}&interval=D&hidesidetoolbar=0&hidetoptoolbar=0&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&hideideas=1&theme=Light&style=1&timezone=Asia%2FHo_Chi_Minh&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=%5B%5D&disabled_features=%5B%5D&locale=vi"
            
            iframe_html = f"""
            <iframe 
                src="{iframe_url}"
                width="100%"
                height="600"
                frameborder="0"
                allowtransparency="true"
                scrolling="no">
            </iframe>
            """
            
            components.html(iframe_html, height=650)
            st.info("📊 TradingView chart loaded via iframe")
            
        except Exception as e2:
            st.error(f"❌ Both TradingView methods failed: {e2}")
    
    # Thêm link mở TradingView trực tiếp
    tradingview_url = f"https://www.tradingview.com/chart/?symbol=HOSE%3A{symbol}"
    st.markdown(f"[🔗 Mở {symbol} trên TradingView]({tradingview_url})")

# =====================
# Main App
# =====================

def main():
    st.title("🔥 Stock Scanner Vietnam")
    st.markdown("**Quét cổ phiếu Việt Nam với 2 bộ lọc chuyên nghiệp**")
    
    # Sidebar cho cấu hình
    st.sidebar.header("⚙️ Cấu hình")
    
    # Chọn bộ lọc
    filter_option = st.sidebar.selectbox(
        "📊 Chọn bộ lọc:",
        options=["mua1", "muasin"],
        format_func=lambda x: "🔍 MUA 1 (Bộ lọc gốc)" if x == "mua1" else "🔥 MUA SỊN (Bộ lọc mới)",
        index=0
    )
    
    # Hiển thị thông tin bộ lọc
    st.sidebar.markdown("---")
    if filter_option == "mua1":
        st.sidebar.markdown("""
        **🔍 Bộ lọc MUA 1:**
        - 🚀 **Mua Break**: Nền tăng + Phá đỉnh
        - 📈 **Mua Thường**: Nền tăng + Không phá đỉnh
        - 📉 **Bán**: Giá ≤ đáy 8 phiên
        - 🔻 **Short**: Giảm liên tục hoặc dưới 95% đỉnh
        - 📈 **Cover**: Phục hồi sau giảm
        - ↔️ **Sideway**: Đi ngang chuẩn bị bứt phá
        """)
    else:
        st.sidebar.markdown("""
        **🔥 Bộ lọc MUA SỊN:**
        
        **Phiên hiện tại:**
        - Giá cao nhất ≥ giá cao nhất 4 phiên trước × 99%
        - Giá hiện tại dương (tăng)
        
        **Phiên trước:**
        - Nến đỏ (đóng cửa < mở cửa)
        - Giảm không quá 2%
        - Volume < Volume MA20
        
        **Điều kiện chung:**
        - Giá nằm trên EMA 34
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Nút quét
        if filter_option == "mua1":
            scan_button = st.button("🔍 Quét Tín Hiệu MUA", type="primary", use_container_width=True)
        else:
            scan_button = st.button("🔥 Quét Mua Sịn", type="primary", use_container_width=True)
    
    with col2:
        # Hiển thị thời gian quét cuối
        if "last_scan_time" in st.session_state:
            st.info(f"⏰ Quét lần cuối: {st.session_state.last_scan_time}")
    
    # Xử lý khi nhấn nút quét
    if scan_button:
        with st.spinner("🔄 Đang quét thị trường..."):
            try:
                # Lấy danh sách mã
                syminfo = fetch_all_symbols()
                symbols = [s.code for s in syminfo]
                
                if not symbols:
                    st.error("❌ Không thể lấy danh sách mã cổ phiếu")
                    return
                
                st.info(f"📊 Đang quét {len(symbols)} mã cổ phiếu...")
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Quét
                start_time = time.time()
                results = scan_symbols(symbols, filter_option)
                end_time = time.time()
                
                progress_bar.progress(100)
                
                # Lưu kết quả vào session state
                st.session_state.results = results
                st.session_state.filter_type = filter_option
                st.session_state.last_scan_time = datetime.datetime.now().strftime("%H:%M:%S")
                st.session_state.scan_duration = end_time - start_time
                
                status_text.success(f"✅ Hoàn tất quét trong {end_time - start_time:.1f}s")
                
            except Exception as e:
                st.error(f"❌ Lỗi khi quét: {e}")
                return
    
    # Hiển thị kết quả
    if "results" in st.session_state and st.session_state.results:
        results = st.session_state.results
        filter_type = st.session_state.filter_type
        
        st.markdown("---")
        st.subheader("📊 Kết quả quét")
        
        # Thống kê tổng quan
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📈 Tổng mã có tín hiệu", len(results))
        
        with col2:
            if filter_type == "mua1":
                buy_signals = sum(1 for r in results if r["BuyBreak"] or r["BuyNormal"])
                st.metric("🟢 Tín hiệu mua", buy_signals)
            else:
                buy_sin_signals = sum(1 for r in results if r["BuySin"])
                st.metric("🔥 Mua Sịn", buy_sin_signals)
        
        with col3:
            avg_pct = sum(r["pct"] for r in results) / len(results)
            st.metric("📊 % thay đổi TB", f"{avg_pct:+.2f}%")
        
        with col4:
            st.metric("⏱️ Thời gian quét", f"{st.session_state.scan_duration:.1f}s")
        
        # Tạo và hiển thị bảng kết quả
        df = create_results_dataframe(results, filter_type)
        
        if not df.empty:
            # Hiển thị bảng với styling
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
                column_config={
                    "Mã": st.column_config.TextColumn("Mã", width="small"),
                    "Giá": st.column_config.TextColumn("Giá (₫)", width="small"),
                    "Thay đổi (%)": st.column_config.TextColumn("Thay đổi (%)", width="small"),
                    "Tín hiệu": st.column_config.TextColumn("Tín hiệu", width="large")
                }
            )
            
            # Nút download CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Tải xuống CSV",
                data=csv,
                file_name=f"stock_scan_{filter_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Chart selector với clickable buttons
            st.markdown("---")
            st.subheader("📊 Bấm vào mã để xem chart")
            
            # Debug info
            with st.expander("🔧 Debug Info", expanded=False):
                st.write(f"Filter type: {filter_type}")
                st.write(f"Number of results: {len(results)}")
                if "selected_chart_symbol" in st.session_state:
                    st.write(f"Selected symbol: {st.session_state.selected_chart_symbol}")
                else:
                    st.write("No symbol selected yet")
            
            # Tạo buttons cho từng mã cổ phiếu
            symbol_list = [r["symbol"] for r in results]
            
            # Chia thành columns (5 mã mỗi hàng)
            cols_per_row = 5
            for i in range(0, len(symbol_list), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, symbol in enumerate(symbol_list[i:i+cols_per_row]):
                    result = next(r for r in results if r["symbol"] == symbol)
                    pct = result["pct"]
                    
                    # Chọn màu button dựa trên % thay đổi
                    if pct > 2:
                        button_type = "primary"  # Xanh
                    elif pct > 0:
                        button_type = "secondary"  # Xám
                    else:
                        button_type = "secondary"  # Xám
                    
                    with cols[j]:
                        # Tạo unique key đơn giản
                        unique_key = f"chart_btn_{filter_type}_{symbol}_{i}_{j}_{int(time.time())}"
                        
                        if st.button(
                            f"📈 {symbol}\n{pct:+.1f}%", 
                            key=unique_key,
                            type=button_type,
                            width='stretch'
                        ):
                            st.session_state.selected_chart_symbol = symbol
                            st.session_state.chart_type = "vndirect"
                            st.success(f"🎯 Đã chọn {symbol}!")
                            st.rerun()
            
            # Hiển thị chart nếu có mã được chọn
            if "selected_chart_symbol" in st.session_state and st.session_state.selected_chart_symbol:
                st.markdown("---")
                
                # Chọn loại chart
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.markdown("**� Chart sẽ tự động tìm nguồn tốt nhất**")
                
                with col3:
                    if st.button("❌ Đóng chart", type="secondary"):
                        if "selected_chart_symbol" in st.session_state:
                            del st.session_state.selected_chart_symbol
                
                # Hiển thị chart theo loại đã chọn
                selected_symbol = st.session_state.selected_chart_symbol
                st.info(f"🔍 Đang hiển thị chart cho mã: {selected_symbol}")
                
                # Chỉ sử dụng function chart duy nhất
                create_working_chart(selected_symbol)
        else:
            st.warning("⚠️ Không tìm thấy mã nào có tín hiệu")
    
    elif "results" in st.session_state and not st.session_state.results:
        st.warning("⚠️ Không tìm thấy mã nào có tín hiệu")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **📝 Lưu ý:**
    - Dữ liệu từ VNDIRECT API
    - Kết quả chỉ mang tính chất tham khảo
    - Telegram bot vẫn hoạt động song song
    
    **🔗 Links:**
    - [GitHub Repository](https://github.com/nam11993/loccophieu)
    """)

if __name__ == "__main__":
    main()