# models.py
#
"""
Google App Engine NDB Models
"""

from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def refreshed(self):
        """Pulls the version of the instance entity from the datastore.

        Does not update this instance.

        Returns
        -------
        The instance entity pulled fresh from the datastore.
        """
        return self.key.get(use_cache=False, use_memcache=False)


class Email(BaseModel):
    email = ndb.StringProperty(required=True)

