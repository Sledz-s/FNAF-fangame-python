
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdint.h>

static uint32_t rng_state = 1;

// ----------------------------------------
// Xorshift32
// ----------------------------------------

static uint32_t xorshift32(void) {
    uint32_t x = rng_state;

    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;

    rng_state = x;

    return x;
}

// ----------------------------------------
// Seed
// ----------------------------------------

static PyObject *rng_seed(PyObject *self, PyObject *args) {
    unsigned long seed;

    if (!PyArg_ParseTuple(args, "k", &seed))
        return NULL;

    rng_state = (uint32_t)seed;

    if (rng_state == 0)
        rng_state = 1;

    Py_RETURN_NONE;
}

// ----------------------------------------
// Random integer
// ----------------------------------------

static PyObject *rng_randint(PyObject *self, PyObject *args) {
    int a, b;

    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;

    if (a > b) {
        PyErr_SetString(PyExc_ValueError, "a must be <= b");
        return NULL;
    }

    uint32_t range = (uint32_t)((int64_t)b - a + 1);
    uint32_t value = xorshift32() % range;

    return PyLong_FromLong((long)((int64_t)a + value));
}

static PyObject *rng_choice(PyObject *self, PyObject *args) {
    PyObject *seq = NULL;

    if(!PyArg_ParseTuple(args, "O", &seq)){
        return NULL;
    }

    Py_ssize_t len = PySequence_Size(seq);
    if (len < 0) {
        return NULL;
    }

    if (len == 0) {
        PyErr_SetString(PyExc_IndexError, "Cannot choose from an empty sequence");
        return NULL;
    }

    uint32_t choosed_index = xorshift32() % (uint32_t)len;
    PyObject *choosed_item = PySequence_GetItem(seq, (Py_ssize_t)choosed_index);

    return choosed_item;
}

// ----------------------------------------
// Module methods
// ----------------------------------------

static PyMethodDef RandomMethods[] = {
    {"seed", rng_seed, METH_VARARGS, "Set RNG seed."},
    {"randint", rng_randint, METH_VARARGS, "Generate random integer."},
    {"choice", rng_choice, METH_VARARGS, "Choose item from list"},
    {NULL, NULL, 0, NULL}
};

// ----------------------------------------
// Module definition
// ----------------------------------------

static struct PyModuleDef random_module = {
    PyModuleDef_HEAD_INIT,
    "random_native",
    NULL,
    -1,
    RandomMethods
};

PyMODINIT_FUNC PyInit_random_native(void) {
    return PyModule_Create(&random_module);
}
