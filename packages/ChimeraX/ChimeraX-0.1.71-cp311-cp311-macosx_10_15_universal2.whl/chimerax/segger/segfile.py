# -----------------------------------------------------------------------------
# Read and write segmentation data in hdf5 format.
#
# Example layout:
#
# format = "segger"
# format_version = 1
#
# name = "somedata segmentation"
# mask = <3-d array of region indices>
# region_ids = <array or region ids numbers, length N>
# region_colors = <array of rgba, N by 4>
# ref_points = <array of region reference points, N by 3>
# parent_ids = <array each regions parent (0 = no parent), length N>
# smoothing_levels = <array of float, length N>
#
# map_path = "/Users/smith/somedata.mrc"
# map_size = (512, 512, 200)
# map_level = 1.245
# ijk_to_xyz_transform = <3x4 matrix>
#
# Region attributes are each written in a separate group named to match
# the attribute name with a type int, float, string appened to the name.
# An array named "attributes" contains names of these group nodes.
#
# attributes = <array of node names>, e.g. ["curvature float", ...]
#
# /curvature float
#   attribute_name = "curvature"
#   ids = <array of region indices, length M>
#   values = <array of values, length M>
#
# skeleton = 'string encoding chimera marker file'
#
# The file is saved with the Python PyTables modules which includes
# additional attributes "VERSION", "CLASS", "TITLE", "PYTABLES_FORMAT_VERSION".
#
# Tests with alternate data storage with every region being a separate HDF
# node and every contact being a separate HDF node gave extremely slow
# read/write speed.
#
def write_segmentation(seg, path = None):

    if path is None:
        show_save_dialog(seg)
        return

    import tables
    h5file = tables.open_file(path, mode = 'w')

    try:

        root = h5file.root
        a = root._v_attrs
        a.format = 'segger'
        a.format_version = 2
        a.name = seg.name

        m = seg.mask
        atom = tables.Atom.from_dtype(m.dtype)
        filters = tables.Filters(complevel=5, complib='zlib')
        ma = h5file.create_carray(root, 'mask', atom, m.shape, filters = filters)
        ma[:] = m

        debug(" - updating region colors...")
        seg.region_colors ()

        from numpy import array, int32, float32
        rlist = list(seg.id_to_region.values())
        rlist.sort(key = lambda r: r.rid)

        rids = array([r.rid for r in rlist], int32)
        h5file.create_array(root, 'region_ids', rids)

        rcolors = array([r.color for r in rlist], float32)
        h5file.create_array(root, 'region_colors', rcolors)

        refpts = array([r.max_point for r in rlist], float32)
        h5file.create_array(root, 'ref_points', refpts)

        slev = array([r.smoothing_level for r in rlist], float32)
        h5file.create_array(root, 'smoothing_levels', slev)

        pids = array([(r.preg.rid if r.preg else 0) for r in rlist], int32)
        h5file.create_array(root, 'parent_ids', pids)

        map = seg.volume_data()
        if map:
            d = map.data
            a.map_path = d.path
            debug(" - map path: " + d.path)
            a.map_size = array(d.size, int32)

        if not seg.map_level is None:
            a.map_level = seg.map_level

        t = seg.point_transform()
        if t:
            from numpy import array, float32
            a.ijk_to_xyz_transform = array(t.matrix, float32)

        write_attributes(h5file, seg)

        if seg.adj_graph:
            write_skeleton(h5file, seg.adj_graph)

    finally:

        h5file.close()

    seg.path = path

# -----------------------------------------------------------------------------
#
def open_segmentation(session, path, name = None, **kw):
    seg = read_segmentation(session, path, open = False)
    if name is not None:
        seg.name = name

    from .segment_dialog import volume_segmentation_dialog
    d = volume_segmentation_dialog(session, create=True)
    d.show_segmentation(seg)

    return [seg], 'Opened %s' % seg.name
  
# -----------------------------------------------------------------------------
#
def save_segmentation(session, path, models = None, **kw):
    if models is None:
        from chimerax.core.errors import UserError
        raise UserError('Must specify segmentation model number to save')
    from .regions import Segmentation
    segs = [m for m in models if isinstance(m, Segmentation)]
    if len(segs) != 1:
        from chimerax.core.errors import UserError
        raise UserError('Can only save 1 segmentation, got %d' % len(models))
    seg = segs[0]
    write_segmentation(seg, path)

# -----------------------------------------------------------------------------
#
def show_open_dialog(session, dir):

    from chimerax.open_command import show_open_file_dialog
    show_open_file_dialog(session, format_name = 'Segmentation',
                          initial_directory = dir)

