from __future__ import absolute_import, print_function

from pytraj.action_dict import ActionDict
from .externals.six import string_types
from pytraj.DataSetList import DataSetList
from pytraj._get_common_objects import _get_data_from_dtype

adict = ActionDict()

def _update_legend_hbond(_dslist):

    # SER_20@O-SER_20@OG-HG --> SER20_O-SER20_OG-HG
    for d0 in _dslist:
        d0.legend = d0.legend.replace("_", "")
        d0.legend = d0.legend.replace("@", "_")

    for d0 in _dslist:
        if d0.legend == 'HB00000[UU]':
            d0.legend = 'avg_solute_solute'


def search_hbonds_noseries(traj, mask="", dtype='dataset', *args, **kwd):
    """search hbonds for a given mask
    Parameters
    ----------
    traj : {Trajectory-like object, frame_iter object, list of traj}
    mask : str 
        Amber atom mask
    dtype : str {'list', 'pyarray', 'dataset', 'ndarray'}, default='dataset'
    *args, **kwd: optional

    Returns
    -------
    out : DataSetList | pyarray | ndarray | list | dict (depend on 'dtype')

    http://ambermd.org/doc12/Amber15.pdf (page 575)
    """
    update_legend = False
    if 'update_legend' in kwd.keys():
        if kwd['update_legend'] == True:
            update_legend = True
        del kwd['update_legend']

    dslist = DataSetList()
    act = adict['hbond']

    command = mask
    if "series" in command:
        raise ValueError("don't accept key `series`")
    act(command, traj, dslist=dslist, *args, **kwd)
    act.print_output()

    if update_legend:
        _update_legend_hbond(dslist)

    if dtype == 'dataframe':
        # return DataFrame.T to have better visual effect
        return dslist.to_dataframe().T
    else:
        return _get_data_from_dtype(dslist, dtype=dtype)

def search_hbonds(traj, mask="", dtype='dataset', *args, **kwd):
    """search hbonds for a given mask
    Parameters
    ----------
    traj : {Trajectory-like object, frame_iter object, list of traj}
    mask : str 
        Amber atom mask
    dtype : str {'list', 'pyarray', 'dataset', 'ndarray'}, default='dataset'
    *args, **kwd: optional

    Returns
    -------
    out : DataSetList | pyarray | ndarray | list | dict (depend on 'dtype')

    Examples
    --------
    * The syntax was adapted from http://ambermd.org/doc12/Amber15.pdf (page 575)
    * The explaniation in " " is direct excerpt from this manual

    * "search for all hydrogen bonds within residues 1-22"
        dslist = search_hbonds(traj, ":1-22")
        
    * "search for all hydrogen bonds within residues 1-22, specifying output files"

        dslist = search_hbonds(traj, ":1-22 out nhb.dat avgout avghb.dat", dflist=dflist)
        dflist.write_all_datafile()

    * "search for all hydrogen bonds formed between donors in residue 1 and acceptors in residue 2" 

        dslist = search_hbonds(traj, "donormask :1 acceptormask :2", dtype='ndarray'))
   
    See Also
    --------
    http://ambermd.org/doc12/Amber15.pdf (page 575)
    """
    update_legend = False
    if 'update_legend' in kwd.keys():
        if kwd['update_legend'] == True:
            update_legend = True
        del kwd['update_legend']

    dslist = DataSetList()
    act = adict['hbond']

    command = "series " + mask
    act(command, traj, dslist=dslist, *args, **kwd)
    act.print_output()

    if update_legend:
        _update_legend_hbond(dslist)
    if dtype == 'dataframe':
        # return DataFrame.T to have better visual effect
        return dslist.to_dataframe().T
    else:
        return _get_data_from_dtype(dslist, dtype=dtype)

def search_nointramol_hbonds(traj, mask="solventacceptor :WAT@O solventdonor :WAT", 
                             dtype='dataset', *args, **kwd):
    """
    Search hbonds between solute and solvent, ignoring intra-hbond

    Parameters
    ----------
    traj : Trajectory-like or any iterable object that _frame_iter_mater return a Frame
    mask : str, default "solventacceptor :WAT@O solventdonor :WAT"
        cpptraj command
    dtype : str, default 'dataset'
    *args, **kwd: optional

    Examples
    --------
    >>> pyca.search_nointramol_hbonds(traj)
    >>> pyca.search_nointramol_hbonds([traj, traj2], top=traj.top)

    See Also
    --------
       search_hbonds
    """
    update_legend = False
    if 'update_legend' in kwd.keys():
        if kwd['update_legend'] == True:
            update_legend = True
        del kwd['update_legend']

    dslist = DataSetList()
    act = adict['hbond']
    command = "series nointramol " + mask
    act(command, traj, dslist=dslist, *args, **kwd)
    act.print_output()

    if update_legend:
        _update_legend_hbond(dslist)
    return _get_data_from_dtype(dslist, dtype=dtype)
