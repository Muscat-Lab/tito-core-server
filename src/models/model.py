import datetime
import uuid
from typing import List

from snowflake import SnowflakeGenerator
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    Uuid,
)
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .area import Area
from .base import Base, metadata
from .pre_booking import PreBooking
from .seat import Seat

gen = SnowflakeGenerator(42)


class HotPerformance(Base):
    __tablename__ = "hot_performances"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)

    performance: Mapped["Performance"] = relationship(
        back_populates="hot", overlaps="hot_performances"
    )


class Performance(Base):
    __tablename__ = "performances"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    title = mapped_column(String(50), nullable=False)
    running_time = mapped_column(String(30), nullable=False)
    grade = mapped_column(String(30), nullable=False)
    begin = mapped_column(Date, nullable=False)
    end = mapped_column(Date, nullable=False)
    pre_booking_enabled = mapped_column(Boolean, nullable=False)
    pre_booking_closed_at = mapped_column(DateTime(timezone=True), nullable=True)
    poster_image_id = mapped_column(ForeignKey("images.id"), nullable=True)
    snowflake_id = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
        default=lambda: next(gen),
    )
    genre_idents = mapped_column(ARRAY(String), nullable=False, default=[])

    areas: Mapped[List["Area"]] = relationship(back_populates="performance")
    seat_grades: Mapped[List["SeatGrade"]] = relationship(back_populates="performance")
    discounts: Mapped[List["Discount"]] = relationship(back_populates="performance")
    schedules: Mapped[List["Schedule"]] = relationship(back_populates="performance")
    content: Mapped["PerformanceContent"] = relationship(back_populates="performance")
    roles: Mapped[List["Role"]] = relationship(back_populates="performance")
    castings: Mapped[List["Casting"]] = relationship(back_populates="performance")
    poster_image: Mapped["Image"] = relationship(
        "Image",
        foreign_keys=[poster_image_id],
        backref="performances",
        lazy=None,
    )
    like_users: Mapped[List["User"]] = relationship(
        secondary="user_performance_likes", back_populates="like_performances"
    )
    hot: Mapped["HotPerformance"] = relationship(
        "HotPerformance",
        foreign_keys=[HotPerformance.performance_id],
        backref="hot_performances",
    )

    pre_bookings: Mapped[List["PreBooking"]] = relationship(
        back_populates="performance",
    )

    @classmethod
    def create(
        cls,
        title: str,
        running_time: str,
        grade: str,
        begin: datetime.date,
        end: datetime.date,
        pre_booking_enabled: bool,
        pre_booking_closed_at: datetime.datetime | None,
        genre_idents: list[str] | None = None,
    ) -> "Performance":
        return cls(
            title=title,
            running_time=running_time,
            grade=grade,
            begin=begin,
            end=end,
            pre_booking_enabled=pre_booking_enabled,
            pre_booking_closed_at=pre_booking_closed_at,
            genre_idents=genre_idents or [],
        )

    @property
    def poster_image_url(self) -> str | None:
        if self.poster_image is None:
            return None

        from src.config import get_config
        from src.utils.image import get_presigned_url_by_path

        return get_presigned_url_by_path(
            config=get_config(), path=self.poster_image.path
        )

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "running_time": self.running_time,
            "grade": self.grade,
            "begin": self.begin,
            "end": self.end,
            "pre_booking_enabled": self.pre_booking_enabled,
            "pre_booking_closed_at": self.pre_booking_closed_at,
            "poster_image_url": self.poster_image_url,
            "snowflake_id": self.snowflake_id,
        }


class PerformanceContent(Base):
    __tablename__ = "performance_contents"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    showtime_info = mapped_column(Text, nullable=True)
    notice = mapped_column(Text, nullable=True)
    introduction = mapped_column(Text, nullable=True)
    casting_schedule = mapped_column(JSON, nullable=True)
    discount_info = mapped_column(JSON, nullable=True)

    performance: Mapped["Performance"] = relationship(back_populates="content")

    @classmethod
    def create(
        cls,
        performance_id: uuid.UUID,
        notice: str | None = None,
        introduction: str | None = None,
    ) -> "PerformanceContent":
        return cls(
            performance_id=performance_id,
            notice=notice,
            introduction=introduction,
        )


