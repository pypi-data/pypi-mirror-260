#!python

from radtools._osfix import _winwait
from radtools.score.make_template import create_parser, manager

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    manager(**vars(args))
    _winwait()
