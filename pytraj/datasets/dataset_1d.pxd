# distutils: language = c++
from .DataSet cimport _DataSet, DataSet


cdef extern from "DataSet_1D.h": 
    cdef cppclass _DataSet_1D "DataSet_1D" (_DataSet):
        _DataSet_1D() 
        _DataSet_1D(_DataSet)
        # virtual methods
        #virtual ~_DataSet_1D() 
        int Allocate1D(size_t)
        double Dval(size_t) const
        double Xcrd(size_t) const
        # end virtual methods
        inline bint IsTorsionArray() const 
        double Avg() const 
        double Avg(double& sd) const 
        double Min() const 
        double Max() const 
        int CrossCorr(const _DataSet_1D&, _DataSet_1D&, int, bint, bint) const 
        double CorrCoeff(const _DataSet_1D&) const 


cdef class DataSet_1D (DataSet):
    # baseptr0 is from DataSet
    cdef _DataSet_1D* baseptr_1
# distutils: language = c++
from libcpp.vector cimport vector
from .DataSet cimport _DataSet, DataSet
from .DataSet_1D cimport _DataSet_1D, DataSet_1D


cdef extern from "DataSet_double.h": 
    cdef cppclass _DatasetDouble "DataSet_double" (_DataSet_1D):
        _DatasetDouble() 
        @staticmethod
        _DataSet * Alloc() 
        double& operator[](size_t idx)
        double& index_opr "operator[]"(size_t idx)
        const vector[double]& Data() const 
        void assign_opr "operator =" (const vector[double]& rhs)
        void AddElement(double d)
        void Resize(size_t sizeIn)
        size_t Size()
        int Sync() 
        void Info() const 
        int Allocate1D(size_t)
        void Add(size_t, const void *)
        double Dval(size_t idx) const 
        double Xcrd(size_t idx) const 
        void Append(const _DatasetDouble&)
        void SetNOE(double b, double bh, double r)
        double NOE_bound() const 
        double NOE_boundH() const 
        double NOE_rexp() const 
        void ShiftTorsions(double, double)


cdef class DatasetDouble (DataSet_1D):
    cdef _DatasetDouble* thisptr
    cdef bint py_free_mem 
# distutils: language = c++
from libcpp.vector cimport vector
from .DataSet cimport _DataSet, DataSet
from .DataSet_1D cimport _DataSet_1D, DataSet_1D


cdef extern from "DataSet_float.h": 
    cdef cppclass _DatasetFloat "DataSet_float" (_DataSet_1D):
        _DatasetFloat() 
        @staticmethod
        _DataSet * Alloc() 
        float& operator[](size_t idx)
        float& index_opr "operator[]"(size_t idx)
        int Size()
        void Resize(size_t)

cdef class DatasetFloat (DataSet_1D):
    cdef _DatasetFloat* thisptr
    cdef bint py_free_mem 

# distutils: language = c++
from libcpp.vector cimport vector
from .DataSet cimport _DataSet, DataSet
from .DataSet_1D cimport _DataSet_1D, DataSet_1D


cdef extern from "DataSet_integer.h": 
    cdef cppclass _DatasetInteger "DataSet_integer" (_DataSet_1D):
        _DatasetInteger() 
        @staticmethod
        _DataSet * Alloc() 
        int& operator[](size_t idx)
        int& index_opr "operator[]"(size_t idx)
        void AddElement(int i)
        int Size()
        void Resize(size_t)
        void Add( size_t, const void* )

cdef class DatasetInteger (DataSet_1D):
    cdef _DatasetInteger* thisptr
    cdef bint py_free_mem 

# distutils: language = c++
from libcpp.string cimport string
from .DataSet cimport _DataSet, DataSet
from .DataSet_1D cimport _DataSet_1D, DataSet_1D


cdef extern from "DataSet_string.h": 
    cdef cppclass _DatasetString "DataSet_string" (_DataSet_1D):
        _DatasetString()
        _DataSet * Alloc() 
        string& index_opr "operator[]"(size_t idx)
        void AddElement(const string& s)
        void Resize(size_t sizeIn)
        int Size()

cdef class DatasetString(DataSet_1D):
    cdef _DatasetString* thisptr
    cdef bint py_free_mem
