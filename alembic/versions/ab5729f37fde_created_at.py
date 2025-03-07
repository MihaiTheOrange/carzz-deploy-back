"""created at

Revision ID: ab5729f37fde
Revises: 
Create Date: 2024-04-24 16:18:24.315687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab5729f37fde'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_make_title', table_name='make')
    op.drop_table('make')
    op.drop_table('favorites')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_profile_pictures_id', table_name='profile_pictures')
    op.drop_table('profile_pictures')
    op.drop_index('ix_images_id', table_name='images')
    op.drop_table('images')
    op.drop_table('seller_ratings')
    op.drop_index('ix_model_title', table_name='model')
    op.drop_table('model')
    op.drop_index('ix_announcements_title', table_name='announcements')
    op.drop_table('announcements')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('announcements',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('description', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('make', sa.VARCHAR(), nullable=True),
    sa.Column('model', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('mileage', sa.FLOAT(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=True),
    sa.Column('additional_features', sa.VARCHAR(), nullable=True),
    sa.Column('motor_capacity', sa.INTEGER(), nullable=True),
    sa.Column('fuel_type', sa.VARCHAR(), nullable=True),
    sa.Column('gearbox', sa.VARCHAR(), nullable=True),
    sa.Column('car_body', sa.VARCHAR(), nullable=True),
    sa.Column('seats', sa.INTEGER(), nullable=True),
    sa.Column('horsepower', sa.INTEGER(), nullable=True),
    sa.Column('color', sa.VARCHAR(), nullable=True),
    sa.Column('condition', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_announcements_title', 'announcements', ['title'], unique=False)
    op.create_table('model',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('make_id', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_model_title', 'model', ['title'], unique=False)
    op.create_table('seller_ratings',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('seller_id', sa.INTEGER(), nullable=False),
    sa.Column('rating', sa.INTEGER(), nullable=False),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('created_at', sa.VARCHAR(), nullable=False),
    sa.ForeignKeyConstraint(['seller_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('filename', sa.VARCHAR(), nullable=True),
    sa.Column('announcement_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['announcement_id'], ['announcements.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_images_id', 'images', ['id'], unique=False)
    op.create_table('profile_pictures',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('filename', sa.VARCHAR(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_profile_pictures_id', 'profile_pictures', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('full_name', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('county', sa.VARCHAR(), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('favorites',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('announcement_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['announcement_id'], ['announcements.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('make',
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('title')
    )
    op.create_index('ix_make_title', 'make', ['title'], unique=False)
    # ### end Alembic commands ###
