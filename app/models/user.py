from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, UUID, Boolean, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.services.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, nullable=True)

    avatar: Mapped[str | None] = mapped_column(String(256), nullable=True)  # 用户头像 URL
    bio: Mapped[str | None] = mapped_column(String(256), nullable=True)  # 坐右铭
    favorite_sites: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # 常用站点（JSON 格式）
    # 时间统一使用 UTC
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # 关注关系
    following = relationship(
        "UserFollow",
        foreign_keys="[UserFollow.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "UserFollow",
        foreign_keys="[UserFollow.followed_id]",
        back_populates="followed",
        cascade="all, delete-orphan",
    )


class UserFollow(Base):
    __tablename__ = "user_follow"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    follower_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    followed_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    # 关注类型: 关注 / 好友 / 拉黑
    f_type: Mapped[str] = mapped_column(
        Enum("follow", "friend", "blocked", name="follow_type"), default="follow", nullable=False
    )
    remark: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # 关系
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
