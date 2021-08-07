#include <Python.h>

double energy(long *sigma, int n_list_length) {
	double H = 0;
	double H1 = 0;
	double H2 = 0;
	long price[] = {100,120,110,110, 70, 80, 40, 30};
	long volum[] = {110,150,120,120,100, 90, 40, 30};
	
	for (int i = 0; i < n_list_length; i++){
		H1 += (double)(price[i]*sigma[i]);
		H2 += (double)(volum[i]*sigma[i]);
	}
	H = -H1 + (300-H2)*(300-H2);
	return H;
}

static PyObject* cc_list_param(PyObject* self, PyObject* args)
{
	int n_list_length;
	PyObject* cc_list, *item;
	if (!PyArg_ParseTuple(args, "O", &cc_list)){
		return NULL;
	}
	if PyList_Check(cc_list){
		n_list_length = (int)PyList_Size(cc_list);
	}else{
		return NULL;
	}

	long sigma[] = {0,0,0,0,0,0,0,0,0,0,0,0};

	for (int i = 0; i < n_list_length; i++){
		item = PyList_GetItem(cc_list, i);
		sigma[i] = PyLong_AsLong(item);
//		Py_DECREF(item);
	}
//	Py_DECREF(cc_list); // Decrement the reference count

	return Py_BuildValue("d", energy(sigma,n_list_length));
}

// Function Definition struct
static PyMethodDef HamiltonianMethods[] = {
	{ "energy", cc_list_param, METH_VARARGS, "ecaluate cost function"},
	{ NULL }
};

// Module Definition struct
static struct PyModuleDef Hamiltonian = {
	PyModuleDef_HEAD_INIT,
	"Hamiltonian",
	"Python3 C API Module(Sample 4)",
	-1,
	HamiltonianMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_Hamiltonian(void)
{
	return PyModule_Create(&Hamiltonian);
}

