from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    MaND: str
    HoTen: str
    Email: EmailStr
    SDT: Optional[str] = None
    TaiKhoan: str
    TrangThai: str = "Active"

class UserCreate(UserBase):
    MatKhau: str
    VaiTroPhanLoai: str  # "HOC_VIEN", "GIANG_VIEN", hoặc "ADMIN"
    Lop: Optional[str] = None            # Dành cho học viên
    HocHamHocVi: Optional[str] = None    # Dành cho giảng viên
    ChuyenMon: Optional[str] = None      # Dành cho giảng viên
    VaiTroAdmin: Optional[str] = None    # Dành cho admin

class UserResponse(UserBase):
    NgaySinh: Optional[date] = None
    AnhDaiDien: Optional[str] = None

    class Config:
        from_attributes = True