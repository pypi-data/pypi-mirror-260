
from typing import Optional, Set
from pydantic import BaseModel
from datetime import datetime , date

class UserProfileUpdate(BaseModel):
    email:  Optional[str] = None
    username: Optional[str] = None
    aliases: Optional[Set[str]] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile: Optional[str] = None
    dob: Optional[date] = None 
    updt_date: Optional[datetime] = None 
    updt_by_user: Optional[str] = None
    
    def model_dump(self, **kwargs):
            return super().model_dump(exclude_none=True, **kwargs)