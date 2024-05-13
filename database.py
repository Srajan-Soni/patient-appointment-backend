from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey , Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

DATABASE_URL = "mysql://root:1234@localhost/patient_app"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(16))

    patients = relationship("Patient", back_populates="user")
    appointment = relationship("Appointment", back_populates="user")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    phone = Column(String(12), unique=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"))
    
    bookedAppointment = Column(Boolean, default=False)

    user = relationship("User", back_populates="patients")
    appointment = relationship("Appointment", back_populates="patient")
    

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(10), nullable=False)
    time = Column(String(10), nullable=False)
    reason = Column(String(200),nullable=False)
    userId = Column(Integer, ForeignKey("users.id"))
    patientId = Column(Integer, ForeignKey("patients.id"),unique=True)

    user = relationship("User", back_populates="appointment")
    patient = relationship("Patient", back_populates="appointment")
    
    