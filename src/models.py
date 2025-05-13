from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, ForeignKey
from typing import List
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class User(db.Model):

    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True)
    username: Mapped[str] = mapped_column(nullable= False)
    firstname: Mapped[str] = mapped_column(nullable = False)
    lastname: Mapped[str] = mapped_column( nullable = False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    comments : Mapped[List["Comment"]] = relationship(back_populates = "author")
    posts: Mapped[List["Post"]] = relationship(back_populates = "author")
    users_followed: Mapped[List["Follower"]] = relationship(back_populates = "users_following")
    users_following:  Mapped[List["Follower"]] = relationship(back_populates = "users_followed")


    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Follower(db.Model):
        __tablename__ = "Follower"

        user_from_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
        user_to_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
        users_following: Mapped["User"] = relationship(back_populates = "users_followed")
        users_followed: Mapped["User"] = relationship(back_populates = "users_following")

        def serialize(self):
             return {
                  "user_from_id" :self.user_from_id,
                  "user_to_id" : self.user_to_id
             }


class Comment(db.Model):
        __tablename__ = "Comment"

        id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
        comment_text: Mapped[str] = mapped_column()
        author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
        post_id: Mapped[int] = mapped_column(nullable = False)
        author: Mapped["User"] = relationship(back_populates="comments")
        post: Mapped["Post"] = relationship(back_populates= "comment")

        def serialize(self):
              return{
                    "id": self.id,
                    "comment_text": self.comment_text,
                    "author_id" : self.author_id,
                    "post_id": self.post_id
              }

class Post(db.Model):
      __tablename__ = "Post"

      id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
      user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
      author: Mapped["User"] = relationship(back_populates="posts")
      media_name: Mapped[List["Media"]] = relationship(back_populates= "post")
      comment: Mapped[List["Comment"]] = relationship(back_populates = "post")

      def serialize(self):
            return{
                  "id": self.id,
                  "user_id": self.user_id
            }

class Media(db.Model):
      __tablename__ = "Media"

      id: Mapped[int] = mapped_column(primary_key = True, autoincrement = True)
      type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
      url: Mapped[str] = mapped_column( nullable =True)
      post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))
      post: Mapped["Post"] = relationship(back_populates = "media_name")

      def serialize(self):
            return{
                  "id": self.id,
                  "type": self.type,
                  "url" : self.url,
                  "post_id": self.post_id
            }
    
    


