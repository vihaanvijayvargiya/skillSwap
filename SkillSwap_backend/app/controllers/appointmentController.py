from fastapi import HTTPException, status, Depends, Query,status as http_status 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from pymongo import ReturnDocument
from bson import ObjectId
from app.database.database import get_db
from app.middlewares.authMiddleware import get_current_user
from datetime import datetime, timedelta
import calendar

# Model for appointment creation
class AppointmentCreateModel(BaseModel):
    user2_id: str
    appointment_date: str  # Format: YYYY-MM-DD
    appointment_time: str  # Format: HH:MM (24-hour format)
    message: str
    
    @validator('appointment_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    @validator('appointment_time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM (24-hour format)")

# Model for listing appointments
class AppointmentResponseModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    user2_id: str
    user2_name: Optional[str] = None
    user_name: Optional[str] = None
    appointment_date: str
    appointment_time: str
    message: str
    status: str
    created_at: datetime
    
    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

# Helper function to check if a time slot is available
async def is_slot_available(db, user2_id, date_str, time_str):
    # Convert to ObjectId
    user2_obj_id = ObjectId(user2_id)
    
    # Get the user2
    user2 = await db["users"].find_one({"_id": user2_obj_id})
    if not user2:
        return False, "user not found"
    
    # Get day of week
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day_of_week = calendar.day_name[date_obj.weekday()].lower()
    except ValueError:
        return False, "Invalid date format"
    
    # Check if user2 works on this day
    availability = user2.get("availability_schedule", {}).get(day_of_week, [])
    if not availability:
        return False, f"User is not available on {day_of_week.capitalize()}"
    
    # Check if the requested time is within available time slots
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    slot_found = False
    
    for time_range in availability:
        start_str, end_str = time_range.split("-")
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()
        
        if start_time <= time_obj < end_time:
            slot_found = True
            break
    
    if not slot_found:
        return False, "Requested time is outside doctor's available hours"
    
    # Check if slot is already booked
    booked_slots = user2.get("booked_slots", {})
    date_slots = booked_slots.get(date_str, [])
    
    if time_str in date_slots:
        return False, "This time slot is already booked"
    
    # All checks passed
    return True, "Slot is available"

# Get all available time slots for a specific user2 on a specific date
async def get_available_slots(
    user2_id: str = Query(..., description="User2 ID"),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_db()
        user2_obj_id = ObjectId(user2_id)
        
        # Get the user2
        user2 = await db["users"].find_one({"_id": user2_obj_id})
        if not user2:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"}
            )
        
        # Get day of week
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = calendar.day_name[date_obj.weekday()].lower()
        except ValueError:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid date format. Use YYYY-MM-DD"}
            )
        
        # Get available time ranges for this day
        availability = user2.get("availability_schedule", {}).get(day_of_week, [])
        if not availability:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": f"User is not available on {day_of_week.capitalize()}",
                    "available_slots": []
                }
            )
        
        # Get already booked slots for this date
        booked_slots = user2.get("booked_slots", {}).get(date, [])
        
        # Generate all possible time slots based on doctor's schedule
        all_slots = []
        slot_duration = user2.get("time_slot_duration_minutes", 15)
        
        for time_range in availability:
            start_str, end_str = time_range.split("-")
            start_time = datetime.strptime(start_str, "%H:%M")
            end_time = datetime.strptime(end_str, "%H:%M")
            
            current_slot = start_time
            while current_slot < end_time:
                slot_str = current_slot.strftime("%H:%M")
                if slot_str not in booked_slots:
                    all_slots.append(slot_str)
                current_slot += timedelta(minutes=slot_duration)
        
        
        # Sort slots
        all_slots.sort()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Available slots for {date}",
                "User2_name": user2.get("name", ""),
                "Skills_offerd": user2.get("skills_offered", []),
                "date": date,
                "day": day_of_week.capitalize(),
                "available_slots": all_slots
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get available slots: {str(e)}"
        )

