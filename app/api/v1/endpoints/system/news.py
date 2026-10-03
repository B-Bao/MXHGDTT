from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.system import TinTuc

router = APIRouter(prefix="/news", tags=["Community News (TIN_TUC)"])

@router.get("/", summary="Lấy danh sách tin tức cộng đồng")
def get_news(db: Session = Depends(get_db)):
    news = db.query(TinTuc).order_by(TinTuc.ThoiGianDang.desc()).all()
    return {"total": len(news), "data": news}

@router.post("/", summary="Admin đăng bài viết tin tức mới")
def create_news(
    ma_tin: str, 
    tieu_de: str, 
    noi_dung: str, 
    ma_ad: str, 
    db: Session = Depends(get_db)
):
    new_news = TinTuc(
        MaTin=ma_tin,
        TieuDe=tieu_de,
        NoiDung=noi_dung,
        ThoiGianDang=datetime.now(),
        MaAD=ma_ad
    )
    db.add(new_news)
    db.commit()
    return {"message": "Đăng tin tức thành công", "MaTin": ma_tin}