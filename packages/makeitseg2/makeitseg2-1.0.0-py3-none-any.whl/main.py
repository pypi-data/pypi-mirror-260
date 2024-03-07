"""
developed by Shanu Biswas
"""

__all__ = ['from_data', 'from_file']

from struct import pack_into
import obspy
from .header import BINARY_FILE_HEADER_FORMAT, TRACE_HEADER_FORMAT
from .formats import format_fh, TraceFormat
import os, datetime
import numpy as np


class _Stream(object):
    def __init__(self, src_rcvr_location, traces, ssampling_interval):
        self.src = src_rcvr_location[0]
        self.rcvr = src_rcvr_location[1]
        self.traces = traces
        self.sampling_interval = ssampling_interval
    
    def __len__(self):
        return len(self.rcvr)

def from_data(src_rcvr_location:list, 
              sampling_interval:float, 
              traceArray:np.ndarray | list, 
              newFileName=None, 
              kwargs=dict()):
    """
    Creates a SEG2 (dat) file from stream data.

    Parameters
    ----------
    src_rcvr_location : list
        Container for source and receiver locations. It should be in the following list format:
        [[src_x, src_y], [[rec_1_x, rec_1_y], ..., [rec_NS_x, rec_NS_y]]]
        '_x' and '_y' represent the x and y coordinates respectively.
        1 to Ns in receiver coordinates represents the index of the receiver.

    sampling_interval : float
        Sampling interval in time domain, measured in seconds.

    traceArray : ndarray, list
        Container for time domain trace data. It should have the following structure:
        [[trace_1], [trace_2],....[trace_Ns]]

    newFileName : str
        Name of the new SEG2 file.

    kwargs : dict
        Extra parameters. To include some SEG2 BINARY_FILE_HEADER data, 
        use the keyword "BINARY_FILE_HEADER_data".

    Returns
    --------
    None
    """
    assert len(src_rcvr_location)==2, ValueError(f"src_rcvr_location should have length 2, {len(src_rcvr_location)} given.")
    assert len(src_rcvr_location[0])==2, ValueError(f"source corrdinate should have length 2, (x, y), {len(src_rcvr_location[0])} given.")
    assert len(src_rcvr_location[1])>=1, ValueError()
    assert len(src_rcvr_location[1])==len(traceArray), ValueError()
    # assert any([len(rcvr[0])==2 for rcvr in src_rcvr_location[1]]), ValueError()
    
    info = dict()
    if "BINARY_FILE_HEADER_data" in kwargs.keys():
        info = kwargs["BINARY_FILE_HEADER_data"]
    fh_dict = _fh_initializer(info)
    stream = _Stream(src_rcvr_location, traceArray, sampling_interval)
    trace_header_dict = {
                        "source" : stream.src,
                        "group" : stream.rcvr[0],
                        "samp_int" : stream.sampling_interval
                        }
    th_dict = _th_initializer(trace_header_dict)
    _process(stream, fh_dict, th_dict, newFileName)


def from_file(filename:str, 
              newFileName=None, 
              fdelmodc=False, kwargs=dict()):
    """
    filename    : str | segy or su file name with location
    newFileName : str | seg2 file name if not
                provided new file will be saved 
                as segy file name with .dat extension
                in "Converted_SEG2" folder
    fdelmodc    : bool | True if file is made by fdelmodc software
                otherwise False. default is False 
    kwargs : attribute dict contains

            DATE_TYPE : int | 1: 16-bit ; 2: 32-bit; 
            3: 20-bit, 4: 32-bit
            ======== File Desc Block ==========
            CLIENT : str | file description
                        Block CLIENT
            UNIT :    int | file description
                        Block Note 
            COMPANY : str | file description
                        Block COMPANY       
            INSTRUMENT : str | file description
                        Block INSTRUMENT
            OBSERVER : str | file description
                        Block OBSERVER
            File_NOTE : dict | file description
                        Block Note 
            
            ======== Trace Desc Block ==========
            for each atrribute listed here if only one 
            value is provieded inside the list then
            that value will be assigned for each traces.

            DESCALING_FACTOR : list() | Trace desc block
                        DESCALING FACTOR for each trace. 
            
            RECEIVER : list() | Reciver type
            RECEIVER_SPECS : list | Reciver Specification
            SKEW :  list | SKEW in each trace
            SOURCE : list(<source type>, <Source Param>) |
            Trace_NOTE : Dict | Trace Desc Block Note
            

    """
    # File opening
    assert os.path.exists(filename), FileNotFoundError(f"{filename} file not found!") 
    strm = obspy.read(filename, unpack_trace_headers=True)

    # binary file header and 1st trace header opening for geting buffer size
    if filename.split('.')[-1] == 'su':
        trhead = strm[0].stats.su.trace_header
        binhead = None
        unit, jobid, tsort = [0, 0, 0]
        ftype = 'su'

    elif filename.split('.')[-1] == 'segy':
        trhead = strm[0].stats.segy.trace_header
        binhead = strm.stats.binary_file_header
        unit, jobid, tsort = [binhead.measurement_system, 
            binhead.job_identification_number, binhead.trace_sorting_code]
        ftype = 'segy'
    else:
        raise 'invalid file extention'
    # Strings for File Descriptor Block
    year =trhead.year_data_recorded; day = trhead.day_of_year
    if year==0:    
        today = datetime.date.today()
        year = today.year
    if day==0:
        today = datetime.date.today()
        day = today.day
    info = {
        'day': day,
        'year': year,
        'hh': trhead.hour_of_day,
        'mm': trhead.minute_of_hour,
        'ss': trhead.second_of_minute,
        'jobid': jobid,
        'tsort' : tsort,
        'unit': unit
    }
    fh_dict = _fh_initializer(info)
    th_dict = _th_initializer(strm[0].stats[ftype].trace_header,
                                    binhead, filename, fdelmodc, ftype)
    _process(strm, fh_dict, 
             th_dict, newFileName,
             binhead=binhead, 
             filename=filename, 
             fdelmodc=fdelmodc, 
             ftype=ftype)
        



