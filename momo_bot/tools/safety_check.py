import json

# Giả lập database các số điện thoại lừa đảo (blacklist)
BLACKLIST_PHONES = ["0123456789", "0999999999"]
MAX_AMOUNT_NO_OTP = 5000000 # 5 triệu

def safety_check(phone_number: str, amount: int = 0) -> str:
    """
    Sử dụng công cụ này ĐỂ KIỂM TRA TÍNH AN TOÀN TRƯỚC KHI tạo lệnh chuyển tiền, khi bạn đã có được số điện thoại chính xác.
    Nó kiểm tra xem số điện thoại có lừa đảo không, hoặc số tiền có quá lớn không.
    
    Args:
        phone_number: Số điện thoại người nhận (vd: '0912345678').
        amount: (Tùy chọn) Số tiền muốn chuyển.
    """
    # 1. Check định dạng SĐT cơ bản (giả lập)
    if len(phone_number) < 9 or len(phone_number) > 11:
        return json.dumps({
            "safe": False,
            "reason": "Số điện thoại không đúng định dạng.",
            "next_action": "abort_and_alert"
        }, ensure_ascii=False)
        
    # 2. Check Blacklist
    if phone_number in BLACKLIST_PHONES:
        return json.dumps({
            "safe": False,
            "reason": "CẢNH BÁO: Số điện thoại này nằm trong danh sách đen lừa đảo!",
            "next_action": "abort_and_alert"
        }, ensure_ascii=False)
        
    # 3. Check hạn mức
    if amount > MAX_AMOUNT_NO_OTP:
        return json.dumps({
            "safe": False,
            "reason": f"Số tiền {amount} vượt quá hạn mức chuyển nhanh. Yêu cầu xác thực OTP hoặc khuôn mặt.",
            "next_action": "abort_and_alert" # Hoặc có thể là require_auth
        }, ensure_ascii=False)
        
    return json.dumps({
        "safe": True,
        "message": "Số điện thoại an toàn. Có thể tiến hành mở màn hình chuyển tiền.",
        "next_action": "call_execute_momo_transfer"
    }, ensure_ascii=False)
