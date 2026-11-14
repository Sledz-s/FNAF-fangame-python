from setuptools import setup, Extension

module = Extension(
    "random_native",
    sources=["random_module.c"],
)

setup(
    name="FryderykRandom",
    version="0.1",
    ext_modules=[module],
)
