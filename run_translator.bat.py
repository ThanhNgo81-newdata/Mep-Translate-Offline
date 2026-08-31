@echo off
REM Di chuyển vào thư mục dự án
cd /d C:\Users\S4279\Mep-Translate-Offline

REM Kích hoạt môi trường ảo
call venv\Scripts\activate

REM Kiểm tra thư mục models (ví dụ: models hoặc transformers)
IF NOT EXIST models (
    echo Model chưa tồn tại. Đang tải...
    python download_models.py
) ELSE (
    echo Model đã có sẵn. Bỏ qua bước tải.
)

REM Khởi chạy ứng dụng Streamlit
streamlit run mep_translator_offline.py --server.enableCORS false --server.enableXsrfProtection false
