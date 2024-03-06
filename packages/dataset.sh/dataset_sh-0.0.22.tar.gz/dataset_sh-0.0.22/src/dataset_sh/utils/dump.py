from dataset_sh import create
from dataset_sh.utils.files import checksum
from dataset_sh.utils.misc import get_tqdm


def dump_single_collection(fn, name, data, silent=False):
    with create(fn) as out:
        out.add_collection(name, data, data[0].__class__, tqdm=get_tqdm(silent=silent))
    return checksum(fn)


def dump_collections(fn, data_dict, silent=False):
    tqdm = get_tqdm(silent=silent)
    with create(fn) as out:
        for name, data in tqdm(data_dict.items()):
            if len(data) > 0:
                out.add_collection(name, data, data[0].__class__)
    return checksum(fn)
