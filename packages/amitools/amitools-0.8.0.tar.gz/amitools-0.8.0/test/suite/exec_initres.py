import os


def exec_initres_libnix_test(vamos, buildlibnix):
    lib_file = buildlibnix.make_lib("testnix")
    lib_name = os.path.basename(lib_file)
    lib_dir = os.path.basename(os.path.dirname(lib_file))
    name = "bin:" + lib_dir + "/" + lib_name
    vamos.run_prog_checked("exec_initres", name)


def exec_initres_libsc_test(vamos, buildlibsc):
    lib_file = buildlibsc.make_lib("testsc")
    lib_name = os.path.basename(lib_file)
    lib_dir = os.path.basename(os.path.dirname(lib_file))
    name = "bin:" + lib_dir + "/" + lib_name
    vamos.run_prog_checked("exec_initres", name)