# -----------------------------------------------------------------------------
#
def show_save_dialog(seg, saved_cb = None):

    if hasattr(seg, 'path'):
        import os.path
        idir, ifile = os.path.split(seg.path)
    else:
        idir = None
        ifile = seg.name

    from chimerax.save_command import show_save_file_dialog
    show_save_file_dialog(seg.session, format = 'Segmentation',
                          initial_directory = idir, initial_file = ifile)

# -----------------------------------------------------------------------------
#
def write_attributes(h5file, seg):

    aa = {}
    for r in seg.all_regions():
        for a,v in list(r.attributes().items()):
            ta = (a, attribute_value_type(v))
            if ta in aa:
                aa[ta].append((r.rid, v))
            else:
                aa[ta] = [(r.rid, v)]

    if len(aa) == 0:
        return              # HDF5 doesn't handle 0 length arrays.

    gnames = []
    from numpy import array, uint32, int32, float64
    for (a,t), vals in list(aa.items()):
        gname = a.replace('/','_') + ' ' + t
        gnames.append(gname)
        g = h5file.create_group("/", gname, 'region attribute')
        g._v_attrs.attribute_name = a
        rid = array([i for i,v in vals], uint32)
        h5file.create_array(g, 'ids', rid, 'region id numbers')
        if t == 'int':
            va = array([v for i,v in vals], int32)
        elif t == 'float':
            va = array([v for i,v in vals], float64)
        elif t == 'string':
            va = [v for i,v in vals]
        elif t == 'image':
            va = [image_to_string(v) for i,v in vals]
        h5file.create_array(g, 'values', va, 'attribute values')
        if t == 'image':
            g._v_attrs.value_type = 'PNG image'

    h5file.create_array(h5file.root, 'attributes', gnames)


# -----------------------------------------------------------------------------
#
def read_attributes(h5file, seg):

    r = h5file.root
    if not hasattr(r, 'attributes'):
        return

    id2r = seg.id_to_region
    for gname in r.attributes:
        g = getattr(r, gname)
        a = g._v_attrs.attribute_name
        ids = g.ids
        values = g.values
        img = (hasattr(g._v_attrs, 'value_type') and
               g._v_attrs.value_type == 'PNG image')
        for id,v in zip(ids,values):
            if id in id2r:
                if img:
                    v = string_to_image(v)
                id2r[id].set_attribute(a, v)

# -----------------------------------------------------------------------------
#
import numpy
import importlib
int_types = (int, numpy.int8, numpy.int16, numpy.int32, numpy.int64,
             numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64)
float_types = (float, numpy.float32, numpy.float64)
def attribute_value_type(v):

    from PIL.Image import Image
    if isinstance(v, int_types):
        return 'int'
    elif isinstance(v, float_types):
        return 'float'
    elif isinstance(v, str):
        return 'string'
    elif isinstance(v, Image):
        return 'image'

    raise TypeError("Can't save value type %s" % str(type(v)))

# -----------------------------------------------------------------------------
#
def image_to_string(image):

    from io import StringIO
    s = StringIO()
    image.save(s, 'PNG')
    return s.getvalue()

# -----------------------------------------------------------------------------
#
def string_to_image(string):

    from io import StringIO
    f = StringIO(string)
    from PIL import Image
    i = Image.open(f)
    return i

# -----------------------------------------------------------------------------
#
def write_skeleton(h5file, mset):

    import io
    s = io.StringIO()
    mset.save_as_xml(s)
    import numpy
    skel = numpy.char.array(str(s.getvalue()), itemsize = 1)
    s.close()
    h5file.create_array(h5file.root, 'skeleton', skel)

# -----------------------------------------------------------------------------
#
def read_segmentation(session, path, open = True, task = None):

    import tables
    f = tables.open_file(path)

    try :

        r = f.root
        a = r._v_attrs
        for n in ('format', 'format_version', 'name'):
            if not n in a:
                raise ValueError('Segmentation file does not have "%s" attribute' % n)
        if a.format not in ('segger', b'segger'):
            raise ValueError('Segmentation file format is not "segger", got "%s"' % a.format)
        if a.format_version != 2:
            raise ValueError('Segmentation file format is not 2')

        import os.path
        fname = os.path.basename(path)

        from .regions import Segmentation
        s = Segmentation(fname, session)

        if 'map_path' in a:
            map_path = a.map_path
            if isinstance(map_path, bytes):
                map_path = map_path.decode('utf8')
            s.map_path = map_path
            debug(" - map path: " + map_path)
        if 'map_level' in a:
            s.map_level = a.map_level
        if 'map_name' in a:
            name = a.map_name
            if isinstance(name, bytes):
                name = name.decode('utf8')
            s.map_name = name
            debug(" - map name: " + name)

        v = map_for_segmentation(session, s.map_path)
        s.set_volume_data(v)

        if 'ijk_to_xyz_transform' in a:
            from chimerax.geometry import Place
            s.ijk_to_xyz_transform = Place(a.ijk_to_xyz_transform)

        s.mask = r.mask.read()
        rids = r.region_ids.read()
        rcolors = r.region_colors.read()
        refpts = r.ref_points.read()
        slevels = r.smoothing_levels.read() if hasattr(r, 'smoothing_levels') else None
        pids = r.parent_ids.read()

        create_regions(s, rids, rcolors, refpts, slevels, pids, task)

        debug(" - created regions")

        read_attributes(f, s)

        read_skeleton(f, s)

        read_patches (f, s)

    finally:

        f.close()

    s.path = path

    if open:
        session.models.add([s])
        
    debug(" - done reading seg file: " + path)
    return s


