from pydantic import BaseModel


class userBody(BaseModel):
    username: str


class User(BaseModel):
    uuid: str
    username: str

    def dict(self):
        return {
            "uuid": self.uuid,
            "username": self.username,
        }

