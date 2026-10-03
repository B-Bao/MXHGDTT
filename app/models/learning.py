from sqlalchemy import Column, String, Integer, Float, DateTime, Date, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class BaiTest(Base):
    __tablename__ = "BAI_TEST"

    MaTest = Column(String(50), primary_key=True, index=True)
    MaKH = Column(String(50), ForeignKey("KHOA_HOC.MaKH"), nullable=False)
    TenTest = Column(String(200), nullable=False)
    ThoiGianLamBai = Column(Integer, nullable=False)  # Tính bằng phút
    SoLanLamToiDa = Column(Integer, nullable=False, default=3)
    TrangThai = Column(String(50), nullable=False)

    khoa_hoc = relationship("KhoaHoc", back_populates="bai_test")
    lan_lam_bai = relationship("LanLamBai", back_populates="bai_test", cascade="all, delete-orphan")


class LanLamBai(Base):
    __tablename__ = "LAN_LAM_BAI"

    MaHV = Column(String(50), ForeignKey("HOC_VIEN.MaHV"))
    MaTest = Column(String(50), ForeignKey("BAI_TEST.MaTest"))
    LanThu = Column(Integer)
    ThoiGianBatDau = Column(DateTime, nullable=True)
    ThoiGianNopBai = Column(DateTime, nullable=True)
    DiemSo = Column(Float, nullable=True)
    KetQua = Column(String(50), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('MaHV', 'MaTest', 'LanThu'),
    )

    hoc_vien = relationship("HocVien", back_populates="lan_lam_bai")
    bai_test = relationship("BaiTest", back_populates="lan_lam_bai")


class ThuVien(Base):
    __tablename__ = "THU_VIEN"

    MaTL = Column(String(50), primary_key=True, index=True)
    MaKH = Column(String(50), ForeignKey("KHOA_HOC.MaKH"), nullable=False)
    TenTL = Column(String(200), nullable=False)
    LoaiTL = Column(String(50), nullable=False)
    URL = Column(String(255), nullable=False)
    MoTa = Column(String(500), nullable=True)

    khoa_hoc = relationship("KhoaHoc", back_populates="thu_vien")


class GhiDanhHocTap(Base):
    __tablename__ = "GHI_DANH_HOC_TAP"

    MaHV = Column(String(50), ForeignKey("HOC_VIEN.MaHV"))
    MaKH = Column(String(50), ForeignKey("KHOA_HOC.MaKH"))
    NgayDangKy = Column(Date, nullable=False)
    TrangThaiHoc = Column(String(50), nullable=False)
    TienDoHocTap = Column(Float, nullable=False, default=0.0)
    ThoiGianTruyCapCuoi = Column(DateTime, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('MaHV', 'MaKH'),
    )

    hoc_vien = relationship("HocVien", back_populates="ghi_danh")
    khoa_hoc = relationship("KhoaHoc", back_populates="ghi_danh")


class TangKhoaHoc(Base):
    __tablename__ = "TANG_KHOA_HOC"

    MaAD = Column(String(50), ForeignKey("ADMIN.MaAD"))
    MaHV = Column(String(50), ForeignKey("HOC_VIEN.MaHV"))
    MaKH = Column(String(50), ForeignKey("KHOA_HOC.MaKH"))
    NgayTang = Column(Date, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('MaAD', 'MaHV', 'MaKH'),
    )

    admin = relationship("Admin", back_populates="tang_khoa_hoc")
    hoc_vien = relationship("HocVien", back_populates="tang_khoa_hoc")
    khoa_hoc = relationship("KhoaHoc", back_populates="tang_khoa_hoc")