# -----------------------------------------------------------------------------
#
def map_for_segmentation(session, map_path):

    from chimerax.map import Volume
    for v in session.models.list(type = Volume):
        if v.data.path == map_path:
            return v

    import os.path
    if os.path.exists(map_path):
        from chimerax.map.volume import open_map
        mlist, msg = open_map(session, map_path)
        if len(mlist) == 1:
            v = mlist[0]
            session.models.add([v])
            return v

    return None


# -----------------------------------------------------------------------------
#
def create_regions(s, rids, rcolors, refpts, slevels, pids, task):

    if task:
        task.updateStatus('Making ID table')
    id_to_index = dict([(id,i) for i,id in enumerate(rids)])

    if task:
        task.updateStatus('Collecting child region IDs')
    id_to_child_ids = {}
    n = len(rids)
    for i in range(n):
        pid = pids[i]
        if pid > 0:
            if pid in id_to_child_ids:
                id_to_child_ids[pid].append(rids[i])
            else:
                id_to_child_ids[pid] = [rids[i]]

    if task:
        task.updateStatus('Ordering IDs')
    from .regions import Region
    ids = depth_order(rids, id_to_child_ids, set())
    rlist = []
    for c,rid in enumerate(ids):
        if rid in id_to_child_ids:
            children = [s.id_to_region[cid] for cid in id_to_child_ids[rid]]
        else:
            children = []
        i = id_to_index[rid]
        r = Region(s, rid, refpts[i], children)
        # TODO: Get wrappy error setting surface piece color to numpy array.
        r.color = tuple(rcolors[i])
        if not slevels is None:
            r.smoothing_level = slevels[i]
        rlist.append(r)
        if task and c % 1000 == 0:
            task.updateStatus('Created %d of %d regions' % (c,n))

    if not slevels is None:
        s.smoothing_level = max(slevels)

    return rlist

# -----------------------------------------------------------------------------
#
def depth_order(rids, id_to_child_ids, used):

    idlist = []
    for rid in rids:
        if not rid in used:
            used.add(rid)
            if rid in id_to_child_ids:
                cids = id_to_child_ids[rid]
                idlist.extend(depth_order(cids, id_to_child_ids, used))
            idlist.append(rid)
    return idlist

# -----------------------------------------------------------------------------
#
def read_skeleton(f, s):

    a = f.root
    if not 'skeleton' in a :
        return

    sks = a.skeleton.read().tostring()
    import io
    xml = io.StringIO(sks)
    from VolumePath import markerset
    marker_sets = markerset.load_marker_set_xml(xml, model_id = s.id)
    skel = marker_sets[0]
    skel.show_model(True)

    # Map markers to regions
    id2r = dict([(r.rid, r) for r in s.all_regions()])
    for m in skel.markers():
        rid = int(m.extra_attributes['region_id'])
        m.region = id2r.get(rid, None)
        if m.region is None:
            debug('missing skeleton region %d' % rid)

    s.adj_graph = skel


# -----------------------------------------------------------------------------
#
def read_patches(f, s):

    a = f.root
    if not 'patches' in a :
        return

    debug(" - reading patches:")

    patches = list( a.patches )
    debug(str(patches))

    import chimera
    from . import Mesh
    importlib.reload ( Mesh )
    mesh = None

    for rg in patches:

        rgPath = rg._v_pathname
        debug(" - path: %s" % rgPath)
        rid = rgPath [ len("/patches/"): ]
        debug("  - patch for region %d - type: %s" % (rid, rg._v_attrs["type"]))

        if not 'verts' in rg or not 'tris' in rg :
            debug("  - tris or verts not found")
            continue

        try :
            reg = s.id_to_region[int(rid)]
        except :
            debug(" - did not find region for id")
            continue


        verts = rg.verts.read()
        tris = rg.tris.read()
        debug("   - %d verts, %d tris" % (len(verts), len(tris)))

        if mesh == None :
            mesh = Mesh.MeshFromVertsTris (verts, tris, color=reg.color, m=mesh)
            mesh.name = "patches"
            chimera.openModels.add([mesh])
        else :
            mesh = Mesh.MeshFromVertsTris (verts, tris, color=reg.color, m=mesh)

from .segment_dialog import debug
