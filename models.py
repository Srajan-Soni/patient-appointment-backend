from pydantic import BaseModel

class UserBase(BaseModel):
    fullname: str
    email: str
    password: str
    
class UserLogin(BaseModel):
    
    email: str 
    password: str    
    
class PatientBase(BaseModel):
    
    name: str
    email: str
    phone: str
    userid: int
    bookedAppointment: bool
    
class PatientSend(BaseModel):
    id : int
    name: str
    email: str
    phone: str
    userid: int
    bookedAppointment: bool    
    
class PatientGet(BaseModel):
    userid : int    
    
class AppointmentBase(BaseModel):
    
    
    date: str
    time: str
    reason: str
    patientId: int
    userId: int
    
class AppointmentId(BaseModel):
    
    id : int    
    
    
        
