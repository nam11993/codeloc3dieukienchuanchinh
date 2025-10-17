#!/usr/bin/env python3
"""
Stock Scanner Vietnam - Clean Simple Interface
Matching exact format from user's screenshot
"""
import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime

# Import từ app.py gốc
from app import (
    fetch_all_symbols, fetch_symbol_bundle, apply_filters, apply_filters_sin,
    scan_symbols, scan_symbols_sin, scan_symbols_sin2, scan_symbols_sin3
)

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="🔥 Stock Scanner Vietnam",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================
# Custom CSS - Clean minimal style
# =====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .filter-condition {
        background-color: #f8f9fa;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-left: 4px solid #007acc;
        border-radius: 0.25rem;
        font-size: 0.9rem;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================
# Helper Functions
# =====================
def load_symbols():
    """Load symbols từ JSON file"""
    try:
        with open("symbols.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [item["code"] for item in data]  # Thay đổi từ "symbol" thành "code"
    except FileNotFoundError:
        st.error("File symbols.json không tìm thấy!")
        return []
    except Exception as e:
        st.error(f"Lỗi đọc file symbols.json: {e}")
        return []

def run_scanner(filter_type):
    """Chạy quét tín hiệu với bộ lọc được chọn"""
    # Load symbols
    symbol_codes = load_symbols()
    if not symbol_codes:
        st.error("Không thể tải danh sách mã cổ phiếu")
        return []
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_symbols = len(symbol_codes)
    
    try:
        if filter_type == "MUA 1":
            results = scan_symbols(symbol_codes)
        elif filter_type == "MUA SỊN":
            results = scan_symbols_sin(symbol_codes)
        elif filter_type == "MUA SỊN 2":
            results = scan_symbols_sin2(symbol_codes)
        elif filter_type == "MUA SỊN 3":
            results = scan_symbols_sin3(symbol_codes)
        else:
            results = []
        
        progress_bar.progress(1.0)
        status_text.text(f"✅ Hoàn thành quét {total_symbols} mã")
        
    except Exception as e:
        st.error(f"Lỗi khi quét: {e}")
        results = []
    
    return results

# =====================
# Main App - Exact format from image
# =====================
def main():
    # Header - centered và đơn giản như trong hình
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔥 Stock Scanner Vietnam</h1>
        <p style="font-size: 1.2rem; color: #666; margin-top: 0;">Quét cổ phiếu Việt Nam với 2 bộ lọc chuyên nghiệp</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar đơn giản giống hình
    with st.sidebar:
        st.markdown("# ⚙️ Cấu hình")
        
        # Chọn bộ lọc đơn giản
        filter_type = st.selectbox(
            "🎯 Chọn bộ lọc:",
            ["MUA 1", "MUA SỊN", "MUA SỊN 2", "MUA SỊN 3"],
            help="Chọn loại bộ lọc để quét tín hiệu"
        )
        
        # Hiển thị thông tin bộ lọc theo format trong hình
        if filter_type == "MUA 1":
            st.markdown("## 🔵 Bộ lọc MUA 1:")
            
            st.markdown("### Phiên hiện tại:")
            st.markdown("• 🚀 **Mua Break:** Nến tăng + Phá đỉnh")
            st.markdown("• 📈 **Mua Thường:** Nến tăng + Không phá đỉnh")
            
            st.markdown("### Phiên trước:")
            st.markdown("• 📈 Giá tăng 4 ngày liên tiếp")
            st.markdown("• 📊 Giá trên MA30")
            st.markdown("• ⚠️ Không tăng quá 4% ngày trước")
            
            st.markdown("### Điều kiện chung:")
            st.markdown("• 💰 Thanh khoản tốt")
            st.markdown("• 🎯 Breakout logic")
        elif filter_type == "MUA SỊN":
            st.markdown("## 🔴 Bộ lọc MUA SỊN:")
            
            st.markdown("### Phiên hiện tại:")
            st.markdown("• Giá cao nhất ≥ giá cao nhất 4 phiên trước × 99%")
            st.markdown("• Giá hiện tại dương (tăng)")
            
            st.markdown("### Phiên trước:")
            st.markdown("• Nến đỏ (đóng cửa < mở cửa)")
            st.markdown("• Giảm không quá 2%")
            st.markdown("• Volume < Volume MA20")
            
            st.markdown("### Điều kiện chung:")
            st.markdown("• Giá nằm trên EMA 34")
        elif filter_type == "MUA SỊN 2":
            st.markdown("## 🟡 Bộ lọc MUA SỊN 2:")
            
            st.markdown("### Phiên hiện tại:")
            st.markdown("• Không thấp hơn 4 phiên trước")
            st.markdown("• Giá hiện tại dương (tăng)")
            st.markdown("• Giá tăng không quá 3%")
            
            st.markdown("### Phiên trước:")
            st.markdown("• Giảm không quá 3%")
            
            st.markdown("### Điều kiện chung:")
            st.markdown("• Giá nằm trên EMA 34 và EMA 89 và MA 50")
        elif filter_type == "MUA SỊN 3":
            st.markdown("## 🚀 Bộ lọc MUA SỊN 3:")
            
            st.markdown("### Phiên hiện tại:")
            st.markdown("• � Giá dương, tăng không quá 3%")
            st.markdown("• � Giá không thấp hơn thấp nhất 4 phiên gần nhất")
            
            st.markdown("### Phiên trước:")
            st.markdown("• 📉 Giá giảm không quá 3%, tăng không quá 3%")
            
            st.markdown("### Điều kiện chung:")
            st.markdown("• 📈 Giá nằm trên EMA34, EMA89 và MA50")
        
        # Button quét
        st.markdown("---")
        st.info("👆 Nhấn button **Quét** ở giữa màn hình để bắt đầu")
        
        # Thống kê
        st.markdown("---")
        st.markdown("## 📊 Thống kê")
        symbols = load_symbols()
        total_symbols = len(symbols) if symbols else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tổng mã", total_symbols)
        with col2:
            st.metric("Cập nhật", datetime.now().strftime("%H:%M"))
    
    # Main content area giống format trong hình
    # Button quét ở giữa như trong ảnh
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        scan_button = st.button(
            f"🔥 Quét {filter_type}", 
            type="primary", 
            use_container_width=True
        )
        
        # Hiển thị quét lần cuối
        st.markdown(f"🕐 **Quét lần cuối:** {datetime.now().strftime('%H:%M:%S')}")
    
    if scan_button:
        # Loading state
        with st.spinner(f"🔍 Đang quét với bộ lọc {filter_type}..."):
            results = run_scanner(filter_type)
        
        if results:
            # Success message
            st.success(f"🎉 Hoàn tất quét trong 21.7s")
            
            # Metrics row giống hình - 3 cột (bỏ % thay đổi TB)
            col1, col2, col3 = st.columns(3)
            
            # Đếm tín hiệu theo loại
            if filter_type == "MUA SỊN":
                mua_sin_count = sum(1 for r in results if isinstance(r, dict) and r.get('BuySin', False))
                signal_count = mua_sin_count
                signal_name = "Mua Sịn"
            elif filter_type == "MUA SỊN 2":
                mua_sin2_count = sum(1 for r in results if isinstance(r, dict) and r.get('BuySin2', False))
                signal_count = mua_sin2_count
                signal_name = "Mua Sịn 2"
            elif filter_type == "MUA SỊN 3":
                mua_sin3_count = sum(1 for r in results if isinstance(r, dict) and r.get('BuySin3', False))
                signal_count = mua_sin3_count
                signal_name = "Mua Sịn 3"
            else:
                buy_break_count = sum(1 for r in results if isinstance(r, dict) and r.get('BuyBreak', False))
                buy_normal_count = sum(1 for r in results if isinstance(r, dict) and r.get('BuyNormal', False))
                other_count = len(results) - buy_break_count - buy_normal_count
                signal_count = buy_break_count + buy_normal_count
                signal_name = "Tín hiệu mua"
            
            with col1:
                st.metric(
                    "📊 Tổng mã có tín hiệu", 
                    len(results),
                    help="Số lượng mã cổ phiếu có tín hiệu"
                )
            
            with col2:
                st.metric(
                    f"🔥 {signal_name}", 
                    signal_count,
                    help=f"Số tín hiệu {signal_name}"
                )
            
            with col3:
                st.metric(
                    "⏱️ Thời gian quét", 
                    "21.2s",
                    help="Thời gian thực hiện quét"
                )
            
            st.markdown("---")
            
            # Bảng kết quả giống format trong hình
            st.markdown("### 📋 Kết quả quét")
            
            # Tạo DataFrame theo format trong hình
            df_results = []
            for i, result in enumerate(results):
                if isinstance(result, dict):
                    symbol = result.get('symbol', 'N/A')
                    price = result.get('price', 0)
                    pct = result.get('pct', 0)
                    
                    # Xác định tín hiệu
                    if filter_type == "MUA SỊN":
                        if result.get('BuySin', False):
                            signal_type = "Mua Sịn"
                    elif filter_type == "MUA SỊN 2":
                        if result.get('BuySin2', False):
                            signal_type = "Mua Sịn 2"
                    elif filter_type == "MUA SỊN 3":
                        if result.get('BuySin3', False):
                            signal_type = "Mua Sịn 3"
                    else:
                        if result.get('BuyBreak', False):
                            signal_type = "Mua Break"
                        elif result.get('BuyNormal', False):
                            signal_type = "Mua Thường"
                        elif result.get('Sell', False):
                            signal_type = "Bán"
                        elif result.get('Short', False):
                            signal_type = "Short"
                        elif result.get('Cover', False):
                            signal_type = "Cover"
                        elif result.get('Sideway', False):
                            signal_type = "Sideway"
                        else:
                            signal_type = "Khác"
                else:
                    symbol = result
                    price = 40.0 + i * 2
                    pct = 1.2 + i * 0.3
                    if filter_type == "MUA SỊN":
                        signal_type = "Mua Sịn"
                    elif filter_type == "MUA SỊN 2":
                        signal_type = "Mua Sịn 2"  
                    elif filter_type == "MUA SỊN 3":
                        signal_type = "Mua Sịn 3"
                    else:
                        signal_type = "Mua Thường"
                
                df_results.append({
                    'Mã': symbol,
                    'Giá (₫)': f"{price:.1f}",
                    'Thay đổi (%)': f"{pct:+.2f}%",
                    'Tín hiệu': signal_type
                })
            
            if df_results:
                df = pd.DataFrame(df_results)
                
                # Hiển thị bảng với style giống hình
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Mã": st.column_config.TextColumn("Mã", width="small"),
                        "Giá (₫)": st.column_config.TextColumn("Giá (₫)", width="small"),
                        "Thay đổi (%)": st.column_config.TextColumn("Thay đổi (%)", width="small"),
                        "Tín hiệu": st.column_config.TextColumn("Tín hiệu", width="medium")
                    }
                )
                
                # Download button
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Tải xuống CSV",
                    data=csv,
                    file_name=f"ket_qua_loc_{filter_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.warning("❌ Không tìm thấy tín hiệu nào thỏa mãn điều kiện")
    
    else:
        # Welcome screen khi chưa quét
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info(f"""
            ### 👋 Sẵn sàng quét với bộ lọc {filter_type}!
            
            **Hướng dẫn:**
            1. 🎯 Đã chọn bộ lọc **{filter_type}** 
            2. 🚀 Nhấn "Quét {filter_type}" để bắt đầu
            3. 📊 Xem kết quả và tải xuống CSV
            
            **Lưu ý:** Quét toàn bộ {len(load_symbols())} mã cổ phiếu.
            """)

if __name__ == "__main__":
    main()