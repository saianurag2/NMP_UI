from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256
db = SQLAlchemy()
h = sha256()
h.update(b'python1990K00L')
hash_val = h.hexdigest()
print(hash_val)


# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session,sessionmaker
#
# engine = create_engine(os.getenv("sqlite:///user_details.db"))
# db = scoped_session(sessionmaker(bind=engine))
