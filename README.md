# 🔥 Stock Scanner Vietnam - Web Application# 🔥 Stock Scanner Vietnam



Professional web interface for scanning Vietnamese stocks with dual filtering systems.Hệ thống quét cổ phiếu Việt Nam với 2 bộ lọc chuyên nghiệp, hỗ trợ cả **Telegram Bot** và **Web App**.



## 🌟 Features## 🎯 Tính năng



- **🎯 Dual Filter System**: MUA 1 (6 signal types) and MUA SỊN (strict conditions)### 📱 **Telegram Bot**

- **📊 Real-time Scanning**: Scan all 218 Vietnamese stock symbols- ✅ Nút "🔍 Quét Tín Hiệu MUA" - Bộ lọc gốc

- **🎨 Clean UI**: Professional interface matching exact user specifications- ✅ Nút "🔥 Quét Mua Sịn" - Bộ lọc mới

- **📈 Signal Detection**: Multiple signal types (Buy Break, Buy Normal, Sell, Short, Cover, Sideway)- ✅ Hướng dẫn sử dụng chi tiết

- **📥 CSV Export**: Download scan results for analysis- ✅ Format kết quả chuyên nghiệp

- **⚡ Fast Performance**: Optimized scanning with progress tracking

### 🌐 **Web App**

## 🚀 Quick Start- ✅ Giao diện web hiện đại với Streamlit

- ✅ 2 bộ lọc độc lập

### Prerequisites- ✅ Hiển thị kết quả dạng bảng

- Python 3.12+- ✅ Tải xuống CSV

- Required packages (see `requirements_webapp.txt`)- ✅ Thống kê real-time



### Installation## 🔍 Bộ lọc MUA 1 (Gốc)



```bash**Các tín hiệu:**

# Clone repository- 🚀 **Mua Break**: Nền tăng + Phá đỉnh ngắn hạn

git clone https://github.com/nam11993/loccophieucowebapp.git- 📈 **Mua Thường**: Nền tăng + Không phá đỉnh

cd loccophieucowebapp- 📉 **Bán**: Giá ≤ đáy của 8 phiên liên tiếp

- 🔻 **Short**: Giảm liên tục hoặc dưới 95% đỉnh

# Install dependencies- 📈 **Cover**: Phục hồi sau nhịp giảm

pip install -r requirements_webapp.txt- ↔️ **Sideway**: Đi ngang chuẩn bị bứt phá



# Run webapp## 🔥 Bộ lọc MUA SỊN (Mới)

streamlit run webapp_simple.py

```**Điều kiện phiên hiện tại:**

- Giá cao nhất ≥ giá cao nhất 4 phiên trước × 99%

### Usage- Giá hiện tại dương (tăng so với phiên trước)



1. **🌐 Open Browser**: Navigate to `http://localhost:8501`**Điều kiện phiên trước:**

2. **🎯 Select Filter**: Choose between "MUA 1" or "MUA SỊN" in sidebar- Nến đỏ (đóng cửa < mở cửa)

3. **🚀 Start Scan**: Click "Quét [Filter]" button in center- Giảm không quá 2%

4. **📊 View Results**: See metrics and detailed results table- Volume < Volume MA20

5. **📥 Export Data**: Download CSV for further analysis

**Điều kiện chung:**

## 📋 Filter Types- Giá nằm trên EMA 34



### 🔵 MUA 1 Filter (6 Signal Types)## 🚀 Cài đặt và Chạy

- **🚀 Mua Break**: Rising candle + breaking short-term peak

- **📈 Mua Thường**: Rising candle without breaking peak### 1. Clone Repository

- **📉 Bán**: Price at bottom of 8 recent sessions```bash

- **⬇️ Short**: Declining 4 days OR below 95% of peakgit clone https://github.com/nam11993/loccophieu

- **⬆️ Cover**: Strong recovery after declinecd loccophieu

- **↔️ Sideway**: Sideways movement, preparing for breakout```



**Common Conditions:**### 2. Cài đặt Dependencies

- Price rising 4 consecutive days

- Price above MA30**Cho Telegram Bot:**

- Not rising more than 4% previous day```bash

- Good liquidity (≥ 1M VND)pip install -r requirements.txt

```

### 🔴 MUA SỊN Filter (Strict Conditions)

**Current Session:****Cho Web App:**

- Highest price ≥ highest price 4 sessions ago × 99%```bash

- Current price positive (rising)pip install -r requirements_web.txt

```

**Previous Session:**

- Red candle (close < open)### 3. Chạy Telegram Bot

- Decline not more than 2%

- Volume < Volume MA201. Tạo file `.env`:

```env

**Common Conditions:**TELEGRAM_BOT_TOKEN=your_bot_token_here

- Price above EMA 34```



