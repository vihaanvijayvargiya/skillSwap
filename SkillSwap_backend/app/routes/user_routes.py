from fastapi import APIRouter, Depends,Body
from app.controllers.userController import update_profile, send_user_details,search_users_by_keyword
from app.middlewares.authMiddleware import get_current_user
from typing import List,Optional, Dict


router = APIRouter(tags=["User"])

# ✅ Inject authenticated user
router.put("/update-profile")(update_profile)
router.get("/me", dependencies=[Depends(get_current_user)])(send_user_details)
router.get("/search")(search_users_by_keyword)


# Doctor scheduling routes
@router.put("/update-schedule")
async def update_schedule(
    schedule_data: Dict[str, List[str]] = Body(..., 
        example={
            "monday": ["09:00-12:00", "15:00-18:00"],
            "tuesday": ["09:00-12:00"],
            "wednesday": [],
            "thursday": ["10:00-14:00"],
            "friday": ["09:00-12:00", "13:00-15:00"],
            "saturday": ["10:00-13:00"],
            "sunday": []
        },
        description="Weekly schedule with time ranges in HH:MM-HH:MM format"
    ),
    current_user=Depends(get_current_user)
):
    from app.controllers.appointmentController import update_user_availability
    return await update_user_availability(schedule_data, current_user)