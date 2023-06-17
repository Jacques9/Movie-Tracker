from fastapi import APIRouter, HTTPException, Query
from api.models.users import Users, UsersReq

router = APIRouter (
    prefix='/user'
)

users = Users()

@router.post('/register')  # url/user/register
def register(user: UsersReq):
    if users.check_if_exists(user.email):
        raise HTTPException(
            status_code=400,
            detail='User already exists'
        )
    
    try:
        users.create_user(user)
    except Exception as _:
        raise HTTPException(
            status_code=500,
            detail='User registration failed'
        )

    return {
        'message': 'User created'
    }

@router.get('/all') # url/user/all
def get_all_users():
    all_users = users.fetch_all_users()

    if len(all_users) == 0:
        raise HTTPException(
            status_code=404,
            detail='There are no users in DB'
        )
    
    users_data = [
        {
            'id': user.id,
            'username': user.get('username'),
            'email': user.get('email'),
            'type': user.get('type'),
            'created_at': user.get('created_at'),
        }
        for user in all_users
    ]

    return users_data

@router.get('/find/{id}') # url/user/find/{id}
def get_user(id: str):
    user_doc = users.fetch_a_user(id)

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    
    user_data = user_doc.to_dict()

    return {
        'id': str(user_doc.id),
        'username': user_data['username'],
        'email': user_data['email'],
        'created_at': user_data['created_at'],
        'type': user_data['type']
    }

@router.delete('/delete/{id}') # url/user/delete/{id}
def delete_user(id: str):
    user_doc = users.fetch_a_user(id)

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    
    user_data = user_doc.to_dict()

    users.delete_a_user(user_data, str(user_doc.id))
    
    return {
        'message': 'User deleted successfully!'
    }

@router.put('/username/{id}')
def replace_username(id: str, new_username: str):
    user_doc = users.fetch_a_user(id)

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )       
    
    users.update_username(id, new_username)

    return {
        'message': 'Username updated successfully!'
    }