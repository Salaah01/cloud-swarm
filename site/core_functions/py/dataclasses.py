from typing import Optional
from dataclasses import dataclass
from django.http import JsonResponse


@dataclass
class APIResponse:
    """Object represents a typical response from an API."""
    success: bool
    error_type: Optional[str] = None
    error: Optional[str] = None
    message: Optional[str] = None
    retuned_object: Optional[object] = None

    def as_dict(self, include_returned_obj: bool = True):
        res = {
            'success': self.success,
            'error_type': self.error_type,
            'error': self.error,
            'message': self.message,
        }
        if include_returned_obj:
            res['returned_object': self.retuned_object]
        return res

    def as_json_response(self, status_code: int = 200):
        return JsonResponse(self.as_dict(False), status=status_code)
