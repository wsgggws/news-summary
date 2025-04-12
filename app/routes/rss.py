from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import RSSNotFoundException, RSSSubscribeRepeatException
from app.models.rss import RSSFeed, UserRSS
from app.models.user import User
from app.schemas.rss import RSSSubscribeRequest, RSSSubscribeResponse
from app.services.auth import get_current_user
from app.services.database import get_db

router = APIRouter(prefix="/api/v1/rss", tags=["RSS"])


@router.post("/subscribe", response_model=RSSSubscribeResponse)
async def subscribe_rss(
    data: RSSSubscribeRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    user_id = user.id
    # 检查 RSSFeed 是否已存在
    result = await db.execute(select(RSSFeed).where(RSSFeed.url == str(data.url)))
    rss = result.scalar_one_or_none()

    if not rss:
        rss = RSSFeed(url=str(data.url), title=str(data.title))
        db.add(rss)
        await db.commit()
        await db.flush()
        await db.refresh(rss)

    # 这里需要先记录下值，由于下一次会再执行数据库操作
    rss_id = rss.id
    rss_title = rss.title
    rss_url = rss.url

    # 是否已经订阅
    result = await db.execute(select(UserRSS).where(UserRSS.user_id == user_id, UserRSS.rss_id == rss_id))
    existing = result.scalar_one_or_none()
    if existing:
        raise RSSSubscribeRepeatException

    subscription = UserRSS(user_id=user_id, rss_id=rss_id)
    db.add(subscription)
    await db.commit()
    await db.flush()
    return {"id": rss_id, "title": rss_title, "url": rss_url, "message": "success"}


@router.get("/subscriptions")
async def get_subscriptions(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(RSSFeed).join(UserRSS, RSSFeed.id == UserRSS.rss_id).where(UserRSS.user_id == user.id)
    )
    feeds = result.scalars().all()
    return [{"id": f.id, "url": f.url, "title": f.title} for f in feeds]


@router.delete("/unsubscribe/{rss_id}")
async def unsubscribe_rss(
    rss_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        delete(UserRSS).where(UserRSS.user_id == user.id, UserRSS.rss_id == rss_id).returning(UserRSS.id)
    )
    deleted = result.scalar_one_or_none()
    if not deleted:
        raise RSSNotFoundException
    await db.commit()
    return {"message": "取消订阅成功"}
