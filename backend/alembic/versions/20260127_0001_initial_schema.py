"""Initial persistence schema for AI Ops Copilot."""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260127_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_tenants_id", "tenants", ["id"], unique=False)

    op.create_table(
        "datasets",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("raw_path", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
    )
    op.create_index("ix_datasets_tenant_id", "datasets", ["tenant_id"], unique=False)
    op.create_index("ix_datasets_tenant_status", "datasets", ["tenant_id", "status"], unique=False)

    op.create_table(
        "olist_orders",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("order_status", sa.String(length=32), nullable=False),
        sa.Column("purchase_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivered_carrier_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivered_customer_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estimated_delivery_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "order_id"),
    )
    op.create_index("ix_olist_orders_tenant_id", "olist_orders", ["tenant_id"], unique=False)
    op.create_index("ix_olist_orders_tenant_status", "olist_orders", ["tenant_id", "order_status"], unique=False)
    op.create_index(
        "ix_olist_orders_tenant_purchase_ts",
        "olist_orders",
        ["tenant_id", "purchase_timestamp"],
        unique=False,
    )

    op.create_table(
        "olist_order_items",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("order_id", sa.String(length=64), nullable=False),
        sa.Column("order_item_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("seller_id", sa.String(length=64), nullable=False),
        sa.Column("shipping_limit_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("freight_value", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.PrimaryKeyConstraint("tenant_id", "order_id", "order_item_id"),
    )
    op.create_index("ix_olist_order_items_tenant_id", "olist_order_items", ["tenant_id"], unique=False)
    op.create_index(
        "ix_olist_order_items_tenant_product",
        "olist_order_items",
        ["tenant_id", "product_id"],
        unique=False,
    )
    op.create_index(
        "ix_olist_order_items_tenant_order",
        "olist_order_items",
        ["tenant_id", "order_id"],
        unique=False,
    )

    op.create_table(
        "olist_products",
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("category_name", sa.String(length=255), nullable=True),
        sa.Column("name_length", sa.Integer(), nullable=True),
        sa.Column("description_length", sa.Integer(), nullable=True),
        sa.Column("photos_qty", sa.Integer(), nullable=True),
        sa.Column("weight_g", sa.Integer(), nullable=True),
        sa.Column("length_cm", sa.Integer(), nullable=True),
        sa.Column("height_cm", sa.Integer(), nullable=True),
        sa.Column("width_cm", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("tenant_id", "product_id"),
    )
    op.create_index("ix_olist_products_tenant_id", "olist_products", ["tenant_id"], unique=False)

    op.create_table(
        "dq_checks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("dataset_id", sa.Integer(), sa.ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("check_name", sa.String(length=128), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("metric_value", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("sample_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_dq_checks_tenant_id", "dq_checks", ["tenant_id"], unique=False)

    op.create_table(
        "metrics_daily",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("category_name", sa.String(length=255), nullable=True),
        sa.Column("revenue", sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column("orders_count", sa.Integer(), nullable=False),
        sa.Column("units_sold", sa.Integer(), nullable=False),
        sa.Column("avg_order_value", sa.Numeric(precision=14, scale=2), nullable=False),
    )
    op.create_index("ix_metrics_daily_tenant_id", "metrics_daily", ["tenant_id"], unique=False)
    op.create_index("ix_metrics_daily_tenant_date", "metrics_daily", ["tenant_id", "date"], unique=False)
    op.create_index(
        "ix_metrics_daily_tenant_category_date",
        "metrics_daily",
        ["tenant_id", "category_name", "date"],
        unique=False,
    )

    op.create_table(
        "insights",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tenant_id", sa.String(length=64), nullable=False),
        sa.Column("dataset_id", sa.Integer(), sa.ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("insight_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("score", sa.Numeric(precision=10, scale=4), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("evidence_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_insights_tenant_id", "insights", ["tenant_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_insights_tenant_id", table_name="insights")
    op.drop_table("insights")

    op.drop_index("ix_metrics_daily_tenant_category_date", table_name="metrics_daily")
    op.drop_index("ix_metrics_daily_tenant_date", table_name="metrics_daily")
    op.drop_index("ix_metrics_daily_tenant_id", table_name="metrics_daily")
    op.drop_table("metrics_daily")

    op.drop_index("ix_dq_checks_tenant_id", table_name="dq_checks")
    op.drop_table("dq_checks")

    op.drop_index("ix_olist_products_tenant_id", table_name="olist_products")
    op.drop_table("olist_products")

    op.drop_index("ix_olist_order_items_tenant_order", table_name="olist_order_items")
    op.drop_index("ix_olist_order_items_tenant_product", table_name="olist_order_items")
    op.drop_index("ix_olist_order_items_tenant_id", table_name="olist_order_items")
    op.drop_table("olist_order_items")

    op.drop_index("ix_olist_orders_tenant_purchase_ts", table_name="olist_orders")
    op.drop_index("ix_olist_orders_tenant_status", table_name="olist_orders")
    op.drop_index("ix_olist_orders_tenant_id", table_name="olist_orders")
    op.drop_table("olist_orders")

    op.drop_index("ix_datasets_tenant_status", table_name="datasets")
    op.drop_index("ix_datasets_tenant_id", table_name="datasets")
    op.drop_table("datasets")

    op.drop_index("ix_tenants_id", table_name="tenants")
    op.drop_table("tenants")
