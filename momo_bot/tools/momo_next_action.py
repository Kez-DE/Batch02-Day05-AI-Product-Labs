import json

def execute_momo_transfer(phone_number: str, amount: int = None) -> str:
    """
    CHỈ GỌI CÔNG CỤ NÀY SAU KHI ĐÃ KIỂM TRA AN TOÀN (safety_check). 
    Sử dụng công cụ này để tạo ra Deep-link mở màn hình chuyển tiền MoMo.
    Người dùng sẽ không bị trừ tiền ngay, mà chỉ mở màn hình điền sẵn thông tin.
    
    Args:
        phone_number: Số điện thoại người nhận.
        amount: Số tiền muốn chuyển (nếu người dùng chưa cung cấp thì bỏ trống).
    """
    
    # Tạo deep-link giả lập
    deeplink = f"momo://transfer?phone={phone_number}"
    if amount:
        deeplink += f"&amount={amount}"
        
    return json.dumps({
        "status": "success",
        "action": "trigger_deeplink",
        "deeplink": deeplink,
        "message_to_user": "Đang mở màn hình chuyển tiền MoMo..."
    }, ensure_ascii=False)
