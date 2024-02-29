from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile

from app.api.services import CarService
from app.car_app.schemas import CarCreatingSchema, CarSchema, CarUpdatingSchema
from app.core.exceptions import CarCreationError, CarDeletingError, CarGettingError, CarUpdateError

router = APIRouter(tags=['Car'])


@router.get('/cars', response_model=list[CarSchema])
async def retrieve_cars(car_service: CarService = Depends()):
    return await car_service.get_cars()


@router.get('/cars/{car_id}', response_model=CarSchema)
async def retrieve_car(car_id: int, car_service: CarService = Depends()):
    try:
        car = await car_service.get_car(car_id)
    except CarGettingError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return car


@router.post('/cars', response_model=CarSchema)
async def add_car(
    creating_schema: CarCreatingSchema = Depends(CarCreatingSchema.as_form),
    image: UploadFile = File(),
    car_service: CarService = Depends(),
):
    try:
        created_car = await car_service.create_car(creating_schema, image)
    except CarCreationError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return created_car


@router.put('/cars/{car_id}', response_model=CarSchema)
async def upgrade_car(
    car_id: int,
    updating_schema: CarUpdatingSchema = Depends(CarUpdatingSchema.as_form),
    image: UploadFile = File(),
    car_service: CarService = Depends(),
):
    try:
        updated_car = await car_service.update_car(car_id, updating_schema, image)
    except CarUpdateError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return updated_car


@router.delete('/cars/{car_id}', status_code=204, response_class=Response)
async def remove_car(car_id: int, car_service: CarService = Depends()):
    try:
        await car_service.delete_car(car_id)
    except CarDeletingError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))
