from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.database import get_db
from app.models.learning import GhiDanhHocTap, BaiTest, LanLamBai, TangKhoaHoc

router = APIRouter(prefix="/learning", tags=["Learning & Testing"])

@router.post("/enroll", summary="Học viên ghi danh khóa học (Kiểm tra ràng buộc không trùng lặp)")
def enroll_course(ma_hv: str, ma_kh: str, db: Session = Depends(get_db)):
    # Kiểm tra xem đã ghi danh trước đó chưa (Ràng buộc không trùng lặp khóa chính cặp MaHV, MaKH)
    existing = db.query(GhiDanhHocTap).filter(
        GhiDanhHocTap.MaHV == ma_hv, 
        GhiDanhHocTap.MaKH == ma_kh
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Học viên đã đăng ký khóa học này rồi.")
    
    new_enroll = GhiDanhHocTap(
        MaHV=ma_hv,
        MaKH=ma_kh,
        NgayDangKy=date.today(),
        TrangThaiHoc="Đang học",
        TienDoHocTap=0.0 # Ràng buộc miền giá trị [0, 100]
    )
    db.add(new_enroll)
    db.commit()
    return {"message": "Ghi danh khóa học thành công", "MaHV": ma_hv, "MaKH": ma_kh}


@router.get("/courses/{ma_kh}/progress/{ma_hv}", summary="Xem tiến độ học tập (TienDoHocTap) của học viên trong khóa học")
def get_student_progress(ma_kh: str, ma_hv: str, db: Session = Depends(get_db)):
    # Lấy thông tin từ bảng GHI_DANH_HOC_TAP
    enrollment = db.query(GhiDanhHocTap).filter(
        GhiDanhHocTap.MaHV == ma_hv,
        GhiDanhHocTap.MaKH == ma_kh
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Học viên chưa ghi danh khóa học này")
        
    return {
        "MaHV": enrollment.MaHV,
        "MaKH": enrollment.MaKH,
        "NgayDangKy": str(enrollment.NgayDangKy),
        "TrangThaiHoc": enrollment.TrangThaiHoc,
        "TienDoHocTap": f"{enrollment.TienDoHocTap}%", # Miền giá trị [0, 100]
        "ThoiGianTruyCapCuoi": str(enrollment.ThoiGianTruyCapCuoi) if enrollment.ThoiGianTruyCapCuoi else None
    }


@router.post("/tests/submit", summary="Nộp bài test và kiểm tra giới hạn SoLanLamToiDa")
def submit_test(ma_hv: str, ma_test: str, diem_so: float, db: Session = Depends(get_db)):
    # 1. Lấy thông tin bài test để biết SoLanLamToiDa
    test_info = db.query(BaiTest).filter(BaiTest.MaTest == ma_test).first()
    if not test_info:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài test")
    
    # 2. Đếm số lần học viên đã làm bài này trước đó
    existing_attempts = db.query(LanLamBai).filter(
        LanLamBai.MaHV == ma_hv,
        LanLamBai.MaTest == ma_test
    ).all()
    
    current_attempt_count = len(existing_attempts)
    
    # Ràng buộc giới hạn số lần thực hiện[cite: 1]
    if current_attempt_count >= test_info.SoLanLamToiDa:
        raise HTTPException(
            status_code=400, 
            detail=f"Đã vượt quá số lần làm bài tối đa ({test_info.SoLanLamToiDa} lần)."
        )
    
    next_lan_thu = current_attempt_count + 1
    ket_qua = "Đạt" if diem_so >= 5.0 else "Chưa đạt"
    
    new_attempt = LanLamBai(
        MaHV=ma_hv,
        MaTest=ma_test,
        LanThu=next_lan_thu,
        ThoiGianBatDau=datetime.now(),
        ThoiGianNopBai=datetime.now(),
        DiemSo=diem_so, # Thuộc thang điểm hợp lệ[cite: 1]
        KetQua=ket_qua
    )
    db.add(new_attempt)
    db.commit()
    
    return {
        "message": f"Nộp bài thành công lần thứ {next_lan_thu}",
        "diem_so": diem_so,
        "ket_qua": ket_qua
    }


@router.post("/admin/grant-course", summary="Admin thực hiện liên kết TẶNG khóa học cho học viên (TANG_KHOA_HOC)")
def grant_course_to_student(ma_ad: str, ma_hv: str, ma_kh: str, db: Session = Depends(get_db)):
    # Liên kết 3 ngôi giữa ADMIN, HOC_VIEN và KHOA_HOC[cite: 1]
    existing_gift = db.query(TangKhoaHoc).filter(
        TangKhoaHoc.MaAD == ma_ad,
        TangKhoaHoc.MaHV == ma_hv,
        TangKhoaHoc.MaKH == ma_kh
    ).first()
    
    if existing_gift:
        raise HTTPException(status_code=400, detail="Khóa học này đã được Admin tặng cho học viên từ trước.")
        
    new_gift = TangKhoaHoc(
        MaAD=ma_ad,
        MaHV=ma_hv,
        MaKH=ma_kh,
        NgayTang=date.today()
    )
    db.add(new_gift)
    
    # Đồng thời tự động tạo luôn một bản ghi Ghi danh học tập cho học viên nếu chưa có
    existing_enroll = db.query(GhiDanhHocTap).filter(
        GhiDanhHocTap.MaHV == ma_hv,
        GhiDanhHocTap.MaKH == ma_kh
    ).first()
    
    if not existing_enroll:
        auto_enroll = GhiDanhHocTap(
            MaHV=ma_hv,
            MaKH=ma_kh,
            NgayDangKy=date.today(),
            TrangThaiHoc="Được tặng",
            TienDoHocTap=0.0
        )
        db.add(auto_enroll)
        
    db.commit()
    return {"message": "Admin tặng khóa học cho học viên thành công!", "MaAD": ma_ad, "MaHV": ma_hv, "MaKH": ma_kh}