## 🎨 UI Layout2. Chạy bot:

```bash

- **Header**: Centered title with subtitlepython app.py

- **Sidebar**: Filter selection and information```

- **Main Area**: Centered scan button with timestamp

- **Results**: 3-column metrics + detailed table### 4. Chạy Web App

- **Export**: CSV download functionality

```bash

## 📊 Metrics Displaystreamlit run streamlit_app.py

```

1. **📊 Tổng mã có tín hiệu**: Total symbols with signals

2. **🔥 [Signal Type]**: Count of specific signal type**Web app sẽ chạy tại:** http://localhost:8501

3. **⏱️ Thời gian quét**: Scan execution time

## 📊 Nguồn dữ liệu

## 🛠️ Technical Stack

- **API**: VNDIRECT Open API (miễn phí, không cần key)

- **Framework**: Streamlit- **Real-time**: Giá phút cuối từ intraday

- **Data Source**: VNDIRECT API- **Lịch sử**: 120 ngày để tính toán chỉ báo kỹ thuật

- **Language**: Python 3.12

- **Styling**: Custom CSS for professional UI## 🏗️ Cấu trúc Project

- **Export**: Pandas DataFrame to CSV

```

## 📁 Project Structureloccophieu/

├── app.py              # Telegram Bot chính

```├── scanner_core.py     # Logic scan dùng chung

├── webapp_simple.py       # Main webapp file├── streamlit_app.py    # Web App

├── app.py                 # Core scanning logic├── requirements.txt    # Dependencies cho bot

├── symbols.json           # Stock symbols database├── requirements_web.txt # Dependencies cho web

├── requirements_webapp.txt # Dependencies├── .env               # Telegram bot token

├── README_WEBAPP.md       # Detailed documentation└── README.md          # Hướng dẫn này

└── demo_signals.py        # Signal demonstration```

```

## 📱 Sử dụng

## 🔧 Configuration

### **Telegram Bot:**

The webapp automatically:1. Tìm bot trên Telegram

- Loads 218 Vietnamese stock symbols2. Gõ `/start` để hiển thị keyboard

- Applies appropriate filters based on user selection3. Nhấn nút để quét:

- Handles API timeouts and retries   - "🔍 Quét Tín Hiệu MUA"

- Provides progress tracking during scans   - "🔥 Quét Mua Sịn"



## 📈 Signal Analysis### **Web App:**

1. Mở http://localhost:8501

Results include:2. Chọn bộ lọc trong sidebar

- **Mã**: Stock symbol3. Nhấn nút quét tương ứng

- **Giá (₫)**: Current price in VND4. Xem kết quả và tải CSV

- **Thay đổi (%)**: Percentage change

- **Tín hiệu**: Signal type detected## ⚙️ Cấu hình



## 🚀 Performance### **Telegram Bot:**

- Chỉnh `MAX_WORKERS` trong `scanner_core.py`

- **Scan Time**: ~21 seconds for all 218 symbols- Thay đổi `CHUNK_SIZE` cho số mã mỗi message

- **API Integration**: VNDIRECT with timeout handling

- **Memory Efficient**: Optimized data processing### **Web App:**

- **Real-time Updates**: Progress tracking and status- Tùy chỉnh UI trong `streamlit_app.py`

- Thêm chart/visualizations nếu cần

## 🤝 Contributing

## 🔄 Phát triển

1. Fork the repository

2. Create feature branch (`git checkout -b feature/amazing-feature`)### **Thêm bộ lọc mới:**

3. Commit changes (`git commit -m 'Add amazing feature'`)1. Tạo function trong `scanner_core.py`

4. Push to branch (`git push origin feature/amazing-feature`)2. Cập nhật `scan_symbols()` 

5. Open a Pull Request3. Thêm UI trong cả bot và web app



## 📄 License### **Deploy Web App:**

- Streamlit Cloud (miễn phí)

This project is licensed under the MIT License - see the LICENSE file for details.- Heroku, Railway, Vercel

- Docker container

## 🆘 Support

## ⚠️ Lưu ý

For issues and questions:

- Open an issue on GitHub- Kết quả chỉ mang tính chất tham khảo

- Check existing documentation- Không phải lời khuyên đầu tư

- Review code comments for implementation details- Luôn tự nghiên cứu trước khi đầu tư



---## 📧 Liên hệ



**🔥 Stock Scanner Vietnam** - Professional Vietnamese stock scanning with dual filtering systems.- **GitHub**: [nam11993](https://github.com/nam11993)
- **Repository**: [loccophieu](https://github.com/nam11993/loccophieu)

---

**🎉 Chúc bạn đầu tư thành công!**