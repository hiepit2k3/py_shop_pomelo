from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

@dataclass
class CustomResponse:
    time: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    data: Any = None
    page: Optional[int] = None
    status_code: Optional[int] = None

    def to_dict(self):
        response = {
            "time": self.time,
            "data": self.data
        }
        print(self.page)
        print(self.status_code)
        if self.page is not None:
            response["page"] = self.page
        if self.status_code is not None:
            response["status_code"] = self.status_code
        return response
