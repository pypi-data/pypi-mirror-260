// Copyright (c) 2023, The Endstone Project. (https://endstone.dev) All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "endstone/server.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "endstone/detail/python.h"
#include "endstone/logger.h"
#include "endstone/plugin/plugin_manager.h"

namespace py = pybind11;

namespace endstone::detail {

void init_server(py::module &m)
{
    py_class<PluginManager>(m, "PluginManager");

    py_class<Server>(m, "Server")
        .def_property_readonly("logger", &Server::getLogger, py::return_value_policy::reference,
                               "Returns the primary logger associated with this server instance.")
        .def_property_readonly("plugin_manager", &Server::getPluginManager, py::return_value_policy::reference,
                               "Gets the plugin manager for interfacing with plugins.")
        .def_property_readonly("name", &Server::getVersion, "Gets the name of this server implementation.")
        .def_property_readonly("version", &Server::getVersion, "Gets the name of this server implementation.")
        .def_property_readonly("minecraft_version", &Server::getMinecraftVersion,
                               "Gets the Minecraft version that this server is running.");
}

}  // namespace endstone::detail
