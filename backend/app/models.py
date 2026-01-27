from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = (Index("ix_tenants_id", "id"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Dataset(Base):
    __tablename__ = "datasets"
    __table_args__ = (
        Index("ix_datasets_tenant_id", "tenant_id"),
        Index("ix_datasets_tenant_status", "tenant_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False, default="olist")
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_path: Mapped[str] = mapped_column(Text, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class OlistOrder(Base):
    __tablename__ = "olist_orders"
    __table_args__ = (
        Index("ix_olist_orders_tenant_id", "tenant_id"),
        Index("ix_olist_orders_tenant_status", "tenant_id", "order_status"),
        Index("ix_olist_orders_tenant_purchase_ts", "tenant_id", "purchase_timestamp"),
    )

    tenant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_status: Mapped[str] = mapped_column(String(32), nullable=False)
    purchase_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_carrier_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    delivered_customer_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    estimated_delivery_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OlistOrderItem(Base):
    __tablename__ = "olist_order_items"
    __table_args__ = (
        Index("ix_olist_order_items_tenant_id", "tenant_id"),
        Index("ix_olist_order_items_tenant_product", "tenant_id", "product_id"),
        Index("ix_olist_order_items_tenant_order", "tenant_id", "order_id"),
    )

    tenant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), nullable=False)
    seller_id: Mapped[str] = mapped_column(String(64), nullable=False)
    shipping_limit_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    freight_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)


class OlistProduct(Base):
    __tablename__ = "olist_products"
    __table_args__ = (Index("ix_olist_products_tenant_id", "tenant_id"),)

    tenant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    category_name: Mapped[str | None] = mapped_column(String(255))
    name_length: Mapped[int | None] = mapped_column(Integer)
    description_length: Mapped[int | None] = mapped_column(Integer)
    photos_qty: Mapped[int | None] = mapped_column(Integer)
    weight_g: Mapped[int | None] = mapped_column(Integer)
    length_cm: Mapped[int | None] = mapped_column(Integer)
    height_cm: Mapped[int | None] = mapped_column(Integer)
    width_cm: Mapped[int | None] = mapped_column(Integer)


class DQCheck(Base):
    __tablename__ = "dq_checks"
    __table_args__ = (Index("ix_dq_checks_tenant_id", "tenant_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
    dataset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    check_name: Mapped[str] = mapped_column(String(128), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    passed: Mapped[bool] = mapped_column(nullable=False)
    metric_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 6))
    sample_json: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class MetricsDaily(Base):
    __tablename__ = "metrics_daily"
    __table_args__ = (
        Index("ix_metrics_daily_tenant_id", "tenant_id"),
        Index("ix_metrics_daily_tenant_date", "tenant_id", "date"),
        Index("ix_metrics_daily_tenant_category_date", "tenant_id", "category_name", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    category_name: Mapped[str | None] = mapped_column(String(255))
    revenue: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)
    orders_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    units_sold: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_order_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False, default=0)


class Insight(Base):
    __tablename__ = "insights"
    __table_args__ = (Index("ix_insights_tenant_id", "tenant_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
    dataset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
    )
    insight_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    score: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False, default=0)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_json: Mapped[dict | None] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
