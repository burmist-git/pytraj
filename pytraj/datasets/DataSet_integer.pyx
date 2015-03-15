# distutils: language = c++
from cpython.array cimport array as pyarray

# python level
#from pytraj.optional_libs import HAS_NUMPY, ndarray

cdef class DataSet_integer (DataSet_1D):
    def __cinit__(self):
        # TODO : Use only one pointer? 
        self.baseptr0 = <_DataSet*> new _DataSet_integer()
        # make sure 3 pointers pointing to the same address?
        self.baseptr_1 = <_DataSet_1D*> self.baseptr0
        self.thisptr = <_DataSet_integer*> self.baseptr0

        # let Python/Cython free memory
        self.py_free_mem = True

    def __dealloc__(self):
        if self.py_free_mem:
            del self.thisptr

    def alloc(self):
        '''return a memoryview as DataSet instane'''
        cdef DataSet dset = DataSet()
        dset.baseptr0 = self.thisptr.Alloc()
        return dset

    def __getitem__(self, idx):
        #return self.thisptr.index_opr(idx)
        cdef pyarray arr0 = pyarray('i', [])
        cdef int i

        if isinstance(idx, (long, int)):
            return self.thisptr.index_opr(idx)
        elif isinstance(idx, slice):
            if idx == slice(None):
                for i in range(self.size):
                    arr0.append(self.thisptr.index_opr(i))
                return arr0
            else:
                raise NotImplementedError("only support slice(None)")
        else:
            raise NotImplementedError("only support single indexing or slice(None)")


    def __setitem__(self, int idx, int value):
        cdef int * ptr
        ptr = &(self.thisptr.index_opr(idx))
        ptr[0] = value
        
    def __iter__(self):
        cdef int i
        for i in range(self.size):
            yield self.thisptr.index_opr(i)

    def add_element(self, int d):
        self.thisptr.AddElement(d)

    def add(self, int idx, int value):
        self.thisptr.Add(idx, &value)

    #@property
    #def size(self):
    #    return self.thisptr.Size()

