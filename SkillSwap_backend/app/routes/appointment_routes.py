from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.controllers.appointmentController import (
    get_available_slots,
    book_appointment,
    get_user_appointments,
    update_user_availability,
)
from app.middlewares.authMiddleware import get_current_user
from app.models.appointment_model import AppointmentCreateModel

# Create router with appointments tag
router = APIRouter(tags=["Appointments"])

# Routes for patients (regular users)
@router.get("/{user2_id}/available-slots")
async def user_available_slots(
    user2_id: str,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    current_user=Depends(get_current_user)
):
    return await get_available_slots(user2_id, date, current_user)

@router.post("/book-appointment")
async def create_appointment(
    appointment_data: AppointmentCreateModel,
    current_user=Depends(get_current_user)
):
    return await book_appointment(appointment_data, current_user)

@router.get("/my-appointments")
async def user_appointments(
    status: Optional[str] = Query(None, description="Filter by status (scheduled, completed, cancelled)"),
    current_user=Depends(get_current_user)
):
    return await get_user_appointments(status, current_user)


@router.put("/user/availability", dependencies=[Depends(get_current_user)])
async def user_availability(
    availability_data: dict,
    current_user=Depends(get_current_user)
):
    return await update_user_availability(availability_data, current_user)