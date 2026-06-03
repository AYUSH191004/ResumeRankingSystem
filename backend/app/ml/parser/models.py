import datetime
from typing import Dict
def _empty_result(self, error_message: str) -> Dict:
        """Return empty result with error"""
        return {
            'status': 'error',
            'error': error_message,
            'file_name': None,
            'parsed_at': datetime.utcnow().isoformat()
        }
