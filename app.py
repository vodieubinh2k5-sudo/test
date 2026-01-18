import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Cấu hình giao diện Web
st.set_page_config(page_title="AI Quiz Generator", page_icon="🎓")

# --- PHẦN CẤU HÌNH AI ---
# Bạn lấy API Key tại: https://aistudio.google.com/
API_KEY = "THAY_VÀO_ĐÂY_API_KEY_CỦA_BẠN" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🎓 Trợ Lý Ôn Thi AI")
st.subheader("Tải tài liệu lên để AI tự soạn đề thi cho bạn")

# --- GIAO DIỆN TẢI FILE ---
uploaded_file = st.file_uploader("Chọn file PDF tài liệu bài học", type="pdf")

if uploaded_file is not None:
    # Đọc nội dung PDF
    with st.spinner("Đang đọc tài liệu..."):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    
    st.success("Đã đọc xong tài liệu!")

    # Cài đặt số lượng câu hỏi
    num_questions = st.slider("Số lượng câu hỏi muốn tạo:", 3, 10, 5)

    if st.button("🚀 Bắt đầu tạo câu hỏi"):
        with st.spinner("AI đang suy nghĩ để soạn đề..."):
            # Lệnh yêu cầu AI (Prompt)
            prompt = f"""
            Dựa trên nội dung văn bản sau: {text[:10000]}
            Hãy tạo ra {num_questions} câu hỏi trắc nghiệm tiếng Việt.
            Mỗi câu hỏi phải có:
            1. Câu hỏi
            2. 4 phương án A, B, C, D
            3. Đáp án đúng
            4. Giải thích chi tiết tại sao đúng.
            Định dạng rõ ràng, dễ đọc.
            """
            
            response = model.generate_content(prompt)
            
            # Hiển thị kết quả
            st.markdown("---")
            st.markdown("### 📝 ĐỀ THI ÔN TẬP CỦA BẠN")
            st.write(response.text)
            
            # Nút tải về (giả lập)
            st.download_button("Tải đề thi về máy (.txt)", response.text, file_name="de_on_tap.txt")
