# Fortran runtime generators


Generates fortan runtime for given DMT blueprints

The generated fortran code depend on fortran modules from other FPM (fortran-package-manager) packages.
The generator will also create a dummy FPM manifest file where the dependencies, including version tag, will be listed.
Note that different versions (version tag) of this repo may use different version of the dependensies.