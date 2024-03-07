# Copyright (c) 2016-2024 by Cisco Systems, Inc. All rights reserved.

import json
import re
from collections import OrderedDict
from jinja2 import Template
from abc import ABC, abstractmethod

from ysrestconf.restconf import DEFAULT_CONTENT_TYPES
from ysrestconf.ansible_helper import DictionaryToXML

ANSIBLE_TEMPLATE = """# Ansible will need some basic information to make sure
# it can connect to the target device before attempting
# sending a request using RESTCONF. Ansible will look
# in the same directory as the playbook file for ansible.cfg.
#
# Nearly all parameters in ansible.cfg can be overridden
# with ansible-playbook command line flags.
# Example of basic ansible.cfg file:
#
#[defaults]
#inventory = ./ansible_host.yaml
#
# Example of basic ansible_host.yaml file referred to in
# ansible.cfg inventory:
#
#[HOST_NAME_HERE]
#IP_ADDRESS_HERE
#
#[HOST_NAME_HERE:vars]
# ansible_connection: httpapi
# ansible_network_os: restconf
# ansible_httpapi_use_ssl: true
# ansible_httpapi_validate_certs: false
# ansible_httpapi_port: 443
# ansible_httpapi_restconf_root: /restconf/data/
# ansible_user: USERNAME_HERE
# ansible_password: PASSWORD_HERE
#
- name: {{ msg_name }}
  hosts: HOST_NAME_HERE
  gather_facts: no
  tasks:
    - name: {{ task_name }}
    {%- if method == 'get' %}
      ansible.netcommon.restconf_get:
      {%- if output %}
        # Output can either be json or xml
        output: {{ output }}
      {%- endif %}
    {%- else %}
      ansible.netcommon.restconf_config:
        method: {{ method }}
        {%- if format %}
        # Format can either be json or xml
        format: {{ format }}
        {%- endif %}
    {%- endif %}
        path: {{ path }}
        {% if content -%}
        content: |
          {{ content }}
        {%- endif -%}"""

OPENAPI_PATH_PARAMS_RE = re.compile(r'=\{.*\}')
CURLY_BRACES_CONTENT_RE = re.compile(r'{(.*?)}')