def _process(stream, fh_dict, 
             th_dict, newFileName ,
             binhead=None, filename=None, 
             fdelmodc=None, ftype=None):
    
    def get_trace_header(id, stream, ftype):
        if ftype is not None:
            return stream[id].stats[ftype].trace_header
        else:
            trace_header_dict = {
                            "source" : stream.src,
                            "group" : stream.rcvr[id],
                            "samp_int" : stream.sampling_interval
                            }
            return trace_header_dict

    def get_trace_data(id, stream, ftype):
        if ftype is not None:
            return stream[id].data
        else:
            return stream.traces[id]
        

    #String Block of FBD
    st = '\x00'  # string terminetor
    str = ''
    for k in list(fh_dict.keys()):   
        s = f'{k} {fh_dict[k]}'
        size = chr(len(s)+3)
        str += f'{size}{st}{s}{st}'    

    str = str[:-1] + f'\n\n{5*chr(0)}'
    fbd_sb = bytes(str, 'ascii')
    fbd_sb_size = len(str)
    #print(fbd_sb_size, fbd_sb)

    #String Block of 1st TBD
    st = '\x00'  # string terminetor
    str = ''
    for k in list(th_dict.keys()):
        s = f'{k} {th_dict[k]}'
        size = chr(len(s)+3)
        str += f'{size}{st}{s}{st}'    

    str = str[:-1] + f'\n\n{5*chr(0)}'
    tbd_sb = bytes(str, 'ascii')
    tbd_sb_size = len(str)
    #print(tbd_sb_size, tbd_sb)

    # Calculate Buffer size
    n_traces = len(stream)
    M = 4*n_traces
    NS = len(get_trace_data(id=0, stream=stream, ftype=ftype))
    backup = n_traces*50
    bufferSize = 32+M + fbd_sb_size + n_traces*(32+ tbd_sb_size + 4*NS) + backup
    #print(bufferSize)

    # Main Process
    #Starting the buffer
    buffer = bytearray(bufferSize)

    # first 32 byte
    fst_block = [85, 58, 1, M, n_traces, b'\x01', b'\x00', b'\x00', b'\x01', b'\n', b'\x00', bytes(f'{(31-13)*chr(0)}', 'ascii')]
    fmt = b'2B3H6c18s'
    pack_into(fmt, buffer, 0, *fst_block)

    # string block FDB
    fmt = b"%is"%(fbd_sb_size)
    offset = 32+M
    pack_into(fmt, buffer, offset, fbd_sb)

    #Trace pointer Sub-block
    offset = 32+M+fbd_sb_size
    pointer = []

    #Trace Block
    st = '\x00'  # string terminetor
    data_format = 4     # 32-bit floating point

    for i in range(n_traces):
        pointer.append(offset)
        trfmt = TraceFormat(bin_fh_dict=binhead, file=filename)
        th_dict = dict()
        for key in list(TRACE_HEADER_FORMAT.keys()):
            th_dict.update({key: trfmt.format_th(key, get_trace_header(id=i, stream=stream, ftype=ftype), fdelflag=fdelmodc, ftype=ftype)})

        str = ''
        for k in list(th_dict.keys()):
            s = f'{k} {th_dict[k]}'
            size = chr(len(s)+3)
            str += f'{size}{st}{s}{st}'    

        str = str[:-1] + f'\n\n{5*chr(0)}'
        tbd_sb = bytes(str, 'ascii')
        tbd_sb_size = len(str)

        Y = data_format*NS
        X = tbd_sb_size+32
        trblock = [17442, X, Y, NS, data_format, bytes(f'{(31-12)*chr(0)}', 'ascii'), tbd_sb]

        fmt = b"2H2IB19s%is"%(tbd_sb_size)
        pack_into(fmt, buffer, offset, *trblock)
        offset += tbd_sb_size 
        if data_format==4:
            fmt = b'%if'%(NS)
        pack_into(fmt, buffer, offset, *get_trace_data(id=i, stream=stream, ftype=ftype))
        offset += 4*NS
    
    # Trace Pointer Sub-block
    p_offset = 32
    fmt = b"%iI"%(n_traces)
    pack_into(fmt, buffer, p_offset, *pointer)

    #save File
    if newFileName == None:
        path = "Converted_SEG2"
        if not os.path.exists(path):
            os.mkdir(path)
        newFileName = path+'/'+filename.split('/')[-1] + ".dat"
    datfile = open(newFileName, 'wb')
    datfile.write(buffer)
    datfile.close()


def _fh_initializer(info:dict=dict()):
    # file header intitializer
    fh_dict= dict()
    for k in list(BINARY_FILE_HEADER_FORMAT.keys()):
        fh_dict.update({k: format_fh(k, info)})
    return fh_dict


def _th_initializer(trace_header_dict:dict, 
                    binhead:dict=dict(), 
                    filename:str=None ,
                    fdelmodc=False, 
                    ftype=None):
    # trace header intitializer
    trfmt = TraceFormat(bin_fh_dict=binhead, file=filename)
    th_dict = dict()
    for key in list(TRACE_HEADER_FORMAT.keys()):
        th_dict.update({key: trfmt.format_th(key, trace_header_dict, fdelflag=fdelmodc, ftype=ftype)})
    return th_dict
    
