from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import update
from models import UserBase,UserLogin,PatientBase,PatientGet,AppointmentBase,PatientSend,AppointmentId
from database import SessionLocal, engine,Base,User,Patient,Appointment
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import stripe


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = "sk_test_51PFDcFSFiJFHUno3Mkj8SV5MkFHPb536uxR8NzYj6lEmjDKmKBlHJYyYvAEuYd6LP519BeNcJ0t9ah1QcNB6SL0U00fUqxkNec"


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup/")
def register_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    print(db_user)
    if db_user is None or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return db_user

@app.post("/addpatients")
def add_patient(patient: PatientBase, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.post("/getpatients", response_model=List[PatientSend])
def get_patients(patient: PatientGet, db: Session = Depends(get_db)):
    patients = db.query(Patient).filter(Patient.userid == patient.userid).all()
    # print(patients)
    for patient in patients:
        print(patient.id,patient.name)
    
    if not patients:
        raise HTTPException(status_code=404, detail="Patients not found")
    return patients

# Getting single patient 

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def update_booked_appointment(patient_id: int):
    db = SessionLocal()
    try:
        
        stmt = update(Patient).where(Patient.id == patient_id).values(bookedAppointment=True)
        db.execute(stmt)
        db.commit()
    finally:
        db.close()
        
@app.get('/payment-link')
async def get_payment_link(id: int):
    
    try:

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Appointment Fee',
                    },
                    'unit_amount': 50000,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/payment-success',
            cancel_url='http://localhost:3000/payment-cancel',    
        )

        return {'payment_link': session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        

@app.post("/createappointment")
def create_appointment(appointment: AppointmentBase,db: Session = Depends(get_db)):
    
    print(appointment)
    
    db_appointment = Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    update_booked_appointment(appointment.patientId)
    return db_appointment


@app.get("/patient/{patient_id}/bookedAppointment", response_model=bool)
def get_patient_booking_status(patient_id: int, db: Session = Depends(get_db)):
    patient = get_patient(db, patient_id=patient_id)
    return patient.bookedAppointment if patient else False

def get_appointment_by_patient_id(db: Session, patient_id: int):
    return db.query(Appointment).filter(Appointment.patientId == patient_id).first()

@app.get("/appointment/{patient_id}", response_model=AppointmentId)
def get_appointment(patient_id: int, db: Session = Depends(get_db)):
    appointment = get_appointment_by_patient_id(db, patient_id=patient_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment