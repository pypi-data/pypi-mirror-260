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

#include "endstone/plugin/plugin.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "endstone/detail/python.h"
#include "endstone/logger.h"
#include "endstone/plugin/plugin_loader.h"
#include "endstone/plugin/plugin_manager.h"
#include "endstone/server.h"

namespace py = pybind11;

namespace endstone::detail {
namespace {
PluginDescription createPluginDescription(std::string name, std::string version,
                                          const std::optional<std::string> &description,
                                          const std::optional<std::vector<std::string>> &authors,
                                          const std::optional<std::string> &prefix, const py::args & /*args*/,
                                          const py::kwargs & /*kwargs*/)
{
    return {std::move(name), std::move(version), description.value_or(""), authors.value_or(std::vector<std::string>()),
            prefix.value_or("")};
}
}  // namespace

class PyPlugin : public Plugin {
public:
    using Plugin::Plugin;

    [[nodiscard]] const PluginDescription &getDescription() const override
    {
        try {
            PYBIND11_OVERRIDE_PURE_NAME(const PluginDescription &, Plugin, "_get_description", getDescription);
        }
        catch (std::exception &e) {
            getLogger().error(e.what());
            std::terminate();
        }
    }

    void onLoad() override
    {
        try {
            PYBIND11_OVERRIDE_NAME(void, Plugin, "on_load", onLoad);
        }
        catch (std::exception &e) {
            getLogger().error("Error occurred when loading {}", getDescription().getFullName());
            getLogger().error(e.what());
        }
    }

    void onEnable() override
    {
        try {
            PYBIND11_OVERRIDE_NAME(void, Plugin, "on_enable", onEnable);
        }
        catch (std::exception &e) {
            getLogger().error("Error occurred when enabling {}.", getDescription().getFullName());
            getLogger().error(e.what());
        }
    }

    void onDisable() override
    {
        try {
            PYBIND11_OVERRIDE_NAME(void, Plugin, "on_disable", onDisable);
        }
        catch (std::exception &e) {
            getLogger().error("Error occurred when disabling {}.", getDescription().getFullName());
            getLogger().error(e.what());
        }
    }
};

class PyPluginLoader : public PluginLoader {
public:
    using PluginLoader::PluginLoader;

    std::vector<Plugin *> loadPlugins(const std::string &directory) override
    {
        try {
            PYBIND11_OVERRIDE_PURE_NAME(std::vector<Plugin *>, PluginLoader, "load_plugins", loadPlugins,
                                        std::ref(directory));
        }
        catch (std::exception &e) {
            server_.getLogger().error("Error occurred when trying to load plugins in '{}': {}", directory, e.what());
            return {};
        }
    }
};

void init_plugin(py::module &m)
{
    py_class<PluginDescription>(m, "PluginDescription")
        .def(py::init(&createPluginDescription), py::arg("name"), py::arg("version"),
             py::arg("description") = py::none(), py::arg("authors") = py::none(), py::arg("prefix") = py::none())
        .def_property_readonly("name", &PluginDescription::getName,
                               "Gives the name of the plugin. This name is a unique identifier for plugins.")
        .def_property_readonly("version", &PluginDescription::getVersion, "Gives the version of the plugin.")
        .def_property_readonly("full_name", &PluginDescription::getFullName,
                               "Returns the name of a plugin, including the version.")
        .def_property_readonly("description", &PluginDescription::getDescription,
                               "Gives a human-friendly description of the functionality the plugin provides.")
        .def_property_readonly("authors", &PluginDescription::getAuthors, "Gives the list of authors for the plugin.")
        .def_property_readonly("prefix", &PluginDescription::getPrefix,
                               "Gives the token to prefix plugin-specific logging messages with.");

    py_class<PluginLoader, PyPluginLoader>(m, "PluginLoader");

    py_class<Plugin, PyPlugin>(m, "Plugin")
        .def(py::init<>())
        .def("on_load", &Plugin::onLoad, "Called after a plugin is loaded but before it has been enabled.")
        .def("on_enable", &Plugin::onEnable, "Called when this plugin is enabled")
        .def("on_disable", &Plugin::onDisable, "Called when this plugin is disabled")
        .def("_get_description", &Plugin::getDescription, py::return_value_policy::reference)
        .def_property_readonly("logger", &Plugin::getLogger, py::return_value_policy::reference,
                               "Returns the plugin logger associated with this server's logger.")
        .def_property_readonly("plugin_loader", &Plugin::getPluginLoader, py::return_value_policy::reference,
                               "Gets the associated PluginLoader responsible for this plugin")
        .def_property_readonly("server", &Plugin::getServer, py::return_value_policy::reference,
                               "Returns the Server instance currently running this plugin")
        .def_property_readonly("enabled", &Plugin::isEnabled,
                               "Returns a value indicating whether or not this plugin is currently enabled")
        .def_property_readonly("name", &Plugin::getName, "Returns the name of the plugin.");

    py_class<PluginLoader, PyPluginLoader>(m, "PluginLoader")
        .def(py::init<Server &>(), py::arg("server"))
        .def("load_plugins", &PluginLoader::loadPlugins, py::arg("directory"),
             py::return_value_policy::reference_internal, "Loads the plugin contained within the specified directory")
        .def("enable_plugin", &PluginLoader::enablePlugin, py::arg("plugin"), "Enables the specified plugin")
        .def("disable_plugin", &PluginLoader::enablePlugin, py::arg("plugin"), "Disables the specified plugin");

    py_class<PluginManager>(m, "PluginManager")
        .def("get_plugin", &PluginManager::getPlugin, py::arg("name"), py::return_value_policy::reference,
             "Checks if the given plugin is loaded and returns it when applicable.")
        .def_property_readonly("plugins", &PluginManager::getPlugins, "Gets a list of all currently loaded plugins")
        .def("is_plugin_enabled", py::overload_cast<const std::string &>(&PluginManager::isPluginEnabled, py::const_),
             py::arg("plugin"), "Checks if the given plugin is enabled or not")
        .def("is_plugin_enabled", py::overload_cast<Plugin *>(&PluginManager::isPluginEnabled, py::const_),
             py::arg("plugin"), "Checks if the given plugin is enabled or not")
        .def("load_plugins", &PluginManager::loadPlugins, py::arg("directory"),
             "Loads the plugin contained within the specified directory")
        .def("enable_plugin", &PluginManager::enablePlugin, py::arg("plugin"), "Enables the specified plugin")
        .def("enable_plugins", &PluginManager::enablePlugins, "Enable all the loaded plugins")
        .def("disable_plugin", &PluginManager::disablePlugin, py::arg("plugin"), "Disables the specified plugin")
        .def("disable_plugins", &PluginManager::disablePlugins, "Disables all the loaded plugins")
        .def("clear_plugins", &PluginManager::clearPlugins, "Disables and removes all plugins");
}

}  // namespace endstone::detail