class Location(Base):
    __tablename__ = "locations"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    title = mapped_column(String(150), nullable=False)
    x = mapped_column(Float, nullable=False)
    y = mapped_column(Float, nullable=False)
    address_name = mapped_column(String(150), nullable=False)
    place_name = mapped_column(String(150), nullable=False)
    kakao_place_name = mapped_column(String(150), nullable=False)
    kakao_place_url = mapped_column(String(150), nullable=False)


class Performer(Base):
    __tablename__ = "performers"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = mapped_column(String(20), nullable=False)
    description = mapped_column(Text, nullable=True)
    profile_image_id = mapped_column(ForeignKey("images.id"), nullable=True)

    castings: Mapped[List["Casting"]] = relationship(back_populates="performer")

    users: Mapped[List["User"]] = relationship(
        secondary="user_performer_likes", back_populates="like_performers"
    )

    profile_image: Mapped["Image"] = relationship(
        "Image",
        foreign_keys=[profile_image_id],
        backref="performers",
    )

    @classmethod
    def create(
        cls,
        name: str,
        description: str | None = None,
    ) -> "Performer":
        return cls(
            name=name,
            description=description,
        )

    @property
    def like_count(self) -> int:
        return len(self.users)

    @property
    def profile_image_url(self) -> str | None:
        if self.profile_image is None:
            return None

        from src.config import get_config
        from src.utils.image import get_presigned_url_by_path

        return get_presigned_url_by_path(
            config=get_config(),
            path=self.profile_image.path,
            expires_in=60 * 60 * 24 * 7,
        )


class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = mapped_column(String(20), nullable=False)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="roles")
    castings: Mapped[List["Casting"]] = relationship(back_populates="role")

    @classmethod
    def create(
        cls,
        performance_id: uuid.UUID,
        name: str,
    ) -> "Role":
        return cls(
            performance_id=performance_id,
            name=name,
        )


class Casting(Base):
    __tablename__ = "castings"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    performer_id = mapped_column(ForeignKey("performers.id"), nullable=False)
    role_id = mapped_column(ForeignKey("roles.id"), nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="castings")
    performer: Mapped["Performer"] = relationship(back_populates="castings")
    role: Mapped["Role"] = relationship(back_populates="castings")
    schedules: Mapped[List["ScheduleCasting"]] = relationship(back_populates="casting")

    @classmethod
    def create(
        cls,
        performance_id: uuid.UUID,
        performer_id: uuid.UUID,
        role_id: uuid.UUID,
    ) -> "Casting":
        return cls(
            performance_id=performance_id,
            performer_id=performer_id,
            role_id=role_id,
        )


class Schedule(Base):
    __tablename__ = "schedules"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    date = mapped_column(Date, nullable=False)
    time = mapped_column(Time, nullable=False)

    castings: Mapped[List["ScheduleCasting"]] = relationship(back_populates="schedule")
    performance: Mapped["Performance"] = relationship(back_populates="schedules")

    pre_bookings: Mapped[List["PreBooking"]] = relationship(
        back_populates="schedule",
    )

    @classmethod
    def create(
        cls,
        performance_id: uuid.UUID,
        date: datetime.date,
        time: datetime.time,
    ) -> "Schedule":
        return cls(
            performance_id=performance_id,
            date=date,
            time=time,
        )


class ScheduleCasting(Base):
    __tablename__ = "schedule_casts"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    schedule_id = mapped_column(ForeignKey("schedules.id"), nullable=False)
    casting_id = mapped_column(ForeignKey("castings.id"), nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="castings")
    casting: Mapped["Casting"] = relationship(back_populates="schedules")

    @classmethod
    def create(
        cls,
        schedule_id: uuid.UUID,
        casting_id: uuid.UUID,
    ) -> "ScheduleCasting":
        return cls(
            schedule_id=schedule_id,
            casting_id=casting_id,
        )


