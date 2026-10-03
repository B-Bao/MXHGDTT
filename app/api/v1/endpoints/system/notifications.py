from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.system import ThongBao

router = APIRouter(prefix="/notifications", tags=["Notifications (THONG_BAO)"])

@router.get("/{ma_nd}", summary="Lấy danh sách thông báo cá nhân của một người dùng")
def get_user_notifications(ma_nd: str, db: Session = Depends(get_db)):
    notifications = db.query(ThongBao).filter(ThongBao.MaND == ma_nd).order_by(ThongBao.ThoiGianGui.desc()).all()
    return {"MaND": ma_nd, "total": len(notifications), "data": notifications}

@router.post("/", summary="Gửi thông báo cá nhân đến người dùng")
def send_notification(
    ma_tb: str, 
    ma_nd: str, 
    noi_dung: str, 
    db: Session = Depends(get_db)
):
    new_tb = ThongBao(
        MaTB=ma_tb,
        MaND=ma_nd,
        NoiDung=noi_dung,
        ThoiGianGui=datetime.now(),
        TrangThai="Chưa đọc"
    )
    db.add(new_tb)
    db.commit()
    return {"message": "Gửi thông báo thành công", "MaTB": ma_tb}