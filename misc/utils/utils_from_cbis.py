# CBIS general utilities

import json
import yaml


#  From cbis_manager project cbis_deploy_helper.py
class CbisHelper:

    @staticmethod
    def get_file_string(file_path):
        with open(file_path, 'r') as myfile:
            content = myfile.read()
            return content

    @staticmethod
    def get_dict_from_file(file_path):
        dict_from_file = None
        with open(file_path, 'r') as stream:
            if file_path.endswith('yaml') or file_path.endswith('yml'):
                dict_from_file = yaml.load(stream)
            if file_path.endswith('json'):
                dict_from_file = json.load(stream)
        return dict_from_file

    @staticmethod
    def write_dict_to_file(file_path, file_data, json_encoder=None):
        with open(file_path, 'w') as outfile:
            if file_path.endswith('yaml') or file_path.endswith('yml'):
                yaml.dump(file_data, outfile, default_flow_style=False,
                          Dumper=ExplicitDumper)
            if file_path.endswith('json'):
                if json_encoder:
                    _str = json.dumps(file_data, indent=4, cls=json_encoder)
                else:
                    _str = json.dumps(file_data, indent=4)
                outfile.write(_str)
        outfile.close()

    @staticmethod
    def write_to_file(file_path, file_data):
        with open(file_path, 'w') as outfile:
            outfile.write(file_data)
        outfile.close()

    @staticmethod
    def write_value_to_yaml(file_path, key, value):
        with open(file_path) as outfile:
            dictionary = yaml.load(outfile)
        if dictionary:
            dictionary[key] = value
        else:
            dictionary = {key: value}

        with open(file_path, 'w') as outfile:
            yaml.dump(dictionary, outfile, default_flow_style=False)

    @staticmethod
    def extract_key_values_from_nested_dict(my_dict, res):
        """
        Warning: recursion ahead! do not change, move or look at directly

        :param my_dict: dict
            a dictionary that requires flattening
        :param res: dict
            the flat dictionary of key values
        :return: no return value
        """
        for key, value in my_dict.iteritems():
            if isinstance(value, dict):
                CbisHelper.extract_key_values_from_nested_dict(value, res)
            else:
                tmp_key = key.split(':')
                if len(tmp_key) > 1 and not tmp_key[0].endswith('CBIS'):
                    tmp_key.pop(0)
                    new_key = ':'.join(tmp_key)
                else:
                    new_key = key
                res[new_key] = value

class ExplicitDumper(yaml.SafeDumper):
    """
    A dumper that will never emit aliases.
    """

    def ignore_aliases(self, data):
        return True


if __name__ == '__main__':
    pass
