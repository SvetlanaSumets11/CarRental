from fastapi import APIRouter, Body, Depends, File, HTTPException, Response, UploadFile

from app.api.services import create_car, delete_car, get_car, get_cars, update_car, update_car_partially
from app.car_app.repository import CarRepository
from app.car_app.schemas import CarCreatingSchema, CarPartialUpdateSchema, CarSchema, CarUpdatingSchema
from app.core.exceptions import (
    CarCreationError,
    CarDeletingError,
    CarGettingError,
    CarUpdateError,
)
from app.storage.s3 import get_s3, S3Manager

router = APIRouter()


@router.get('/cars', response_model=list[CarSchema])
async def retrieve_cars(repository: CarRepository = Depends(), s3: S3Manager = Depends(get_s3)):
    return await get_cars(repository, s3)


@router.get('/cars/{car_id}', response_model=CarSchema)
async def retrieve_car(car_id: int, repository: CarRepository = Depends(), s3: S3Manager = Depends(get_s3)):
    try:
        car = await get_car(car_id, repository, s3)
    except CarGettingError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return car


@router.post('/cars', response_model=CarSchema)
async def add_car(
        creating_schema: CarCreatingSchema = Body(),
        file: UploadFile = File(),
        repository: CarRepository = Depends(),
        s3: S3Manager = Depends(get_s3),
):
    if not file:
        raise HTTPException(status_code=404, detail='No file provided')

    try:
        created_car = await create_car(creating_schema, file, repository, s3)
    except CarCreationError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return created_car


@router.put('/cars/{car_id}', response_model=CarSchema)
async def upgrade_car(
        car_id: int,
        updating_schema: CarUpdatingSchema = Body(),
        file: UploadFile = File(None),
        repository: CarRepository = Depends(),
        s3: S3Manager = Depends(get_s3),
):
    try:
        updated_car = await update_car(car_id, updating_schema, file, repository, s3)
    except CarUpdateError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))

    return updated_car


@router.patch('/cars/{car_id}', response_model=CarSchema)
async def patch_car(
        car_id: int,
        updating_schema: CarPartialUpdateSchema = Body(),
        file: UploadFile = File(None),
        repository: CarRepository = Depends(),
        s3: S3Manager = Depends(get_s3),
):
    try:
        partial_updated_car = await update_car_partially(car_id, updating_schema, file, repository, s3)
    except CarUpdateError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err.message))

    return partial_updated_car


@router.delete('/cars/{car_id}', status_code=204, response_class=Response)
async def remove_car(car_id: int, repository: CarRepository = Depends(), s3: S3Manager = Depends(get_s3)):
    try:
        await delete_car(car_id, repository, s3)
    except CarDeletingError as err:
        raise HTTPException(status_code=err.status_code, detail=str(err))
