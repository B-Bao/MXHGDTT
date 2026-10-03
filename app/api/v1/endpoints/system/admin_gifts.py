from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.learning import TangKhoaHoc, GhiDanhHocTap

router = APIRouter(prefix="/admin-gifts", tags=["Admin Grant Courses (TANG_KHOA_HOC)"])

@router.post("/grant-course", summary="Admin thực hiện cấp tặng khóa học cho học viên")
def grant_course_by_admin(
    ma_ad: str, 
    ma_hv: str, 
    ma_kh: str, 
    db: Session = Depends(get_db)
):
    existing_gift = db.query(TangKhoaHoc).filter(
        TangKhoaHoc.MaAD == ma_ad,
        TangKhoaHoc.MaHV == ma_hv,
        TangKhoaHoc.MaKH == ma_kh
    ).first()
    
    if existing_gift:
        raise HTTPException(status_code=400, detail="Khóa học này đã được Admin tặng cho học viên này rồi.")
        
    new_gift = TangKhoaHoc(
        MaAD=ma_ad,
        MaHV=ma_hv,
        MaKH=ma_kh,
        NgayTang=date.today()
    )
    db.add(new_gift)
    
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
    return {"message": "Admin tặng khóa học thành công!", "MaAD": ma_ad, "MaHV": ma_hv, "MaKH": ma_kh}