class SeatGrade(Base):
    __tablename__ = "seat_grades"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    name = mapped_column(String(30), nullable=False)
    price = mapped_column(Integer, nullable=False)

    snowflake_id = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
        default=lambda: next(gen),
    )

    performance: Mapped["Performance"] = relationship(back_populates="seat_grades")
    seats: Mapped[List["Seat"]] = relationship(back_populates="seat_grade")

    @classmethod
    def create(cls, performance_id, name, price) -> "SeatGrade":
        return cls(
            performance_id=performance_id,
            name=name,
            price=price,
        )


class Discount(Base):
    __tablename__ = "discounts"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    performance_id = mapped_column(ForeignKey("performances.id"), nullable=False)
    name = mapped_column(String(30), nullable=False)
    discount_rate = mapped_column(Float, nullable=False)

    performance: Mapped["Performance"] = relationship(back_populates="discounts")


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    email = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    username = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )
    password = mapped_column(String(256), nullable=False)
    kakao_id = mapped_column(String(256), nullable=True, unique=True, index=True)

    avatar_image_id = mapped_column(ForeignKey("images.id"), nullable=True)

    avatar_image: Mapped["Image"] = relationship(
        "Image",
        foreign_keys=[avatar_image_id],
        backref="users",
    )

    like_performances: Mapped[List["Performance"]] = relationship(
        secondary="user_performance_likes", back_populates="like_users"
    )

    like_performers: Mapped[List["Performer"]] = relationship(
        secondary="user_performer_likes", back_populates="users"
    )

    like_genres: Mapped[List["Genre"]] = relationship(
        secondary="user_genre_likes", back_populates="users"
    )

    pre_bookings: Mapped[List["PreBooking"]] = relationship(
        back_populates="user",
    )

    @classmethod
    def create(cls, email: str, password: str, username: str | None = None) -> "User":
        if username is None:
            username = email.split("@")[0]

        return cls(
            email=email,
            password=password,
            username=username,
        )


class Image(Base):
    __tablename__ = "images"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    path = mapped_column(String(256), nullable=False)
    extension = mapped_column(String(8), nullable=False)


class Genre(Base):
    __tablename__ = "genres"

    id = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = mapped_column(String(30), nullable=False)
    ident = mapped_column(String(30), nullable=False)

    users: Mapped[List["User"]] = relationship(
        secondary="user_genre_likes", back_populates="like_genres"
    )

    @property
    def like_count(self) -> int:
        return len(self.users)


class UserPerformanceLike(Base):
    __tablename__ = "user_performance_likes"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    performance_id = mapped_column(ForeignKey("performances.id"), primary_key=True)

    @classmethod
    def create(
        cls, user_id: uuid.UUID, performance_id: uuid.UUID
    ) -> "UserPerformanceLike":
        return cls(
            user_id=user_id,
            performance_id=performance_id,
        )


class UserPerformerLike(Base):
    __tablename__ = "user_performer_likes"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    performer_id = mapped_column(ForeignKey("performers.id"), primary_key=True)

    @classmethod
    def create(cls, user_id: uuid.UUID, performer_id: uuid.UUID) -> "UserPerformerLike":
        return cls(
            user_id=user_id,
            performer_id=performer_id,
        )


class UserGenreLike(Base):
    __tablename__ = "user_genre_likes"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    genre_id = mapped_column(ForeignKey("genres.id"), primary_key=True)

    @classmethod
    def create(cls, user_id: uuid.UUID, genre_id: uuid.UUID) -> "UserGenreLike":
        return cls(
            user_id=user_id,
            genre_id=genre_id,
        )


__all__ = [
    "metadata",
    "User",
    "Area",
    "Performance",
    "Seat",
    "SeatGrade",
    "Discount",
    "Image",
    "PerformanceContent",
    "Schedule",
    "Performer",
    "Role",
    "Casting",
    "ScheduleCasting",
    "Location",
    "PreBooking",
]
