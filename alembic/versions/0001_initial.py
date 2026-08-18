"""create initial hospital tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-08-13
"""

import sqlalchemy as sa

from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_patients_id",
        "patients",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_patients_email",
        "patients",
        ["email"],
        unique=True,
    )

    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("specialization", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_doctors_id",
        "doctors",
        ["id"],
        unique=False,
    )

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("doctor_id", sa.Integer(), nullable=False),
        sa.Column("appointment_start", sa.DateTime(), nullable=False),
        sa.Column("appointment_end", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_appointments_id",
        "appointments",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_appointments_id", table_name="appointments")
    op.drop_table("appointments")
    op.drop_index("ix_doctors_id", table_name="doctors")
    op.drop_table("doctors")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_index("ix_patients_id", table_name="patients")
    op.drop_table("patients")
