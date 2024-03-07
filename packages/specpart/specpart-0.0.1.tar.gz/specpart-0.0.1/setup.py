from numpy.distutils.core import setup, Extension


setup(
    name="specpart",
    ext_modules=[
        Extension(
            name='specpart',
            sources=[
                "src/specpart/specpart.f90",
            ]
        )
    ]
)