import pybilt.bilayer_analyzer.bilayer_analyzer as ba
import pybilt.com_trajectory.COMTraj as comtraj
import MDAnalysis as mda
import numpy as np
import timeit


def test_run_analysis_mp():
    analyzer = ba.BilayerAnalyzer(structure='../pybilt/sample_bilayer/sample_bilayer.psf',
                                  trajectory='../pybilt/sample_bilayer/sample_bilayer_10frames.dcd',
                                  selection="resname POPC DOPE TLCL2")

    analyzer.add_analysis('nnf nnf_a resname_1 DOPE resname_2 POPC leaflet upper n_neighbors 6')
    analyzer.set_frame_range(interval=2)
    analyzer.print_analysis_protocol()

    #run serial version first
    analyzer.run_analysis()
    msd_1_dat_s = analyzer.get_analysis_data('msd_1')
    nnf_a_dat_s = analyzer.get_analysis_data('nnf_a')

    #run multiprocessing version
    analyzer.reset()
    analyzer.run_analysis_mp(nprocs=2)

    msd_1_dat_mp = analyzer.get_analysis_data('msd_1')
    nnf_a_dat_mp = analyzer.get_analysis_data('nnf_a')

    print "msd serial:"
    print(msd_1_dat_s)
    print "msd_mp:"
    print(msd_1_dat_mp)
    print("nnf serial:")
    print(nnf_a_dat_s)
    print("nnf mp:")
    print(nnf_a_dat_mp)

def run_serial(analyzer):
    #make sure a fresh run
    analyzer.reset()
    analyzer.run_analysis()
    return

def run_parallel(analyzer, nprocs=2):
    #make sure a fresh run
    analyzer.reset()
    analyzer.run_analysis_mp(nprocs=nprocs)
    return

def test_parallel_performance():
    setup = """\
import pybilt.bilayer_analyzer.bilayer_analyzer as ba
from __main__ import run_serial, run_parallel
analyzer = ba.BilayerAnalyzer(structure='../pybilt/sample_bilayer/sample_bilayer.psf',
                              trajectory='../pybilt/sample_bilayer/sample_bilayer_10frames.dcd',
                              selection="resname POPC DOPE TLCL2")

analyzer.add_analysis('nnf nnf_a resname_1 DOPE resname_2 POPC leaflet upper n_neighbors 6')
analyzer.add_analysis('nnf nnf_b resname_1 POPC resname_2 POPC leaflet upper n_neighbors 10')
analyzer.add_analysis('bilayer_thickness bt')
analyzer.set_frame_range(interval=2)
"""
    print("timing the serial execution (10 repetitions):")
    time_s = timeit.timeit('run_serial(analyzer)', setup=setup, number=10)

    print("timing the parallel execution (10 repetitions):")
    time_p = timeit.timeit('run_parallel(analyzer)', setup=setup, number=10)
    print("average serial execution time: {}".format(time_s/10.0))
    print("average parallel execution time: {}".format(time_p/10.0))


if __name__ == '__main__':
    test_run_analysis_mp()
    test_parallel_performance()
