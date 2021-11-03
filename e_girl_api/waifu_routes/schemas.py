from typing import Any, Dict, AnyStr, List, Union, Optional

from pydantic import BaseModel, Field
from datetime import datetime


webhookSchema = Union[List[Any], Dict[AnyStr, Any]]