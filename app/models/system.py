from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class PhongLive(Base):
    __tablename__ = "PHONG_LIVE"

    MaLive = Column(String(50), primary_key=True, index=True)
    TenLive = Column(String(200), nullable=False)
    ThoiGianBatDau = Column(DateTime, nullable=False)
    ThoiGianKetThuc = Column(DateTime, nullable=False)
    MaGV = Column(String(50), ForeignKey("GIANG_VIEN.MaGV"), nullable=False)

    giang_vien = relationship("GiangVien", back_populates="phong_live")


class TinTuc(Base):
    __tablename__ = "TIN_TUC"

    MaTin = Column(String(50), primary_key=True, index=True)
    TieuDe = Column(String(200), nullable=False)
    NoiDung = Column(Text, nullable=False)
    ThoiGianDang = Column(DateTime, nullable=False)
    MaAD = Column(String(50), ForeignKey("ADMIN.MaAD"), nullable=False)

    admin = relationship("Admin", back_populates="tin_tuc")


class ThongBao(Base):
    __tablename__ = "THONG_BAO"

    MaTB = Column(String(50), primary_key=True, index=True)
    MaND = Column(String(50), ForeignKey("NGUOI_DUNG.MaND"), nullable=False)
    NoiDung = Column(Text, nullable=False)
    ThoiGianGui = Column(DateTime, nullable=False)
    TrangThai = Column(String(50), nullable=False)

    nguoi_dung = relationship("NguoiDung", back_populates="thong_bao")