import requests
from datetime import datetime, date
import os
import hashlib
import bcrypt

from api.models import LoginStore
from api.serializers import LoginStoreSerializer
from api.dfg.nodes.DfgNode import DfgNode


class EateryLogin(DfgNode):

    #def __call__(self, *args, **kwargs):

    def _urlsafe_base_64():
        return hashlib.sha1(os.random(64)).hexdigest()
        
    def renew_session(self):
        self.session_token = _urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    def verify_session_token(self):
        if self.sessionID and date.today() > self.sessionIDExpiration:
            return False
        return True

    def verify_update_token(self, updateToken):
	    return updateToken == self.updateToken

