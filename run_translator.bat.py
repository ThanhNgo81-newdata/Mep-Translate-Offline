@echo off
REM Di chuyển vào thư mục dự án
cd /d C:\Users\S4279\Mep-Translate-Offline

REM Kích hoạt môi trường ảo
call venv\Scripts\activate

REM Kiểm tra thư mục models (ví dụ: models hoặc offline_models)
IF NOT EXIST models (
    echo Model chưa tồn tại. Đang tải...
    python download_models.py
) ELSE (
    echo Model đã có sẵn. Bỏ qua bước tải.
)

REM Khởi chạy ứng dụng Streamlit
start "" streamlit run mep_translator_offline.py --server.enableCORS false --server.enableXsrfProtection false

REM Chờ vài giây để server khởi động
timeout /t 5 >nul

REM Tự động mở trình duyệt vào localhost:8501
start http://localhost:8501

