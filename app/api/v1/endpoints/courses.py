from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.course import DanhMucKhoaHoc, KhoaHoc, BaiGiang, TaiLieuDinhKem

router = APIRouter(prefix="/courses", tags=["Courses & Categories"])

@router.get("/categories", summary="Lấy danh sách danh mục khóa học phân cấp (Đệ quy cha - con)")
def get_categories(db: Session = Depends(get_db)):
    """
    Lấy toàn bộ danh mục khóa học. Các danh mục gốc (MaDM_Cha is null) 
    sẽ mang theo danh sách các danh mục con bên trong nhờ quan hệ đệ quy.
    """
    # Lấy các danh mục cấp cha (không có cha hoặc MaDM_Cha là null)
    root_categories = db.query(DanhMucKhoaHoc).filter(DanhMucKhoaHoc.MaDM_Cha == None).all()
    
    def build_category_tree(category):
        return {
            "MaDM": category.MaDM,
            "TenDM": category.TenDM,
            "MaDM_Cha": category.MaDM_Cha,
            "children": [build_category_tree(child) for child in category.children]
        }
        
    result = [build_category_tree(cat) for cat in root_categories]
    return {"categories": result}


@router.get("/", summary="Lấy danh sách khóa học (Hỗ trợ lọc theo MaDM và MaGV)")
def get_courses(
    ma_dm: Optional[str] = Query(None, description="Lọc theo mã danh mục"),
    ma_gv: Optional[str] = Query(None, description="Lọc theo mã giảng viên"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách khóa học có thể kèm điều kiện lọc qua query parameters: 
    - /api/v1/courses?ma_dm=...
    - /api/v1/courses?ma_gv=...
    """
    query = db.query(KhoaHoc)
    
    if ma_dm:
        query = query.filter(KhoaHoc.MaDM == ma_dm)
    if ma_gv:
        query = query.filter(KhoaHoc.MaGV == ma_gv)
        
    courses = query.all()
    return {
        "total": len(courses),
        "data": courses
    }


@router.get("/{ma_kh}", summary="Xem chi tiết khóa học (Bao gồm bài giảng và tài liệu đính kèm)")
def get_course_detail(ma_kh: str, db: Session = Depends(get_db)):
    course = db.query(KhoaHoc).filter(KhoaHoc.MaKH == ma_kh).first()
    if not course:
        raise HTTPException(status_code=404, detail="Không tìm thấy khóa học")
    
    # Lấy danh sách bài giảng sắp xếp theo thứ tự
    lectures = db.query(BaiGiang).filter(BaiGiang.MaKH == ma_kh).order_by(BaiGiang.ThuTuBaiHoc).all()
    
    # Đưa thêm thông tin tài liệu đính kèm của từng bài giảng (Thực thể yếu TAI_LIEU_DINH_KEM)
    lectures_with_materials = []
    for lec in lectures:
        materials = db.query(TaiLieuDinhKem).filter(TaiLieuDinhKem.MaBaiGiang == lec.MaBaiGiang).all()
        lectures_with_materials.append({
            "MaBaiGiang": lec.MaBaiGiang,
            "TenBaiGiang": lec.TenBaiGiang,
            "VideoURL": lec.VideoURL,
            "ThuTuBaiHoc": lec.ThuTuBaiHoc,
            "tai_lieu_dinh_kem": materials
        })
    
    return {
        "course": course,
        "lectures": lectures_with_materials
    }