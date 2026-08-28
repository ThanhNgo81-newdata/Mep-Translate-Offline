# MEP Translator Offline — dùng nội bộ

## 1. Kiến trúc

Bản này đã bỏ hoàn toàn `anthropic`, `ANTHROPIC_API_KEY` và các lời gọi API.

- Streamlit chỉ là giao diện web.
- Máy chủ nội bộ tải mô hình NLLB-200 distilled 600M từ thư mục `models/`.
- Sau khi model được tải về, quá trình dịch có thể chạy **không Internet**.
- Đồng nghiệp truy cập trình duyệt vào IP máy chủ trong LAN; file được xử lý trên máy chủ, không gửi sang dịch vụ AI bên ngoài.
- DOCX / XLSX / PDF / TXT được hỗ trợ; ảnh dùng Tesseract OCR nếu cài thêm language packs.

NLLB-200 là mô hình dịch đa ngôn ngữ hỗ trợ hơn 200 ngôn ngữ. Xem tài liệu Hugging Face để biết mã ngôn ngữ và cách sử dụng. Hãy kiểm tra license của checkpoint trước khi triển khai trong môi trường doanh nghiệp.

## 2. Cài đặt máy chủ

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Tải model một lần

Máy chủ cần Internet ở bước này:

```bash
python download_models.py
```

Model sẽ nằm ở:

```text
models/
└── nllb-200-distilled-600M/
```

Sau bước này có thể ngắt Internet. Không cần API key.

## 4. Chạy trong mạng LAN

```bash
streamlit run mep_translator_offline.py --server.address 0.0.0.0 --server.port 8501
```

Đồng nghiệp mở:

```text
http://IP-MAY-CHU:8501
```

Ví dụ:

```text
http://192.168.1.20:8501
```

Máy chủ phải chạy app trong thời gian đồng nghiệp sử dụng.

## 5. Khuyến nghị bảo vệ app

Nếu chỉ dùng trong LAN tin cậy, có thể dùng firewall chỉ cho phép subnet nội bộ truy cập port 8501.

Nếu cần mật khẩu đăng nhập, có thể bổ sung lớp reverse proxy (Nginx/IIS) hoặc cơ chế xác thực riêng. Không nên mở trực tiếp port Streamlit ra Internet.

## 6. OCR ảnh

Cài Tesseract OCR trên máy chủ và language packs tương ứng.

Ví dụ Windows cần cài Tesseract và các gói ngôn ngữ `eng`, `vie`, `jpn`, `kor`, `chi_sim`, `chi_tra`... tùy tài liệu.

Nếu chỉ dịch PDF/DOCX/XLSX thì có thể bỏ qua OCR.

## 7. Khác biệt so với bản Anthropic

Bản Anthropic trong source sử dụng Claude để dịch và OCR ảnh; key có thể được lấy từ `secrets.toml` hoặc nhập ở sidebar. Bản offline này thay phần đó bằng mô hình NLLB cục bộ và Tesseract OCR.

Do đó:

- Không có chi phí token/API.
- Không phụ thuộc Internet sau khi model đã được tải.
- Dữ liệu tài liệu nằm trong máy chủ nội bộ.
- Chất lượng dịch có thể thấp hơn Claude ở các đoạn MEP dài/phức tạp.
- NLLB không phải model chuyên MEP; phần bảo toàn mã thiết bị/tiêu chuẩn/đơn vị được xử lý bằng cơ chế bảo vệ token trong code.

## 8. Lưu ý về XLSX

Bản hiện tại chèn bản dịch sang cột bên phải ô văn bản. Với workbook có merged cells phức tạp, cần kiểm thử trên mẫu thực tế trước khi dùng hàng loạt.

## 9. Khuyến nghị triển khai thực tế

Nếu nhiều người cùng dùng:

1. Dùng một máy Windows/Linux có RAM đủ lớn.
2. Nếu có GPU NVIDIA, cài PyTorch CUDA tương ứng để tăng tốc.
3. Chạy Streamlit trên máy chủ đó.
4. Chỉ mở port 8501 trong mạng nội bộ.
5. Không copy thư mục `models/` vào từng máy đồng nghiệp.
6. Backup code và model riêng.
