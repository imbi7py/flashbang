"""
Script to extract chk profiles en-masse using multithreading

Usage:
    python extract_profiles <model> <run>
"""
import sys
import multiprocessing as mp
import time

# flashbang
from flashbang import simulation, load_save, tools


def main(model, run, model_set, multithread=True, reload=False, save=True,
         config='default'):
    """
    Parameters
    ----------
    model : str
    run : str
    model_set : str
    multithread : bool
    reload : bool
    save : bool
    config : str
    """
    t0 = time.time()

    multithread = tools.str_to_bool(multithread)
    reload = tools.str_to_bool(reload)
    save = tools.str_to_bool(save)

    chk_list = load_save.find_chk(model=model, run=run, model_set=model_set)
    conf = load_save.load_config(name=config)

    params = conf['profiles']['params'] + conf['profiles']['isotopes']
    derived_params = conf['profiles']['derived_params']

    if multithread:
        args = []
        for chk in chk_list:
            args.append((chk, model, run, model_set, reload, save, params, derived_params))

        with mp.Pool(processes=4) as pool:
            pool.starmap(extract_profiles, args)
    else:
        for chk in chk_list:
            extract_profiles(chk, model=model, run=run,
                             model_set=model_set, reload=reload, save=save,
                             params=params, derived_params=derived_params)

    t1 = time.time()
    print(f'Time taken: {t1-t0:.2f} s')


def extract_profiles(chk, model, run, model_set, reload, save, params, derived_params):
    """Function for multithread pool
    """
    load_save.get_profile(chk, model=model, run=run,
                          model_set=model_set, reload=reload,
                          save=save, params=params,
                          derived_params=derived_params)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Parameters:'
              + '\n1. model'
              + '\n2. run'
              + '\n3. model_set'
              )
        sys.exit(0)
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3],
             **dict(arg.split('=') for arg in sys.argv[3:]))
