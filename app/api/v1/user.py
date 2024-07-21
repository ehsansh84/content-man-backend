from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from app.api_models.general import OutputOnlyNote, OutputCreate
from app.api_models.user import Read, Write, Update, Register, Login, ForgotPassword, ResetPassword, ListRead
from app.db_models.user import User as DataModel

module_name = 'user'
module_text = 'User'
router = APIRouter(
    prefix=f"/{module_name}",
    tags=[module_name]
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=OutputCreate)
async def register(item: Register):
    obj = DataModel()
    obj.set_payload(jsonable_encoder(item))
    _id = obj.insert()

    return {
        'detail': f'Registration successful',
        'data': {
            'id': str(_id)
        }
    }


@router.post("/login", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def login(item: Login):
    obj = DataModel()
    obj.set_payload(jsonable_encoder(item))
    # print(obj.username)
    # print(obj.email)
    # print(obj.mobile)
    if obj.login():
        return {'detail': f'Login successful'}
    else:
        return {'detail': f'Login failed'}


@router.post("/forgot_password", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def forgot_password(item: ForgotPassword):
    obj = DataModel()
    obj.set_payload(jsonable_encoder(item))
    # print(obj.username)
    result = obj.list({
      '$or': [
        {'username': item.username},
        {'email': item.username},
        {'mobile': item.username}
      ]
    })
    if len(result) > 0:
        return {'detail': f'An message has been sent to {result[0].email} => Test Code: 1000'}
    else:
        return {'detail': f'Information is not in our database'}


@router.post("/reset_password", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def forgot_password(item: ResetPassword):
    if item.code == '1000':
        obj = DataModel()
        result = obj.list({'email': item.email})
        if len(result) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {item.email} doesn't exists"
            )
        else:
            user = result[0]
            user.load()
            user.password = item.new_password
            user.hash_password()
            user.update()
            return {'detail': 'Password successfully changed'}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OutputCreate)
async def create(item: Write):
    obj = DataModel()
    obj.set_payload(jsonable_encoder(item))
    _id = obj.insert()

    return {
        'detail': f'{module_text} created.',
        'data': {
            'id': str(_id)
        }
    }


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def update(id, item: Update):
    obj = DataModel(_id=id)
    obj.set_payload(jsonable_encoder(item))
    result = obj.update()
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{id} not updated!',
        )
    return {"detail": f"{module_text} successfully updated."}


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=OutputOnlyNote)
async def delete(id):
    obj = DataModel(_id=id)
    result = obj.delete()
    if result['n'] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{module_text} with id {id} not found!',
        )
    return {
        'detail': f'{module_text} deleted.',
        'data': {
            'id': str(id)
        }
    }


@router.get("/", response_description=f"List all {module_text}s", response_model=ListRead)
# @router.get("/", response_description=f"List all {module_text}s")
async def get_list():
    obj = DataModel()
    return obj.list_json()


@router.get("/{id}", response_description=f"Show a {module_text}", response_model=Read)
async def get_one(id):
    obj = DataModel(_id=id)
    obj.load()

    if obj.is_loaded():
        return obj.to_json()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{module_text} with id {id} not found!',
        )