# Book an appointment
async def book_appointment(
    appointment_data: AppointmentCreateModel,
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_db()
        user_id = current_user["_id"]
        
        # Check if user2 exists
        try:
            user2_obj_id = ObjectId(appointment_data.user2_id)
        except:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Invalid user ID format"}
            )
        
        user2 = await db["users"].find_one({"_id": user2_obj_id})
        if not user2:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"}
            )
        
        
        # Check if slot is available
        is_available, message = await is_slot_available(
            db, 
            appointment_data.user2_id, 
            appointment_data.appointment_date, 
            appointment_data.appointment_time
        )
        
        if not is_available:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": message}
            )
        
        # Create appointment object
        appointment_id = ObjectId()
        appointment = {
            "_id": appointment_id,
            "user_id": user_id,
            "user2_id": user2_obj_id,
            "appointment_date": appointment_data.appointment_date,
            "appointment_time": appointment_data.appointment_time,
            "reason": appointment_data.reason,
            "status": "scheduled",  # scheduled, completed, cancelled
            "created_at": datetime.now()
        }
        
        # Insert appointment
        await db["appointments"].insert_one(appointment)
        
        # Update user's active_sessions
        await db["users"].update_one(
            {"_id": user_id},
            {"$push": {"active_sessions": str(appointment_id)}}
        )
        
        # Update user2's active_patients and booked_slots
        date_key = f"booked_slots.{appointment_data.appointment_date}"
        await db["users"].update_one(
            {"_id": user2_obj_id},
            {"$push": {"active_sessions": str(appointment_id)}}
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Appointment booked successfully",
                "appointment_id": str(appointment_id),
                "user2_name": user2.get("name", ""),
                "appointment_date": appointment_data.appointment_date,
                "appointment_time": appointment_data.appointment_time
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to book appointment: {str(e)}"
        )

# Get user's appointments
async def get_user_appointments(
    status_filter: Optional[str] = Query(None, description="Filter by status (scheduled, completed, cancelled)"),
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_db()
        user_id = current_user["_id"]
        
        # Build query
        query = {"user_id": user_id}
        if status_filter:
            query["status"] = status_filter
        
        # Fetch appointments
        appointments = []
        async for appt in db["appointments"].find(query).sort("appointment_date", 1):
            user2 = await db["users"].find_one({"_id": appt["user2_id"]})
            user2_name = user2.get("name", "Unknown") if user2 else "Unknown"
            appt_with_name = {**appt, "user2_name": user2_name}
            appointments.append(serialize_document(appt_with_name))
        
        return JSONResponse(
            status_code=http_status.HTTP_200_OK,
            content={
                "message": f"Found {len(appointments)} appointment(s)",
                "appointments": appointments
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get appointments: {str(e)}"
        )   


# Update user's availability schedule
async def update_user_availability(
    availability: Dict[str, List[str]],
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_db()
        user_id = current_user["_id"]
        
        # Validate format
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day, slots in availability.items():
            if day not in days:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": f"Invalid day: {day}. Must be one of: {', '.join(days)}"}
                )
            
            # Validate time slots format
            for slot in slots:
                if not isinstance(slot, str) or "-" not in slot:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"message": f"Invalid time slot format: {slot}. Must be in format 'HH:MM-HH:MM'"}
                    )
                
                try:
                    start_str, end_str = slot.split("-")
                    datetime.strptime(start_str, "%H:%M")
                    datetime.strptime(end_str, "%H:%M")
                except ValueError:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"message": f"Invalid time format in slot: {slot}. Use HH:MM-HH:MM (24-hour format)"}
                    )
        
        # Update doctor's availability
        updated_user = await db["users"].find_one_and_update(
            {"_id": user_id},
            {"$set": {"availability_schedule": availability}},
            return_document=ReturnDocument.AFTER
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Availability schedule updated successfully",
                "availability_schedule": updated_user.get("availability_schedule", {})
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update availability: {str(e)}"
        )
# Update user's availability schedule
async def update_user_availability(
    availability: Dict[str, List[str]],
    current_user: dict = Depends(get_current_user)
):
    try:
        db = get_db()
        user_id = current_user["_id"]
        
        # Validate format
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day, slots in availability.items():
            if day not in days:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": f"Invalid day: {day}. Must be one of: {', '.join(days)}"}
                )
            
            # Validate time slots format
            for slot in slots:
                if not isinstance(slot, str) or "-" not in slot:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"message": f"Invalid time slot format: {slot}. Must be in format 'HH:MM-HH:MM'"}
                    )
                
                try:
                    start_str, end_str = slot.split("-")
                    datetime.strptime(start_str, "%H:%M")
                    datetime.strptime(end_str, "%H:%M")
                except ValueError:
                    return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"message": f"Invalid time format in slot: {slot}. Use HH:MM-HH:MM (24-hour format)"}
                    )
        
        # Update user's availability
        updated_user = await db["users"].find_one_and_update(
            {"_id": user_id},
            {"$set": {"availability_schedule": availability}},
            return_document=ReturnDocument.AFTER
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Availability schedule updated successfully",
                "availability_schedule": updated_user.get("availability_schedule", {})
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update availability: {str(e)}"
        )


# Helper function to make MongoDB documents JSON serializable
def serialize_document(doc):
    if isinstance(doc, dict):
        return {k: serialize_document(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()
    else:
        return doc