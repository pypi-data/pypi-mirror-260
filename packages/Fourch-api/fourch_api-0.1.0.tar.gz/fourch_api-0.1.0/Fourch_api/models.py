from typing import List, Optional
from pydantic import BaseModel


class Post(BaseModel):
    no: int
    sticky: Optional[int] = None
    closed: Optional[int] = None
    now: str
    name: str
    sub: Optional[str] = None
    com: Optional[str] = None
    filename: Optional[str] = None
    ext: Optional[str] = None
    w: Optional[int] = None
    h: Optional[int] = None
    tn_w: Optional[int] = None
    tn_h: Optional[int] = None
    tim: Optional[int] = None
    time: int
    md5: Optional[str] = None
    fsize: Optional[int] = None
    resto: int
    capcode: Optional[str] = None
    semantic_url: Optional[str] = None
    replies: Optional[int] = None
    images: Optional[int] = None
    bumplimit: Optional[int] = None
    imagelimit: Optional[int] = None
    omitted_posts: Optional[int] = None
    omitted_images: Optional[int] = None
    tail_size: Optional[int] = None


class Thread(BaseModel):
    posts: List[Post]


class Model(BaseModel):
    threads: List[Thread]
