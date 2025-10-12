#!/usr/bin/env python3
"""
Test script để demo các loại tín hiệu MUA 1
"""

# Mock data để demo
mock_results = [
    {
        'symbol': 'VCB',
        'price': 64.5,
        'pct': 1.2,
        'BuyBreak': True,
        'BuyNormal': False,
        'Sell': False,
        'Short': False,
        'Cover': False,
        'Sideway': False
    },
    {
        'symbol': 'VIC', 
        'price': 192.0,
        'pct': 2.5,
        'BuyBreak': False,
        'BuyNormal': True,
        'Sell': False,
        'Short': False,
        'Cover': False,
        'Sideway': False
    },
    {
        'symbol': 'HPG',
        'price': 29.8,
        'pct': -0.5,
        'BuyBreak': False,
        'BuyNormal': False,
        'Sell': True,
        'Short': False,
        'Cover': False,
        'Sideway': False
    },
    {
        'symbol': 'MSN',
        'price': 84.2,
        'pct': 0.8,
        'BuyBreak': False,
        'BuyNormal': False,
        'Sell': False,
        'Short': False,
        'Cover': True,
        'Sideway': False
    },
    {
        'symbol': 'TCB',
        'price': 39.9,
        'pct': 0.2,
        'BuyBreak': False,
        'BuyNormal': False,
        'Sell': False,
        'Short': False,
        'Cover': False,
        'Sideway': True
    }
]

print("🧪 Demo các loại tín hiệu MUA 1:")
print("=" * 50)

for r in mock_results:
    symbol = r['symbol']
    price = r['price']
    pct = r['pct']
    
    signals = []
    if r['BuyBreak']: signals.append('🚀 Mua Break')
    if r['BuyNormal']: signals.append('📈 Mua Thường')  
    if r['Sell']: signals.append('📉 Bán')
    if r['Short']: signals.append('⬇️ Short')
    if r['Cover']: signals.append('⬆️ Cover')
    if r['Sideway']: signals.append('↔️ Sideway')
    
    signal_text = " | ".join(signals) if signals else "Không có tín hiệu"
    print(f"{symbol:>6} | {price:>7.1f}₫ | {pct:>+6.2f}% | {signal_text}")

print("\n💡 Như vậy MUA 1 có thể phân biệt được:")
print("   🚀 Mua Break    - Tăng + Phá đỉnh")
print("   📈 Mua Thường  - Tăng + Không phá đỉnh") 
print("   📉 Bán         - Giá ở đáy 8 phiên")
print("   ⬇️ Short       - Giảm liên tục hoặc dưới 95% đỉnh")
print("   ⬆️ Cover       - Phục hồi sau nhập giảm")
print("   ↔️ Sideway     - Đi ngang, chuẩn bị bứt phá")