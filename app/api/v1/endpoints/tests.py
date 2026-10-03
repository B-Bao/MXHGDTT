from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.learning import BaiTest, LanLamBai

router = APIRouter(prefix="/tests", tags=["Tests & Quizzes"])

@router.get("/course/{ma_kh}", summary="Lấy danh sách các bài test thuộc về một khóa học")
def get_tests_by_course(ma_kh: str, db: Session = Depends(get_db)):
    """
    Lấy danh sách các bài kiểm tra (BAI_TEST) được cấu hình trong khóa học.
    """
    tests = db.query(BaiTest).filter(BaiTest.MaKH == ma_kh).all()
    return {
        "total": len(tests),
        "data": tests
    }


@router.get("/{ma_test}", summary="Lấy thông tin chi tiết bài test (Đề thi)")
def get_test_detail(ma_test: str, db: Session = Depends(get_db)):
    """
    Lấy chi tiết cấu hình bài test: Thời gian làm bài, số lần làm tối đa (SoLanLamToiDa), trạng thái[cite: 1].
    """
    test = db.query(BaiTest).filter(BaiTest.MaTest == ma_test).first()
    if not test:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài test")
    return test


@router.get("/{ma_test}/history/{ma_hv}", summary="Xem lịch sử các lần làm bài của học viên cho một bài test")
def get_student_test_history(ma_test: str, ma_hv: str, db: Session = Depends(get_db)):
    """
    Xem lại lịch sử các lần làm bài trong bảng LAN_LAM_BAI của học viên[cite: 1].
    """
    history = db.query(LanLamBai).filter(
        LanLamBai.MaHV == ma_hv,
        LanLamBai.MaTest == ma_test
    ).all()
    
    return {
        "MaHV": ma_hv,
        "MaTest": ma_test,
        "total_attempts": len(history),
        "attempts": history
    }