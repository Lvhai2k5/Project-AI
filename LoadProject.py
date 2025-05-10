import os
import subprocess

# Đường dẫn đến thư mục dự án
project_path = r"C:\Users\HAI\Documents\baitap\Tri_Tue_Nhan_Tao"
os.chdir(project_path)

# Thông tin GitHub repository
remote_url = "https://github.com/Lvhai2k5/Do-An-Cuoi-Ki-Tri-Tue-Nhan-Tao.git"

# Các lệnh git
commands = [
    ["git", "init"],
    ["git", "add", "."],
    ["git", "commit", "-m", "Upload project via Python script"],
    ["git", "branch", "-M", "main"],
    ["git", "remote", "add", "origin", remote_url],
    ["git", "push", "-u", "origin", "main"]
]

# Thực thi từng lệnh
for cmd in commands:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Lỗi khi chạy lệnh: {' '.join(cmd)}")
        break
