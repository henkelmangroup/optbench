try:
    import pele.version
    print pele.version.git_revision[:6]
except ImportError:
    print "unknown"