class Playbook(ABC):
    def __init__(
        self, filename, task_name, msg_name,
        xpath, method, openapi_doc, xpath_value='',
        content_type='', user_custom_content=''
    ):
        self.filename = f'{filename}.yaml'
        self.task_name = task_name
        self.msg_name = msg_name
        self.xpath = xpath
        self.xpath_value = xpath_value
        self.method = method.lower()
        self.openapi_doc = openapi_doc

        self.content_type = content_type
        self.user_custom_content = user_custom_content

    @staticmethod
    def remove_path_params(path) -> str:
        if '/' not in path and '=' not in path:
            return path

        tokens = path.split('/')
        # Preserve token before equal sign for all path tokens
        formatted_path = '/'.join([
            token.split('=')[0]
            if '=' in token else token
            for token in tokens
        ])
        # Trim empty spaces
        formatted_path = formatted_path.replace(' ', '')
        # Trim invalid chars
        formatted_path = formatted_path.replace('{', '')
        formatted_path = formatted_path.replace('}', '')

        return formatted_path

    @staticmethod
    def params_exists(path) -> bool:
        """
        Check for parameter existence in any given OpenAPI 3.0 path.

        Args:
            path (str): The path to check for parameter existence.

        Returns:
            bool: True if parameters exist in the path, False otherwise.
        """
        return re.search(OPENAPI_PATH_PARAMS_RE, path) is not None

    @staticmethod
    def get_params_map(path) -> dict:
        """
        Return a map of path elements and their corresponding parameter names.

        Args:
            path (str): The path to be processed.

        Returns:
            dict: A dictionary mapping path elements to their parameter names.
        """
        params_map = {}
        tokens = path.split('/')

        if not path or '/' not in path and '=' not in path:
            # No parameters in path
            return params_map

        for token in tokens:
            if '=' in token:
                param_tokens = token.split('=')
                param_ref = param_tokens[-1]
                param_ref = param_ref.replace('{', '')
                param_ref = param_ref.replace('}', '')
                params_map[param_tokens[0]] = param_ref

        return params_map

    @staticmethod
    def remove_path_namespaces(path) -> str:
        """
        Returns xpath with all namespaces removed

        Args:
            path (str): The xpath with namespaces

        Returns:
            str: The xpath with all namespaces removed
        """
        if not path or '/' not in path or ':' not in path:
            return path

        tokens = path.split('/')
        return '/'.join([
            token.split(':')[-1] if ':' in token else token for token in tokens
        ])

    def get_paths_dict_and_path(self) -> [dict, str]:
        """
        Returns the dict with all endpoints and the XPath's specific endpoint.

        Raises:
            KeyError: If URL or paths keys are nonexistent in OpenAPI document.
            ValueError: If unable to retrieve paths.
            ValueError: If XPath does not exist as a path in OpenAPI document.

        Returns:
            tuple[dict, str]: OpenAPI dict with all endpoints/paths,
                and XPath's OpenAPI path/endpoint.
        """

        paths_dict = {}
        # Most matched path in list of matched paths
        matched_path = None
        path = None

        try:
            paths_dict = self.openapi_doc['paths']
        except KeyError:
            raise KeyError(
                'URL or paths keys are nonexistent in OpenAPI document.'
            )

        if not paths_dict:
            raise ValueError('Unable to retrieve paths')

        # Match XPath to path
        for path in paths_dict:
            # Remove keys and namespaces from path for comparison
            formatted_path = path
            formatted_path = self.remove_path_namespaces(formatted_path)
            formatted_path = self.remove_path_params(formatted_path)

            xpath_tokens = [token.strip() for token in self.xpath.split('/')[1:]]
            formatted_tokens = [
                token.strip() for token in formatted_path.split('/')
            ]
            # Check for equality after splitting xpath and formatted path
            if xpath_tokens == formatted_tokens[
                len(formatted_tokens) - len(xpath_tokens):
            ]:
                matched_path = path

        if not matched_path:
            raise ValueError(
                'XPath does not exist as a path in OpenAPI document'
            )
        return (paths_dict, matched_path)

    def get_schema_from_path_obj(self, path_dict):
        schema_obj = None
        if path_dict.get('requestBody', None) \
          and self.content_type in path_dict['requestBody']['content']:  # noqa: E127
            # Request has a body, method is one of: PATCH, PUT, POST
            path_content = path_dict['requestBody']['content']
            path_json_obj = path_content[self.CONTENT_TYPE]
            schema_obj = path_json_obj['schema']

        if not schema_obj:
            raise ValueError('Schema object does not exist in OpenAPI document')
        return schema_obj

    def get_path_and_content(self) -> tuple:
        """
        Given an OpenAPI document, xpath, and method,
        return endpoint/path and content.

        Returns:
            tuple: A tuple containing the endpoint/path and content.
        """

        content = None
        paths_dict, matched_path = self.get_paths_dict_and_path()

        # Get path object from document using matched path, and gen. url & body
        path_dict = paths_dict.get(matched_path, None).get(self.method, None)
        if path_dict:
            # Path is the matched path without the first slash token (data)
            path = '/'.join(matched_path.split('/')[2:])
            # Convert path's OpenAPI-syntax schema to dict if it exists
            if path_dict.get('requestBody', None) \
               and self.content_type in path_dict['requestBody']['content']:
                # Request has a body, method is one of: PATCH, PUT, POST
                path_content = path_dict['requestBody']['content']
                path_json_obj = path_content[self.content_type]
                schema_obj = path_json_obj['schema']
                # Browse for request body schema obj in document
                schema = {}
                if schema_obj.get('$ref', None):
                    schema_ref = schema_obj['$ref']
                    schema_name = schema_ref.split('/')[-1]
                    schema = self.openapi_doc['components']['schemas'][schema_name]
                else:
                    schema = schema_obj
                # Parse schema to make body/content
                content = self.schema_to_dict(schema, self.xpath)
        else:
            raise ValueError('This REST method is not supported')

        return (path, content)

    def schema_to_dict(self, schema, xpath, data={}) -> dict:
        """
        Convert an OpenAPI schema to dict format, easier for translating.

        Args:
            schema (dict): The OpenAPI schema.
            xpath (str): The XPath expression.
            data (dict): The data dictionary.

        Returns:
            dict: The dict-converted schema data.
        """

        # Set of properties in dict that identify it will have children
        OPENAPI_PROPS = {'type', 'properties', 'items'}
        TYPES_TO_PROPS = {'object': 'properties', 'array': 'items'}
        child_type = 'object'
        tmp_dict = schema

        if isinstance(tmp_dict, OrderedDict):
            # Convert to dict from OrderedDict
            tmp_dict = json.loads(json.dumps(tmp_dict))

        if set(tmp_dict.keys()) & OPENAPI_PROPS:
            child_type = tmp_dict['type']
            tmp_dict = tmp_dict.get('properties', None)\
                or tmp_dict.get('items', None)
            if not tmp_dict:
                return data

        for key, value in tmp_dict.items():
            if isinstance(value, dict):
                value_keys = value.keys()
                if set(value_keys) & OPENAPI_PROPS and len(value_keys):
                    child_type = value['type']
                    value = value.get('properties', None)\
                        or value.get('items', None)
                    if not value and child_type not in TYPES_TO_PROPS.keys():
                        # Not nested anymore
                        data = {**data, key: self.xpath_value}
                    else:
                        if child_type == 'object':
                            data = {
                                **data,
                                key: self.schema_to_dict(value, xpath, data)
                            }
                        elif child_type == 'array':
                            datum = self.schema_to_dict(value, xpath, data)
                            data = {
                                **data,
                                key: [
                                    {datum_key: datum[datum_key]}
                                    for datum_key in datum.keys()
                                ]
                            }
        return data

    @abstractmethod
    def gen_playbook_content(self) -> tuple:
        """
        Generate the content of the playbook.

        This method should be implemented by subclasses to generate the actual content
        of the playbook based on the specific requirements.

        Returns:
            tuple[str, dict]: the playbook content and the parameters map.
        """
        pass


