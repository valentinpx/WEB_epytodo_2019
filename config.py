DEBUG                   = True
SECRET_KEY              = "BGDIdL2QvSB2feRvCsra_g"

DATABASE_NAME           = "epytodo"
DATABASE_HOST           = "localhost"
DATABASE_SOCK           = None
DATABASE_USER           = "root"
DATABASE_PASS           = ""

SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/epytodo"
SQLALCHEMY_DATABASE_URI = "mysql://" + DATABASE_USER + ":" + DATABASE_PASS + "@" + DATABASE_HOST + "/" + DATABASE_NAME

SQLALCHEMY_TRACK_MODIFICATIONS = False