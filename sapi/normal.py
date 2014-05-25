try:
    unicode
except NameError:
    # Python 3.x
    basestring_ = str
else:
    # Python 2.x
    basestring_ = basestring
