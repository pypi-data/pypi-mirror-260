# Copyright 2016 to 2024, Cisco Systems, Inc., All rights reserved.
"""Python backend logic for restconf.

Nothing in this file should use any Django APIs.
"""

from ysyangtree import YSContext, YSYangModels
from ysfilemanager import YSYangSet, split_user_set
from yangsuite.logs import get_logger
from ysrestconf.rmodels import ParseRestconf


log = get_logger(__name__)

# Max depth to generate from any selected tree node
MAX_DEPTH = 6

# Valid REST methods that this plugin supports
REST_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

DEFAULT_CONTENT_TYPES = {
    'xml': 'application/yang-data+xml',
    'json': 'application/yang-data+json',
}


class ParseRestconfError(Exception):
    """General restconf parsing error."""

    def __init__(self, msg=''):
        if not msg:
            raise self
        self.message = msg


def nodes_match(swagobj, node_ids):
    """Check if filtering matches request."""
    if node_ids and not swagobj.tags or swagobj.tags and not node_ids:
        # The cached swagobj does not match the filtering request
        return False
    if swagobj.tags and node_ids:
        for node in swagobj.tags:
            if node not in node_ids:
                # The cached swagobj has different filters so get a new one
                return False
    return True


def get_restconf_parser(ysmodels, **req):
    """Get cached instance of swagger object."""
    node_ids = []

    nodes = req.get('nodes', None)
    names = req.get('models', None)
    user = req.get('user')
    yangset = req.get('yangset')
    host = req.get('host')
    proxyhost = req.get('proxyhost')
    custom_media_types = req.get('custommediatypes', None)
    ncparse = None

    try:
        ncparse = ysmodels.yangs[names[0]]
    except KeyError:
        """ If the module is not inside the YSYangModels object,
        create new YSYangModels object with it, and new YSContext
        """
        owner, setname = split_user_set(yangset)
        ys = YSYangSet.load(owner, setname)
        YSContext.discard_instance(setname, owner)
        ctx = YSContext(ys, setname, [], owner)
        ctx.load_module_files(names)
        ysmodels = YSYangModels(ctx, names)
        YSYangModels.store_instance(ysmodels, user)
        ncparse = ysmodels.yangs[names[0]]

    depth_limit = req.get('depthlimit', None)
    if nodes:
        node_ids = [node['schema_node_id'] for node in nodes]
    if not hasattr(ncparse, 'swagobj') or \
       ysmodels.modelnames != sorted(names) or \
       not nodes_match(ncparse.swagobj, node_ids) or \
       ncparse.host != host or \
       ncparse.depth_limit != depth_limit:
        # Not a match - need a new one
        try:
            """ Get YSContext from YSYangModels object,
            if the context does not have the correct modules loaded,
            load new modules
            """
            ctx = ysmodels.ctx
            ctx_has_correct_modules = False
            ctx_modules = ctx.modules
            for module in ctx_modules:
                if module[0] == names[0]:
                    ctx_has_correct_modules = True
                    break
            if not ctx_has_correct_modules:
                ctx.load_module_files(names)
        except RuntimeError:
            raise ParseRestconfError("Context: No such user")
        except ValueError:
            raise ParseRestconfError("Invalid yangset: " + str(yangset))
        except KeyError:
            raise ParseRestconfError("Context: Bad cache reference")
        except OSError:
            raise ParseRestconfError("No such yangset")
        if ctx is None:
            raise ParseRestconfError("User context not found")
        ncparse.swagobj = ParseRestconf(user, names[0], ctx, node_ids,
                                        host, depth_limit, custom_media_types,
                                        proxyhost=proxyhost)
        ncparse.depth_limit = depth_limit
        ncparse.host = host
        ysmodels.yangs[names[0]] = ncparse
        YSYangModels.store_instance(ysmodels, user)

    if not hasattr(ncparse, 'swagobj'):
        raise ParseRestconfError('Unable to generate APIs')
    else:
        return ncparse.swagobj.get_header(user, page=0)


def generate_swagger(request):
    """Main accessor function for module."""
    user = request.get('user')

    # Do we have a cached yangset instance?
    ysmodels = YSYangModels.get_instance(user)

    if not ysmodels:
        yangset = request.get('yangset')
        models = request.get('models')
        ctx = YSContext.get_instance(user, yangset)

        ysmodels = YSYangModels(ctx, models)
        YSYangModels.store_instance(ysmodels, user)
    return get_restconf_parser(ysmodels, **request)


def get_parse_status(user):
    """Return status of current RESTCONF parser."""
    return ParseRestconf.get_status(user)


def get_header(request):
    """Return OpenAPI header with paths chunk coresponding to chosen page."""
    user = request.user.username
    page = int(request.GET.get('page'))
    return ParseRestconf.get_header(user, page)
