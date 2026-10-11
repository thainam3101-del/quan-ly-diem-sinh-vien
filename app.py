import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="📚",
    layout="wide"
)

st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.write("Ứng dụng quản lý, tra cứu và thống kê điểm của 10 sinh viên.")

# Dữ liệu mẫu: anh có thể thay bằng dữ liệu thực tế của lớp
data = {
    "Ho_ten": [
        "Nguyen Van An", "Tran Thi Binh",
        "Le Van Cuong", "Pham Thi Dung",
        "Hoang Van Em", "Vu Thi Giang",
        "Do Van Hung", "Bui Thi Lan",
        "Dang Van Minh", "Ngo Thi Hoa"
    ],
    "Chuyen_can": [9, 8, 7, 10, 6, 9, 5, 8, 7, 9],
    "Giua_ky": [8, 7, 6, 9, 5, 8, 4, 7, 6, 9],
    "Cuoi_ky": [9, 8, 7, 9, 6, 8, 5, 8, 7, 10]
}

df = pd.DataFrame(data)

# Tính điểm tổng kết theo công thức của đề bài
df["Tong_ket"] = (
    0.2 * df["Chuyen_can"]
    + 0.3 * df["Giua_ky"]
    + 0.5 * df["Cuoi_ky"]
).round(2)

# Xếp loại theo ngưỡng điểm của đề bài
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Bảng điểm
st.subheader("1. Bảng điểm sinh viên")
bang_diem = df.rename(columns={
    "Ho_ten": "Họ tên",
    "Chuyen_can": "Chuyên cần",
    "Giua_ky": "Giữa kỳ",
    "Cuoi_ky": "Cuối kỳ",
    "Tong_ket": "Tổng kết",
    "Xep_loai": "Xếp loại"
})
st.dataframe(bang_diem, use_container_width=True, hide_index=True)

# Thống kê
st.subheader("2. Thống kê kết quả học tập")
c1, c2, c3 = st.columns(3)
c1.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
c2.metric("Điểm tổng kết cao nhất", f"{df['Tong_ket'].max():.2f}")
c3.metric("Số sinh viên đạt (≥ 5)", int((df["Tong_ket"] >= 5).sum()))

sv_max = df.loc[df["Tong_ket"].idxmax()]
sv_min = df.loc[df["Tong_ket"].idxmin()]
st.write(f"**Sinh viên có điểm cao nhất:** {sv_max['Ho_ten']} — {sv_max['Tong_ket']:.2f}")
st.write(f"**Sinh viên có điểm thấp nhất:** {sv_min['Ho_ten']} — {sv_min['Tong_ket']:.2f}")

# Tra cứu sinh viên
st.subheader("3. Tra cứu thông tin sinh viên")
ten_sv = st.selectbox("Chọn một sinh viên", df["Ho_ten"].tolist())
sv = df.loc[df["Ho_ten"] == ten_sv].iloc[0]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Chuyên cần", f"{sv['Chuyen_can']:.1f}")
m2.metric("Giữa kỳ", f"{sv['Giua_ky']:.1f}")
m3.metric("Cuối kỳ", f"{sv['Cuoi_ky']:.1f}")
m4.metric("Tổng kết", f"{sv['Tong_ket']:.2f}")
st.write(f"**Xếp loại:** {sv['Xep_loai']}")

# Biểu đồ
st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(df["Ho_ten"], df["Tong_ket"])
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", labelrotation=45)
for label in ax.get_xticklabels():
    label.set_horizontalalignment("right")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Thông tin người tạo: thay hai chỗ bên dưới trước khi nộp bài
st.markdown("---")
st.caption("Người tạo: [Đoàn Thái Nam ]")
