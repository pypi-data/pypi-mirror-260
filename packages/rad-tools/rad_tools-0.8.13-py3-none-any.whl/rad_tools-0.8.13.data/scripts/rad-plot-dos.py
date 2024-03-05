#!python

from radtools._osfix import _winwait
from radtools.score.plot_dos import create_parser, manager

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    manager(**vars(args))
    _winwait()
