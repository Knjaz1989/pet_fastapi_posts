from fastapi import Depends, HTTPException, status

from database.db_async import get_async_session
from . import helpers as hls, db_handlers as db_h
from .dependencies import get_user
from .schemas import PostBase, PostAdd, PostUpdate, \
    PostRate, PostSearch


async def add_post(
    post: PostAdd, user=Depends(get_user), session=Depends(get_async_session)
):
    await db_h.create_post(session, user.id, post.title, post.content)
    return {"status": "Success", "msg": "The post was created successfully"}


async def get_all_posts(user: dict = Depends(get_user)):
    posts = await db_h.get_posts()
    return {"status": "Success", "data": posts}


async def get_current_post(
        post_data: PostBase, user=Depends(get_user),
        session=Depends(get_async_session)
):
    post = db_h.get_post(post_id=post_data.id)
    return {"status": "Success", "data": post}


async def delete_post(
        post_data: PostBase, user=Depends(get_user),
        session=Depends(get_async_session)
):
    await db_h.delete_post(session, user.id, post_data.id)
    return {"status": "Success", "msg": 'The post was deleted successfully'}


async def change_post(
        post_data: PostUpdate, user=Depends(get_user),
        session=Depends(get_async_session)
):
    answer = await db_h.check_owner(session, user.id, post_data.id)
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have not such post'
        )
    await db_h.change_post(
        session, user.id, post_data.id, post_data.title, post_data.content
    )
    return {"status": "Success", "msg": 'The post was changed successfully'}


async def rate_post(post: PostRate, user: dict = Depends(get_user)):
    await hls.set_rate(
        user_id=user.get("id"), post_id=post.id, action=post.action.value
    )
    return {"status": "Success",
            "msg": f'You paste {post.action.value} successfully'}


async def unrate_post(post_data: PostBase, user: dict = Depends(get_user)):
    await db_h.delete_rate(user.get('id'), post_data.id)
    return {"status": "Success", "msg": 'The rate was deleted successfully'}


async def search_post(post_data: PostSearch, user: dict = Depends(get_user)):
    posts = await db_h.search_posts(post_data.title, post_data.content)
    return {'status': 'Success', 'data': posts}
