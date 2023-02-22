from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Post


async def create_post(
        session: AsyncSession,user_id: int, title: str, content: str,
) -> None:
    """Add post into the database"""
    stmt = insert(Post).values(title=title, content=content, user_id=user_id)
    await session.execute(stmt)


async def check_owner(
        session: AsyncSession, user_id: int, post_id: int
) -> bool:
    stmt = select(Post).where(Post.id == post_id, Post.user_id == user_id)
    post = await session.execute(stmt)
    post = post.scalars().first()
    if post:
        return True
    return False


async def delete_post(
        session: AsyncSession, user_id: int, post_id: int
):
    """Delete post from the database"""
    stmt = delete(Post).where(
        Post.id == post_id, Post.user_id == user_id).returning(Post.id)
    post = await session.execute(stmt)
    post = post.scalars().first()
    if post:
        return post


async def change_post(
        session: AsyncSession, user_id: int, post_id: int, title: str = None,
        content: str = None
):
    """Change current post in the database"""
    values = {'title': title, 'content': content}
    for key, value in values.copy().items():
        if not value:
            del values[key]
    stmt = update(Post).where(
        Post.id == post_id, Post.user_id == user_id
    ).values(**values)
    await session.execute(stmt)


async def get_post(post_id: int) -> dict | None:
    """Get current post from the database"""
    query = """
        SELECT * FROM posts WHERE id = :id;
        """
    post = db.fetch_one(query=query, values={'id': post_id})
    if post:
        return dict(post._mapping)


async def get_posts():
    """Get all posts from the database"""
    query = """
        SELECT * FROM posts;
        """
    posts = await db.fetch_all(query=query)
    return posts


async def get_ids_of_all_users_posts(user_id: int):
    pass


async def search_posts(title: str = None, content: str = None):
    """Search posts from the database"""
    select_list = []
    values = {'title': title, 'content': content}
    new_values = {}
    for key, value in values.items():
        if value:
            select_list.append(
                f"STRING_TO_ARRAY(LOWER({key}), ' ') && ARRAY[:{key}]"
            )
            new_values[key] = value
    query = f"""
        SELECT id, title, content FROM posts WHERE {' AND '.join(select_list)}; 
        """
    posts = await db.fetch_all(query=query, values=new_values)
    return posts


async def create_rate(user_id: int, post_id: int, rate: str):
    values = {
        'user_id': user_id, 'post_id': post_id, 'like': False,
        'dislike': False
    }
    values[rate] = True
    query = """
        INSERT INTO rates VALUES (:user_id, :post_id, :like, :dislike)
        """
    await db.execute(query=query, values=values)


async def delete_rate(user_id: int, post_id: int):
    query = """
        DELETE FROM rates 
        WHERE user_id = :user_id AND post_id = :post_id 
        RETURNING *
        """
    rate = await db.fetch_one(
        query=query, values={'user_id': user_id, 'post_id': post_id}
    )
    if not rate:
        return rate


async def get_rate(user_id: int, post_id: int) -> dict | None:
    select_query = """
        SELECT * FROM rates WHERE user_id = :user_id AND post_id = :post_id
        """
    rate = await db.fetch_one(
        query=select_query, values={'user_id': user_id, 'post_id': post_id}
    )
    if rate:
        return dict(rate._mapping)


async def update_rate(user_id: int, post_id: int, action: str):
    final_data = {
        'user_id': user_id, 'post_id': post_id, 'like': False,
        'dislike': False
    }
    if action == 'like':
        final_data['like'] = True
    else:
        final_data['dislike'] = True
    update_query = """
        UPDATE rates
        SET "like" = :like, dislike = :dislike
        WHERE user_id = :user_id AND post_id = :post_id
        """
    await db.execute(query=update_query, values=final_data)
