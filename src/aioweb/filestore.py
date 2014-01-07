import os
from os.path import join
import glob


class FileStore():
    def __init__(self, path, extensions=["*.rst"]):
        self.path = path
        self.extensions = extensions

    def list_posts(self):
        posts = []
        for ext in self.extensions:
            posts.extend(glob.glob(join(self.path, ext)))
        return posts

    def get_post(self, postid):
        pass
