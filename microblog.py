#! .venv/bin/python

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import blog, db
from app.models import User, Post

# cf = blog.config.items()
# for k, v in cf:
#     print(f'{k}: {v}')

@blog.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Post': Post
    }
