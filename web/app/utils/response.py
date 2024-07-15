from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

@dataclass
class CustomResponse:
    time: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))
    data: Any = None
    page: Optional[int] = None
    error_code: Optional[int] = None

    def to_dict(self):
        response = {
            "time": self.time,
            "data": self.data
        }
        print(self.page)
        print(self.error_code)
        if self.page is not None:
            response["page"] = self.page
        if self.error_code is not None:
            response["error_code"] = self.error_code
        return response