class XmlPlaybook(Playbook):
    def __init__(
        self, filename, task_name, msg_name, xpath, method, openapi_doc,
        xpath_value='', content_type=DEFAULT_CONTENT_TYPES['xml'],
        user_custom_content='',
    ):
        super().__init__(
            filename, task_name, msg_name, xpath, method, openapi_doc,
            xpath_value=xpath_value, content_type=content_type,
            user_custom_content=user_custom_content,
        )

    def gen_playbook_content(self) -> tuple:
        result = {}
        tplt = Template(ANSIBLE_TEMPLATE)
        path, content = self.get_path_and_content()
        # Additional parameters that user needs to fill out in front-end
        params_map = self.get_params_map(path)

        result = tplt.render({
            'path': path,
            'method': self.method,
            'content': DictionaryToXML(content).xml_str if self.method != 'get' else None,
            'task_name': self.task_name,
            'msg_name': self.msg_name,
            'output': 'xml',
            'format': 'xml',
        })
        return (result, params_map)


class JsonPlaybook(Playbook):
    def __init__(
        self, filename, task_name, msg_name, xpath, method, openapi_doc,
        xpath_value='', content_type=DEFAULT_CONTENT_TYPES['json'],
        user_custom_content='',
    ):
        super().__init__(
            filename, task_name, msg_name, xpath, method, openapi_doc,
            xpath_value=xpath_value, content_type=content_type,
            user_custom_content=user_custom_content,
        )

    def gen_playbook_content(self) -> tuple:
        """
        Generate the content of the playbook.

        Returns:
            tuple: A tuple containing the playbook content and parameters map.
        """
        result = {}
        tplt = Template(ANSIBLE_TEMPLATE)
        path, content = self.get_path_and_content()
        # Additional parameters that user needs to fill out in front-end
        params_map = self.get_params_map(path)

        result = tplt.render({
            'path': path,
            'method': self.method,
            'content': json.dumps(content) if content else None,
            'task_name': self.task_name,
            'msg_name': self.msg_name,
            'output': 'json',
            'format': 'json'
        })
        return (result, params_map)


class CustomContentPlaybook(Playbook):
    def __init__(
        self, filename, task_name, msg_name, xpath, method, openapi_doc,
        content_type='', user_custom_content='',
    ):
        super().__init__(
            filename, task_name, msg_name, xpath, method, openapi_doc,
            content_type=content_type, user_custom_content=user_custom_content,
        )

    def get_path(self) -> str:
        """
        Given an OpenAPI document, xpath, and method,
        return endpoint/path.

        Returns:
            tuple: A tuple containing the endpoint/path and content.
        """

        paths_dict, matched_path = self.get_paths_dict_and_path()

        # Get path object from document using matched path, and gen. url & body
        path_dict = paths_dict.get(matched_path, None).get(self.method, None)
        if path_dict:
            # Path is the matched path without the first slash token (data)
            path = '/'.join(matched_path.split('/')[2:])
        else:
            raise ValueError('This REST method is not supported')

        return path

    def gen_playbook_content(self) -> tuple:
        """
        Generate the content of the playbook.

        Returns:
            tuple: A tuple containing the playbook content and parameters map.
        """
        result = {}
        tplt = Template(ANSIBLE_TEMPLATE)
        path = self.get_path()
        # Additional parameters that user needs to fill out in front-end
        params_map = self.get_params_map(path)
        content = None

        if self.user_custom_content and self.method != 'get':
            content = self.user_custom_content

        result = tplt.render({
            'path': path,
            'method': self.method,
            'content': content,
            'task_name': self.task_name,
            'msg_name': self.msg_name,
            'output': None,
        })
        return (result, params_map)


def create_playbook(
    filename, task_name, msg_name, xpath, method,
    openapi_doc, xpath_value='', content_type='',
    user_custom_content='',
) -> Playbook:
    """
    Factory method to create a playbook object.

    Args:
        filename (str): The filename of the playbook.
        task_name (str): The name of the task.
        msg_name (str): The name of the message.
        xpath (str): The XPath expression.
        xpath_value (str): The value of the XPath expression.
        method (str): The HTTP method.
        openapi_doc (dict): The OpenAPI document.

    Returns:
        Playbook: A Playbook object.
    """
    if content_type == DEFAULT_CONTENT_TYPES['xml']:
        return XmlPlaybook(
            filename, task_name, msg_name, xpath, method,
            openapi_doc, xpath_value=xpath_value, content_type=content_type,
            user_custom_content=user_custom_content,
        )
    elif content_type == DEFAULT_CONTENT_TYPES['json']:
        return JsonPlaybook(
            filename, task_name, msg_name, xpath, method,
            openapi_doc, xpath_value=xpath_value, content_type=content_type,
            user_custom_content=user_custom_content,
        )
    else:
        return CustomContentPlaybook(
            filename, task_name, msg_name, xpath, method,
            openapi_doc, content_type=content_type,
            user_custom_content=user_custom_content,
        )
