from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.system import PhongLive

router = APIRouter(prefix="/lives", tags=["Live Rooms (PHONG_LIVE)"])

@router.get("/", summary="Lấy danh sách các buổi học phát sóng trực tiếp")
def get_live_rooms(db: Session = Depends(get_db)):
    lives = db.query(PhongLive).all()
    return {"total": len(lives), "data": lives}

@router.post("/", summary="Giảng viên tạo phòng live mới")
def create_live_room(
    ma_live: str, 
    ten_live: str, 
    thoi_gian_bat_dau: datetime, 
    thoi_gian_ket_thuc: datetime, 
    ma_gv: str, 
    db: Session = Depends(get_db)
):
    new_live = PhongLive(
        MaLive=ma_live,
        TenLive=ten_live,
        ThoiGianBatDau=thoi_gian_bat_dau,
        ThoiGianKetThuc=thoi_gian_ket_thuc,
        MaGV=ma_gv
    )
    db.add(new_live)
    db.commit()
    return {"message": "Tạo phòng live thành công", "MaLive": ma_live}