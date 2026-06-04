import json
import os
from providers.llm_provider import UniversalProvider
from tools import AGENT_TOOLS, TOOL_SCHEMAS

class MoniAgent:
    def __init__(self):
        self.provider = UniversalProvider()
        self.system_instruction = self._load_system_prompt()
        self.tools = TOOL_SCHEMAS
        
        # Với OpenAI, chúng ta cần tự duy trì mảng messages
        self.messages = [
            {"role": "system", "content": self.system_instruction}
        ]
        
    def _load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "artifacts", "system_prompt.md")
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def process_message(self, user_message: str):
        """
        Gửi tin nhắn cho LLM và xử lý luồng Function Calling.
        """
        try:
            self.messages.append({"role": "user", "content": user_message})
            
            response = self.provider.generate_response(
                messages=self.messages,
                tools=self.tools
            )
            
            choice = response.choices[0]
            message = choice.message
            
            # Lưu lại phản hồi của AI vào lịch sử
            self.messages.append(message)
            
            # Kiểm tra xem LLM có yêu cầu gọi tool nào không
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args_str = tool_call.function.arguments
                    args = json.loads(args_str) if args_str else {}
                    
                    # Log ra terminal để dễ debug (Developer Mode)
                    print(f"\n[🔧 AI ĐANG GỌI TOOL]: {name}({args})")
                    
                    # Chúng ta map tên hàm với hàm thực tế trong AGENT_TOOLS
                    function_map = {tool.__name__: tool for tool in AGENT_TOOLS}
                    if name in function_map:
                        tool_func = function_map[name]
                        # Thực thi tool
                        tool_result = tool_func(**args)
                        
                        # Trả lại kết quả của tool cho LLM để nó biết kết quả
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": name,
                            "content": str(tool_result)
                        })
                        
                # Sau khi có kết quả từ các tool, gọi LLM lần nữa để sinh ra câu trả lời cuối
                second_response = self.provider.generate_response(
                    messages=self.messages,
                    tools=self.tools
                )
                
                final_msg = second_response.choices[0].message
                self.messages.append(final_msg)
                return final_msg.content
            
            # Nếu không gọi tool, trả về câu trả lời bình thường
            return message.content

        except Exception as e:
            return f"❌ [Lỗi Hệ Thống]: {str(e)}"
