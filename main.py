import re
import os
import shutil
import json
from itertools import chain


class QtProParser:
    def __init__(self, filepath, var=None, cfg=None):
        """

        :param filepath: filepath of *.pro or *.pri
        :param var: dictionary of local variables which must be replaced by values
        :param cfg: dictionary of configure variables
        """
        self.filepath = filepath
        self.variable = var
        self.config = cfg
        self.data = None

    def read_all(self):
        """
            Read all data from qmake project file
        :return:
        """
        with open(self.filepath, 'r') as filepath:
            self.data = filepath.read()
            self.data = QtProParser.replace_multiline_data(self.data)
            self.data = QtProParser.replace_variables(self.data, self.variable)

    def get_sources(self):
        """
            Parse qmake project file and return list of filepaths specified in HEADERS and SOURCES variables.
            Get sources only from main scope and 'contains(:cond){}' blocks.
        :return: list of filepaths specified in HEADERS and SOURCES variables of .pri or .pro qmake file
        """
        s = self.data.strip()
        st = True

        sources = []
        while st:
            st = False
            index = 0
            v = ''
            for m in QtProParser.parse_block(s):
                if QtProParser.check_contains(m[0]):
                    for n in QtProParser.parse_contains(m[0]):
                        if QtProParser.check_binary(n[3], n[4], n[2].find('!') == -1, self.config):
                            sources.append([k[2] for k in QtProParser.parse_sources(n[5])])
                            sources.append([k[2] for k in QtProParser.parse_headers(n[5])])

                v += s[index:m.start()]
                index = m.end()
                st = True
            s = v + s[index:]

        sources.append([k[2] for k in QtProParser.parse_sources(s)])
        sources.append([k[2] for k in QtProParser.parse_headers(s)])

        sources = list(chain(*sources))
        return ' '.join(sources).split(' ')

    def copy_sources(self, input_path, output_path):
        """
            Copy files specified in HEADERS and SOURCES variables of .pri or .pro qmake file
            from input_path to output_path
        :param input_path: string value of input path
        :param output_path: string value of output path
        :return:
        """
        try:
            shutil.rmtree(output_path)
        except Exception:
            pass

        sources = self.get_sources()
        for s in sources:
            ins = os.path.join(input_path, s)
            outs = os.path.join(output_path, s)
            dir = os.path.dirname(outs) + '/'
            if os.path.exists(ins) and os.path.isfile(ins):
                try:
                    os.makedirs(dir)
                except Exception:
                    pass
                shutil.copy(ins, outs)

    def replace_multiline_data(lines):
        """
            Replace all '\' by ' '
        :return: text without '\'
        """
        s = lines.strip()
        return re.sub(r'\s*\\\s*', ' ', s)

    def replace_variables(line, variable):
        """
            Replace all keys of variable by values
        :param variable: dictionary of variable names and values
        :return:
        """
        s = line.strip()
        for i, v in variable.items():
            s = s.replace(i, v)
        return s

    def parse_block(lines):
        """
            Parse block: value { text }
        :return: iterator
        """
        return re.finditer(r'(^([^\n]*)\s*\{\s*([^{}]*)\s*\})', lines, re.MULTILINE)

    def parse_contains(lines):
        """
            Parse block: contains(key, val) { text }
        :return: iterator
        """
        return re.finditer(r'(^([!]?)contains\(\s*([\w]*)\s*,\s*([\w]*)\s*\)\s*\{\s*([^{}]*)\s*\})', lines,
                           re.MULTILINE)

    def parse_sources(line):
        """
            Parse line SOURCES +=
        :return: iterator
        """
        return re.finditer(r'(SOURCES\s*[\+\*]{1}=\s([^\n]*))', line)

    def parse_headers(line):
        """
            Parse line HEADERS +=
        :return: iterator
        """
        return re.finditer(r'(HEADERS\s*[\+\*]{1}=\s([^\n]*))', line)

    def check_contains(line):
        return line.find('contains') != -1

    def check_unary(tag, config, flag):
        for i, v in config.items():
            if i.find(tag) != -1:
                return True if flag else False
        return False if flag else True

    def check_binary(tag, value, flag, config):
        for i, v in config.items():
            if i.find(tag) != -1 and \
                    v.find(value) != -1:
                return True if flag else False
        return False if flag else True


if __name__ == '__main__':
    with open("config.json", "r") as read_file:
        data = json.load(read_file)

    in_path = data['in_path']
    out_path = data['out_path']
    fp = in_path + data['pro']
    vars = data['vars']
    config = data['cfg']

    p = QtProParser(fp, vars, config)
    p.read_all()
    p.copy_sources(in_path, out_path)

    exit(0)
