import enum
from datetime import date, datetime, time

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TaskStatus(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class EventKind(enum.Enum):
    CLASS = "CLASS"
    MEETING = "MEETING"
    HABIT = "HABIT"
    OTHER = "OTHER"


class EventSource(enum.Enum):
    MANUAL = "MANUAL"
    HABIT = "HABIT"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    estimate_min: Mapped[int]
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.TODO)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    sessions: Mapped[list[FocusSession]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    started_at: Mapped[datetime]
    ended_at: Mapped[datetime | None]
    paused_ms: Mapped[int] = mapped_column(default=0)

    task: Mapped[Task] = relationship(back_populates="sessions")
    breaks: Mapped[list[Break]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class Break(Base):
    __tablename__ = "breaks"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("focus_sessions.id", ondelete="CASCADE")
    )
    started_at: Mapped[datetime]
    ended_at: Mapped[datetime | None]

    session: Mapped[FocusSession] = relationship(back_populates="breaks")


class HabitPlan(Base):
    __tablename__ = "habit_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_type: Mapped[str] = mapped_column(String(50))
    params: Mapped[dict] = mapped_column(JSONB)
    start_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    events: Mapped[list[Event]] = relationship(
        back_populates="habit_plan", cascade="all, delete-orphan"
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    kind: Mapped[EventKind]
    day_of_week: Mapped[int | None]  # 0 = Monday ... 6 = Sunday, for weekly events
    event_date: Mapped[date | None]  # for one-off events
    start_time: Mapped[time]
    end_time: Mapped[time]
    source: Mapped[EventSource] = mapped_column(default=EventSource.MANUAL)
    habit_plan_id: Mapped[int | None] = mapped_column(
        ForeignKey("habit_plans.id", ondelete="CASCADE")
    )

    habit_plan: Mapped[HabitPlan | None] = relationship(back_populates="events")