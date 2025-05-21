from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Request
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import RSSInvalidException, RSSNotFoundException, RSSSubscribeRepeatException, UserBannedException
from app.models.rss import RSSArticle, RSSFeed, UserRSS
from app.models.user import User
from app.schemas.rss import RSSSubscribeRequest, RSSSubscribeResponse
from app.services.auth import get_current_user
from app.services.database import get_db
from app.utils.limiter import rss_limiter
from app.utils.validator import get_rss_title
from settings import settings

router = APIRouter(prefix="/api/v1/rss", tags=["RSS"])


@router.post("/subscribe", response_model=RSSSubscribeResponse)
@rss_limiter.limit(f"{settings.RSS_LIMITER}/{settings.RSS_TIME_UNIT}")
async def subscribe_rss(
    request: Request,
    data: RSSSubscribeRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    user_id = user.id
    # 检查 RSSFeed 是否已存在
    result = await db.execute(select(RSSFeed).where(RSSFeed.url == str(data.url)))
    rss = result.scalar_one_or_none()

    if not rss:
        # 是不是有效的 Feed url, 并拿到 title
        title = await get_rss_title(data.url)
        if not title:
            raise RSSInvalidException
        rss = RSSFeed(url=str(data.url), title=title)
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
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    total = await db.scalar(select(func.count()).select_from(UserRSS).where(UserRSS.user_id == user.id))

    result = await db.execute(
        select(RSSFeed)
        .join(UserRSS, RSSFeed.id == UserRSS.rss_id)
        .where(UserRSS.user_id == user.id)
        .offset(offset)
        .limit(limit)
    )
    feeds = result.scalars().all()
    return {
        "items": [{"id": f.id, "url": f.url, "title": f.title} for f in feeds],
        "total": total,
    }


@router.get("/subscriptions/{rss_id}/articles")
async def get_articles_by_subscription(
    rss_id: UUID = Path(...),
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 验证该订阅是否属于该用户
    result = await db.scalar(
        select(func.count())
        .select_from(RSSFeed)
        .join(UserRSS, RSSFeed.id == UserRSS.rss_id)
        .where(UserRSS.user_id == user.id, UserRSS.rss_id == rss_id)
    )
    if result == 0:
        return {"items": [], "total": 0}

    # 查询总数
    total = await db.scalar(select(func.count()).select_from(RSSArticle).where(RSSArticle.rss_id == rss_id))

    # 分页查询文章
    result = await db.execute(
        select(RSSArticle)
        .where(RSSArticle.rss_id == rss_id)
        .order_by(RSSArticle.published_at.desc())
        .offset(offset)
        .limit(limit)
    )
    articles = result.scalars().all()

    return {
        "items": [
            {
                "id": a.id,
                "title": a.title,
                "link": a.link,
                "published_at": a.published_at,
                "summary_md": a.summary_md,
            }
            for a in articles
        ],
        "total": total,
    }


@router.get("/subscriptions/{rss_id}/articles/{article_id}")
async def get_article_detail(
    rss_id: UUID = Path(...),
    article_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 校验该订阅是否属于当前用户
    has_access = await db.scalar(select(UserRSS).where(UserRSS.user_id == user.id, UserRSS.rss_id == rss_id))
    if not has_access:
        raise UserBannedException

    # 查找文章
    result = await db.execute(select(RSSArticle).where(RSSArticle.id == article_id, RSSArticle.rss_id == rss_id))
    article = result.scalar_one_or_none()

    if not article:
        raise RSSNotFoundException

    return {
        "id": article.id,
        "title": article.title,
        "link": article.link,
        "published_at": article.published_at,
        "summary_md": article.summary_md,
    }


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
