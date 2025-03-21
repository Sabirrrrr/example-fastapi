# \"\"\"fresh_start

# Revision ID: 554e1f8eb6be
# Revises: 
# Create Date: 2025-03-11 05:15:02.911415

# \"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '554e1f8eb6be'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    
    # Create nutrient table
    op.create_table('nutrient',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('unit_name', sa.String(), nullable=False),
        sa.Column('nutrient_nbr', sa.String(), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create food table
    op.create_table('food',
        sa.Column('fdc_id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('data_type', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('food_category_id', sa.Integer(), nullable=True),
        sa.Column('publication_date', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('fdc_id')
    )

    # Create food_nutrient table
    op.create_table('food_nutrient',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('fdc_id', sa.Integer(), nullable=False),
        sa.Column('nutrient_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('data_points', sa.Integer(), nullable=True),
        sa.Column('derivation_id', sa.Integer(), nullable=True),
        sa.Column('min_year_acquired', sa.Integer(), nullable=True),
        sa.Column('footnote', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['fdc_id'], ['food.fdc_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['nutrient_id'], ['nutrient.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('food_nutrient')
    op.drop_table('food')
    op.drop_table('nutrient')
    # ### end Alembic commands ###
