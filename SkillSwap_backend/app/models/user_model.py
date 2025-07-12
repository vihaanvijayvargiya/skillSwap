from pydantic import BaseModel, Field
from typing import List,Optional, Dict
from bson import ObjectId

class User(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    name: str
    phone: str
    email: Optional[str] = None
    profile_photo: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    education: Optional[List[dict]] = []
    experience: Optional[List[dict]] = []
    certifications: Optional[List[dict]] = []
    skills_offered: Optional[List[str]] = []
    skills_wanted: Optional[List[str]] = []
    preferences: Optional[dict] = {}
      # Appointments
    active_sessions: Optional[List[str]] = []  # List of appointment IDs
     # Availability and scheduling
    availability_schedule: Optional[Dict[str, List[str]]] = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": []
    }
    time_slot_duration_minutes: Optional[int] = 15
    
    # Keep track of booked slots
    booked_slots: Optional[Dict[str, List[str]]] = {}

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }
