# -*- coding: utf-8 -*-

from config import Config

c = Config("confibula.cfg")
c.load()
c.params["miaou"]="dit le chat"
c.save()
