from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.learning import GhiDanhHocTap
from app.models.user import NguoiDung, HocVien
from app.models.course import KhoaHoc

router = APIRouter(prefix="/reports", tags=["Reports & Statistics"])

@router.get("/student-progress", summary="Báo cáo danh sách học viên và tiến độ học tập các khóa học")
def get_student_progress_report(db: Session = Depends(get_db)):
    """
    Kết xuất dữ liệu báo cáo: Lấy danh sách học viên, khóa học họ đăng ký 
    và tiến độ học tập (TienDoHocTap) để hiển thị lên bảng báo cáo của Frontend.
    """
    results = (
        db.query(
            NguoiDung.HoTen,
            NguoiDung.Email,
            HocVien.Lop,
            KhoaHoc.TenKH,
            GhiDanhHocTap.NgayDangKy,
            GhiDanhHocTap.TrangThaiHoc,
            GhiDanhHocTap.TienDoHocTap
        )
        .join(HocVien, NguoiDung.MaND == HocVien.MaHV)
        .join(GhiDanhHocTap, HocVien.MaHV == GhiDanhHocTap.MaHV)
        .join(KhoaHoc, GhiDanhHocTap.MaKH == KhoaHoc.MaKH)
        .all()
    )

    # Chuyển đổi kết quả sang dạng JSON trả về cho Frontend
    report_data = []
    for row in results:
        report_data.append({
            "HoTen": row.HoTen,
            "Email": row.Email,
            "Lop": row.Lop,
            "TenKhoaHoc": row.TenKH,
            "NgayDangKy": str(row.NgayDangKy),
            "TrangThaiHoc": row.TrangThaiHoc,
            "TienDoHocTap": f"{row.TienDoHocTap}%"
        })

    return {
        "total_records": len(report_data),
        "data": report_data
    }