import pandas as pd
import json

# --- Cấu hình ---
# Tên tệp Excel (.xlsx) đầu vào của bạn
input_xlsx_path = "C:\\Users\\Admin\\Downloads\\applications-20230306\\applications\\lectures\\210-models\\Vocabulary Bank.xlsx"

# Tên tệp JSON bạn muốn tạo ra
output_json_path = "vocabulary_output.json"

# Phần đầu của URL bạn muốn thêm vào
base_url = "https://nguyenthanhdat10012004.github.io/anki_ar/data/"

# --- Bắt đầu xử lý ---
try:
    # 1. Đọc tệp Excel (.xlsx)
    # Giả định dữ liệu nằm ở trang tính (sheet) đầu tiên
    df = pd.read_excel(input_xlsx_path)

    # 2. Lấp đầy các ô trống trong cột 'Category'
    # Sử dụng phương thức 'ffill' (forward-fill)
    df['Category'] = df['Category'].ffill()

    # 3. Tạo trường 'link_glb' mới
    # .str.strip() để loại bỏ các khoảng trắng thừa (nếu có)
    df['link_glb'] = base_url + df['Category'].str.strip() + '/' + df['Tên file (.glb)'].str.strip()
    df['link_glb'] = df['link_glb'].str.lower()
    # 4. Chọn các cột cần thiết và đổi tên chúng
    df_final = df[['Từ vựng', 'Nghĩa', 'Category', 'link_glb']]
    df_final = df_final.rename(columns={
        'Từ vựng': 'vocabulary',
        'Nghĩa': 'meaning',
        'Category': 'category'
    })

    # 5. Chuyển đổi DataFrame thành định dạng JSON (list of dictionaries)
    json_data = df_final.to_dict(orient='records')

    # 6. Ghi dữ liệu JSON ra tệp
    with open(output_json_path, 'w', encoding='utf-8') as f:
        # ensure_ascii=False để đảm bảo tiếng Việt hiển thị đúng
        # indent=4 để tệp JSON dễ đọc hơn
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"--- Hoàn tất! ---")
    print(f"Đã xử lý và lưu thành công vào tệp: {output_json_path}")

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy tệp tại '{input_xlsx_path}'.")
    print("Vui lòng đảm bảo tệp Excel nằm cùng thư mục với mã này.")
except ImportError:
    print("Lỗi: Cần cài đặt thư viện 'openpyxl' để đọc tệp .xlsx.")
    print("Hãy chạy lệnh: pip install openpyxl")
except KeyError as e:
    print(f"Lỗi: Không tìm thấy cột cần thiết. Vui lòng kiểm tra tên cột có chính xác không: {e}")
except Exception as e:
    print(f"Đã xảy ra một lỗi không mong muốn: {e}")