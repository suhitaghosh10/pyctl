#include <pybind11/pybind11.h>
#include <projectors/dynamicprojectorextension.h>

namespace py = pybind11;

void init_dynamicprojectorextension(py::module& m)
{
    using namespace CTL;
    using namespace py::literals;

    py::class_<DynamicProjectorExtension, ProjectorExtension>(m, "DynamicProjectorExtension")
        .def(py::init<>())
        .def("configure", &DynamicProjectorExtension::configure, "setup"_a, py::keep_alive<1,2>())
        .def("project", &DynamicProjectorExtension::project, "volume"_a)
        .def("project_composite", &DynamicProjectorExtension::projectComposite, "volume"_a);
}
