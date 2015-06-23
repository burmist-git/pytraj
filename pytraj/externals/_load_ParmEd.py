from pytraj.utils import has_
from pytraj.warnings import PytrajWarningMissing
from ._load_pseudo_parm import load_pseudo_parm
from ..Trajectory import Trajectory
from ..Frame import Frame

def load_ParmEd(parmed_obj, restype="top"):
    """return pytraj's Topology or Trajectory objects

    Parameters
    ---------
    parmed_obj : ParmEd's Structure object
    restype : str {'top', 'traj'}
       return type
    """
    ptop = load_pseudo_parm(parmed_obj)
    if restype.lower() == 'top':
        return ptop
    elif restype.lower() == 'traj':
        if parmed_obj.coordinates is None:
            raise ValueError("can not convert to Traj with None-coords")
        else:
            coords = parmed_obj.coordinates
            shape = coords.shape
            fa = Trajectory()
            fa.top = ptop
            fa._allocate(shape[0], shape[1])
            fa.update_coordinates(coords)
            return fa
    else:
        raise ValueError("only support `top` or `traj` keyword")

def _load_parmed(parm_name):
    has_parmed = has_("parmed")
    if has_parmed:
        from parmed import load_file
        return load_file(parm_name)
    else:
        if not has_parmed:
            PytrajWarningMissing("`parmed`")
        return None

def to_ParmEd(pytraj_top):
    # TODO: exten to gromacs, charmm too
    # need to change extension
    """convert to ParmEd object"""
    from pytraj.utils.context import goto_temp_folder
    from pytraj.parms.ParmFile import ParmFile
    import parmed as chem

    # I am not a fan of saving/loading again but this might be best choice
    with goto_temp_folder():
        fname = "tmp_pytrajtop.prmtop"
        ParmFile().writeparm(pytraj_top, fname, format="")
        return chem.load_file(fname)
