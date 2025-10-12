# 📈 Webapp Lọc Cổ Phiếu Việt Nam

## 🚀 Hướng dẫn chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements_webapp.txt
```

### 2. Chạy webapp
```bash
streamlit run webapp_simple.py --server.port 8502
```

### 3. Truy cập
- **Local**: http://localhost:8502
- **Network**: http://192.168.31.200:8502

## ✨ Tính năng

### 🎯 Bộ lọc có sẵn:
- **MUA 1**: Bộ lọc chuẩn với tín hiệu mua thông thường
- **MUA SỊN**: Bộ lọc nghiêm ngặt với điều kiện khắt khoảng

### 📊 Chức năng:
- ✅ Quét cổ phiếu theo bộ lọc
- ✅ Hiển thị kết quả dạng bảng
- ✅ Tải xuống CSV
- ✅ Thống kê real-time
- ✅ Giao diện đơn giản, dễ sử dụng

### 🔧 Cài đặt:
- Chọn loại bộ lọc
- Quét tất cả mã cổ phiếu (218 mã)
- Tự động xử lý timeout và lỗi API

## 📋 So sánh bộ lọc

### MUA 1 (Chuẩn):
- Giá tăng 4 ngày liên tiếp
- Giá trên MA30  
- Không tăng quá 4% ngày trước
- Logic breakout
- **Tỷ lệ**: ~15-20% mã đạt điều kiện

### MUA SỊN (Nghiêm ngặt):
- High >= High[-4] × 99%
- Giá tăng hôm nay
- Nến đỏ hôm qua
- Giảm tối đa 2% hôm qua  
- Volume thấp hôm qua
- Trên EMA34
- **Tỷ lệ**: ~5-10% mã đạt điều kiện

## 🚨 Lưu ý
- **Không có chart**: Webapp này không hiển thị biểu đồ
- **Chỉ quét**: Tập trung vào tìm tín hiệu
- **API timeout**: Giới hạn số mã để tránh lỗi mạng
- **Local data**: Sử dụng file symbols.json khi API fail

## 🛠️ Troubleshooting

### Lỗi API:
```
⚠️ API error: Failed to resolve 'api.vndirect.com.vn'
🔄 Trying fallback from symbols.json...
✅ Loaded 218 symbols from local file
```
**Giải pháp**: Webapp tự động fallback, tiếp tục sử dụng bình thường.

### Timeout khi quét:
**Giải pháp**: Webapp tự động xử lý timeout và skip các mã lỗi, tiếp tục quét mã khác.

### Không tìm thấy tín hiệu:
**Giải pháp**: 
- Thử bộ lọc MUA 1 (ít khắt khoảng hơn)
- Kiểm tra điều kiện thị trường
- 3 tín hiệu MUA SỊN là bình thường!