from asyncio import gather

from fastapi import UploadFile

from app.car_app.repository import CarRepository
from app.car_app.schemas import CarCreatingSchema, CarPartialUpdateSchema, CarSchema, CarUpdatingSchema
from app.core.exceptions import (
    CarCreationError,
    CarDeletingError,
    CarGettingError,
    CarUpdateError,
    UploadFileError,
)
from app.storage.s3 import S3Manager

IMAGE_NAME = '{car_number}_{file_name}'


async def get_cars(repository: CarRepository, s3: S3Manager) -> list[CarSchema]:
    cars = await repository.get_all()

    tasks = [s3.create_presigned_url(car.image) for car in cars]
    urls = await gather(*tasks)
    for car, url in zip(cars, urls):
        car.image = url

    return cars


async def get_car(car_id: int, repository: CarRepository, s3: S3Manager) -> CarSchema:
    car = await repository.get_by_id(car_id)
    car.image = await s3.create_presigned_url(car.image)
    return car


async def create_car(
        creating_schema: CarCreatingSchema,
        file: UploadFile,
        repository: CarRepository,
        s3: S3Manager,
) -> CarSchema:
    file_name = IMAGE_NAME.format(car_number=creating_schema.number, file_name=file.filename)

    uploaded = await s3.upload_file(file, file_name)
    if uploaded is False:
        raise CarCreationError('Cannot update car image', status_code=520)

    created_car = await repository.create(creating_schema, file_name)
    created_car.image = await s3.create_presigned_url(file_name)

    return created_car


async def update_car(
        car_id: int,
        updating_schema: CarUpdatingSchema,
        file: UploadFile,
        repository: CarRepository,
        s3: S3Manager,
) -> CarSchema:
    try:
        file_name = await _upload_file(car_id, file, repository, s3)
    except UploadFileError as err:
        raise CarUpdateError(err.message, err.status_code)

    updated_car = await repository.update(car_id, updating_schema, file_name)
    updated_car.image = await s3.create_presigned_url(file_name)

    return updated_car


async def update_car_partially(
        car_id: int,
        updating_schema: CarPartialUpdateSchema,
        file: UploadFile,
        repository: CarRepository,
        s3: S3Manager,
) -> CarSchema:
    try:
        file_name = await _upload_file(car_id, file, repository, s3)
    except UploadFileError as err:
        raise CarUpdateError(err.message, err.status_code)

    updated_car = await repository.update_partially(car_id, updating_schema, file_name)
    updated_car.image = await s3.create_presigned_url(file_name)

    return updated_car


async def _upload_file(car_id: int, file: UploadFile, repository: CarRepository, s3: S3Manager) -> str:
    try:
        old_car = await repository.get_by_id(car_id)
    except CarGettingError as err:
        raise UploadFileError(err.message, err.status_code)
    file_name = old_car.image

    if file:
        deleted = await s3.delete_objects(file_name)
        if deleted is False:
            raise UploadFileError('Cannot delete car image', status_code=520)

        file_name = IMAGE_NAME.format(car_number=old_car.number, file_name=file.filename)
        uploaded = await s3.upload_file(file, file_name)
        if uploaded is False:
            raise UploadFileError('Cannot update car image', status_code=520)

    return file_name


async def delete_car(car_id: int, repository: CarRepository, s3: S3Manager):
    try:
        car = await repository.get_by_id(car_id)
    except CarGettingError as err:
        raise CarDeletingError(err.message, err.status_code)

    deleted = await s3.delete_objects(car.image)
    if deleted is False:
        raise CarDeletingError('Cannot delete car image', status_code=520)

    await repository.remove(car_id)
