"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import yaml

from programy.config.file.file import BaseConfigurationFile
from programy.config.programy import ProgramyConfiguration

class YamlConfigurationFile(BaseConfigurationFile):

    def __init__(self):
        BaseConfigurationFile.__init__(self)
        self.yaml_data = None

    def load_from_text(self, text, client_configuration, bot_root):
        self.yaml_data = yaml.load(text)
        if self.yaml_data is None:
            raise Exception("Yaml data is missing")
        configuration = ProgramyConfiguration(client_configuration)
        configuration.load_config_data(self, bot_root)
        return configuration

    def load_from_file(self, filename, client_configuration, bot_root):
        configuration = ProgramyConfiguration(client_configuration)
        with open(filename, 'r+', encoding="utf-8") as yml_data_file:
            self.yaml_data = yaml.load(yml_data_file)
            configuration.load_config_data(self, bot_root)
        return configuration

    def get_section(self, section_name, parent_section=None):
        if parent_section is None:
            if section_name in self.yaml_data:
                return self.yaml_data[section_name]
        else:
            if section_name in parent_section:
                return parent_section[section_name]
        return None

    def get_keys(self, section):
        return section.keys()

    def get_child_section_keys(self, child_section_name, parent_section):
        if child_section_name in parent_section:
            return parent_section[child_section_name].keys()
        return None

    def get_option(self, section, option_name, missing_value=None):
        if option_name in section:
            return section[option_name]
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Missing value for [%s] in config, return default value %s", option_name, missing_value)
            return missing_value

    def get_bool_option(self, section, option_name, missing_value=False):
        if option_name in section:
            return section[option_name]
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Missing value for [%s] in config, return default value %s", option_name, missing_value)
            return missing_value

    def get_int_option(self, section, option_name, missing_value=0):
        if option_name in section:
            return section[option_name]
        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Missing value for [%s] in config, return default value %d", option_name, missing_value)
            return missing_value

    def get_multi_option(self, section, option_name, missing_value=None):

        if missing_value is None:
            missing_value = []

        if option_name in section:
            values = section[option_name]
            splits = values.split('\n')
            multis = []
            for value in splits:
                if value is not None and value != '':
                    multis.append(value)
            return multis

        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Missing value for [%s] in config, return default value", option_name)
            return missing_value

    def get_multi_file_option(self, section, option_name, bot_root, missing_value=None):

        if missing_value is None:
            missing_value = []

        if option_name in section:
            values = section[option_name]
            splits = values.split('\n')
            multis = []
            for value in splits:
                if value is not None and value != '':
                    multis.append(value.replace('$BOT_ROOT', bot_root))
            return multis

        else:
            if logging.getLogger().isEnabledFor(logging.WARNING):
                logging.warning("Missing value for [%s] in config, return default value", option_name)
            return missing_value
