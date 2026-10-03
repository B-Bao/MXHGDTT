from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class NguoiDung(Base):
    __tablename__ = "NGUOI_DUNG"

    MaND = Column(String(50), primary_key=True, index=True)
    HoTen = Column(String(100), nullable=False)
    NgaySinh = Column(Date, nullable=True)
    Email = Column(String(100), unique=True, index=True, nullable=False)
    SDT = Column(String(20), nullable=True)
    TaiKhoan = Column(String(50), unique=True, index=True, nullable=False)
    MatKhau = Column(String(255), nullable=False)
    AnhDaiDien = Column(String(255), nullable=True)
    TrangThai = Column(String(50), nullable=False, default="Active")

    # Mối quan hệ ISA (1-1 với Học viên, Giảng viên, Admin tùy theo vai trò)
    hoc_vien = relationship("HocVien", back_populates="nguoi_dung", uselist=False, cascade="all, delete-orphan")
    giang_vien = relationship("GiangVien", back_populates="nguoi_dung", uselist=False, cascade="all, delete-orphan")
    admin = relationship("Admin", back_populates="nguoi_dung", uselist=False, cascade="all, delete-orphan")
    
    # Quan hệ 1-N với THONG_BAO
    thong_bao = relationship("ThongBao", back_populates="nguoi_dung", cascade="all, delete-orphan")


class HocVien(Base):
    __tablename__ = "HOC_VIEN"

    MaHV = Column(String(50), ForeignKey("NGUOI_DUNG.MaND", ondelete="CASCADE"), primary_key=True)
    Lop = Column(String(50), nullable=True)

    # Mối quan hệ ngược lại
    nguoi_dung = relationship("NguoiDung", back_populates="hoc_vien")
    
    # Quan hệ liên kết N-M và 3 ngôi
    ghi_danh = relationship("GhiDanhHocTap", back_populates="hoc_vien", cascade="all, delete-orphan")
    lan_lam_bai = relationship("LanLamBai", back_populates="hoc_vien", cascade="all, delete-orphan")
    tang_khoa_hoc = relationship("TangKhoaHoc", back_populates="hoc_vien", cascade="all, delete-orphan")


class GiangVien(Base):
    __tablename__ = "GIANG_VIEN"

    MaGV = Column(String(50), ForeignKey("NGUOI_DUNG.MaND", ondelete="CASCADE"), primary_key=True)
    HocHamHocVi = Column(String(100), nullable=True)
    ChuyenMon = Column(String(255), nullable=True)

    # Mối quan hệ ngược lại
    nguoi_dung = relationship("NguoiDung", back_populates="giang_vien")
    
    # Quan hệ với Khóa học và Phòng Live
    khoa_hoc = relationship("KhoaHoc", back_populates="giang_vien")
    phong_live = relationship("PhongLive", back_populates="giang_vien")


class Admin(Base):
    __tablename__ = "ADMIN"

    MaAD = Column(String(50), ForeignKey("NGUOI_DUNG.MaND", ondelete="CASCADE"), primary_key=True)
    VaiTro = Column(String(100), nullable=False)

    # Mối quan hệ ngược lại
    nguoi_dung = relationship("NguoiDung", back_populates="admin")
    
    # Quan hệ với Tin tức và Tặng khóa học
    tin_tuc = relationship("TinTuc", back_populates="admin")