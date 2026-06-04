import json

# Mock Data (Danh bạ giả lập)
MOCK_CONTACTS = {
    "mẹ": [
        {"name": "Mẹ (Vina)", "phone": "0912345678"},
        {"name": "Mẹ vợ", "phone": "0987654321"}
    ],
    "vợ": [
        {"name": "Vợ Yêu", "phone": "0909090909"}
    ],
    "long": [
        {"name": "Hải Long", "phone": "0999888777"},
        {"name": "Long Cty", "phone": "0977666555"}
    ]
}

def clarify_contact(name_hint: str) -> str:
    """
    Công cụ này được sử dụng khi người dùng nhắc đến một tên mơ hồ (ví dụ: 'chuyển cho mẹ', 'chuyển anh Long') mà chưa có số điện thoại cụ thể.
    Nó sẽ tìm kiếm trong danh bạ và trả về các lựa chọn để bạn (AI) hỏi lại người dùng.
    
    Args:
        name_hint: Tên hoặc từ khóa người dùng nhắc tới (ví dụ: 'mẹ', 'long').
    """
    key = name_hint.lower().strip()
    
    # Tìm kiếm gần đúng (chứa từ khóa)
    results = []
    for k, v in MOCK_CONTACTS.items():
        if key in k or k in key:
            results.extend(v)
            
    if not results:
        return json.dumps({
            "status": "not_found",
            "message": f"Không tìm thấy ai tên '{name_hint}' trong danh bạ. Vui lòng hỏi người dùng số điện thoại cụ thể."
        }, ensure_ascii=False)
        
    return json.dumps({
        "status": "success",
        "action": "ask_user_to_choose",
        "options": results,
        "message": "Hãy hiển thị các lựa chọn này dưới dạng nút bấm (button) cho người dùng chọn."
    }, ensure_ascii=False)
