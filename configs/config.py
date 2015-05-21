# -*- coding: utf-8 -*-

"""
    config.py
    ~~~~~~~~~

    This module is the middle man for handling/consolidating
    configurations for Eugene's project.

    :copyright: (c) 2012 by Eugene
    :license: see LICENSE for more details.
"""

import ConfigParser
import os
import types

path = os.path.dirname(os.path.realpath(__file__))
_op = os.path.join(__file__, '..', '..','data')
_lp = os.path.join(__file__, '..', '..','logs')
DEFAULT_LOGPATH = os.path.abspath(_lp)
DEFAULT_OUTPATH = os.path.abspath(_op)


def argparser():
    parser = argparse.ArgumentParser(description="nap_score")
    parser.add_argument('--out', help="output filepath", default=DEFAULT_OUTPATH)
    parser.add_argument('--log', help="log path", default=DEFAULT_LOGPATH)
    return parser

def getdef(self, section, option, default_value):
    """This is a function which provides an alternative to
    config.get("fieldname", "key") -- since config.get does not
    fallback to default values and will cause the program to break

    getdef is injected into the config module s.t. it can be called as
    config.get in the line:

    >>> config.getdef = types.MethodType(getdef, config)

    example config:
        [creds]
        password = foo

    usage:
        >>> password = config.getdef('creds', 'password', '******')
        >>> # if 'creds' is not a valid fieldname or 
        >>> # 'password' is not a valid key ...
        >>> print password 
        ******
        >>> # Let's say we're using the example config above:
        >>> print password
        foo
    """
    try:
        return self.get(section, option)
    except:
        return default_value

config = ConfigParser.ConfigParser()
config.read('%s/config.cfg' % path)
config.getdef = types.MethodType(getdef, config)

pathDIR = {'pathDIR': config.getdef('paths', 'pathDIR', '')
        }

connStr = {'s4_production': 'dbname=dd73gbh7ndvoju port=5432 user=u7cdkcoqc8c665 host=ec2-174-129-13-49.compute-1.amazonaws.com password=p5g77jc7aoe30beurd8s6l03ogk',
            'connect_db': 'dbname=prospective port=5432 user=arvind host=ec2-54-205-157-146.compute-1.amazonaws.com password=Talent2012'
    }


