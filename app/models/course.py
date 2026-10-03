from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DanhMucKhoaHoc(Base):
    __tablename__ = "DANH_MUC_KHOA_HOC"

    MaDM = Column(String(50), primary_key=True, index=True)
    TenDM = Column(String(100), nullable=False)
    MaDM_Cha = Column(String(50), ForeignKey("DANH_MUC_KHOA_HOC.MaDM"), nullable=True)

    # Quan hệ đệ quy cha - con
    parent = relationship("DanhMucKhoaHoc", remote_side=[MaDM], back_populates="children")
    children = relationship("DanhMucKhoaHoc", back_populates="parent")
    
    # Quan hệ với Khóa học
    khoa_hoc = relationship("KhoaHoc", back_populates="danh_muc")


class KhoaHoc(Base):
    __tablename__ = "KHOA_HOC"

    MaKH = Column(String(50), primary_key=True, index=True)
    TenKH = Column(String(200), nullable=False)
    AnhBia = Column(String(255), nullable=True)
    GioiThieu = Column(Text, nullable=True)
    TrangThai = Column(String(50), nullable=False, default="Draft")
    MaGV = Column(String(50), ForeignKey("GIANG_VIEN.MaGV"), nullable=False)
    MaDM = Column(String(50), ForeignKey("DANH_MUC_KHOA_HOC.MaDM"), nullable=False)

    # Quan hệ ngược lại
    giang_vien = relationship("GiangVien", back_populates="khoa_hoc")
    danh_muc = relationship("DanhMucKhoaHoc", back_populates="khoa_hoc")

    # Quan hệ 1-N và N-M khác
    bai_giang = relationship("BaiGiang", back_populates="khoa_hoc", cascade="all, delete-orphan")
    bai_test = relationship("BaiTest", back_populates="khoa_hoc", cascade="all, delete-orphan")
    thu_vien = relationship("ThuVien", back_populates="khoa_hoc", cascade="all, delete-orphan")
    ghi_danh = relationship("GhiDanhHocTap", back_populates="khoa_hoc", cascade="all, delete-orphan")
    tang_khoa_hoc = relationship("TangKhoaHoc", back_populates="khoa_hoc", cascade="all, delete-orphan")


class BaiGiang(Base):
    __tablename__ = "BAI_GIANG"

    MaBaiGiang = Column(String(50), primary_key=True, index=True)
    MaKH = Column(String(50), ForeignKey("KHOA_HOC.MaKH"), nullable=False)
    TenBaiGiang = Column(String(200), nullable=False)
    VideoURL = Column(String(255), nullable=True)
    ThuTuBaiHoc = Column(Integer, nullable=False)

    khoa_hoc = relationship("KhoaHoc", back_populates="bai_giang")
    tai_lieu = relationship("TaiLieuDinhKem", back_populates="bai_giang", cascade="all, delete-orphan")


class TaiLieuDinhKem(Base):
    __tablename__ = "TAI_LIEU_DINH_KEM"

    MaBaiGiang = Column(String(50), ForeignKey("BAI_GIANG.MaBaiGiang"), primary_key=True)
    STTTaiLieu = Column(Integer, primary_key=True)
    TenTaiLieu = Column(String(200), nullable=False)
    URL = Column(String(255), nullable=False)

    bai_giang = relationship("BaiGiang", back_populates="tai_lieu")