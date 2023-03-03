from fastapi import FastAPI

from rental_store.api.api_models import RentFilmRequest

store = FastAPI()

"""
naming convientions Ill use:
DTO - data transfer object in DDD called ValueObject or DataClass - it's mere purpose is to gather and move data togerhter,
it doesn't have any builtin logic in most cases

As I have multiple contexts Ill create such DTOs naming conventions:
- Request/Response - for API layer models
- Params/Results - for service layer model
- Entity - for data layer model 

to transform one type to other Ill use classes called Mappers

"""

