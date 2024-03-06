# pylint: disable=W0622
"""cubicweb-oauth2 application packaging information"""


modname = "cubicweb_oauth2"
distname = "cubicweb-oauth2"

numversion = (0, 5, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Oauth2/OpenID authentication for cubicweb"
web = "http://www.cubicweb.org/project/%s" % distname

__depends__ = {
    "cubicweb": ">=3.38.0,<3.39.0",
    "authlib": ">=1.2.0,<1.3.0",
    "requests": ">=2.31.0,<2.32.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
]
