import tempfile
from dataclasses import dataclass, field

from pydantic import BaseModel

from dataset_sh.clients import LocalStorage
from dataset_sh.utils.dump import dump_collections
import os


class NameAndAge(BaseModel):
    name: str
    age: int


class AgeAndAddr(BaseModel):
    age: int
    addr: str


@dataclass
class DatasetVersions:
    versions: list[str] = field(default_factory=list)


@dataclass
class DatasetAndVersions:
    dataset: dict[str, DatasetVersions] = field(default_factory=dict)


TEST_USERNAME = 'test-user'
TEST_USERNAME_ANOTHER = 'test-another-user'


def create_test_datasets(location, count=10) -> DatasetAndVersions:
    lc = LocalStorage(location)
    ds = DatasetAndVersions()
    with tempfile.TemporaryDirectory() as scratch_folder:
        dataset_name = f'ad'
        fn = os.path.join(scratch_folder, 'tmp')

        vid = dump_collections(
            fn,
            {
                "seq": [
                    NameAndAge(name=f"ad-{i}", age=i) for i in range(15)
                ],
                "seq2": [

                ],
            }
            ,
            silent=True
        )

        lc.dataset(to_dataset_name(TEST_USERNAME_ANOTHER, dataset_name)).import_file(
            fn,
            verify_version=vid
        )

        for i in range(count):
            versions = []
            dataset_name = f'd{i}'
            for j in range(i):
                name = f'd-{i}-v-{j}'
                fn = os.path.join(scratch_folder, name)
                vid = dump_collections(
                    fn,
                    {
                        "seq": [
                            NameAndAge(name=f"d{i}", age=j)
                        ],
                    }
                    ,
                    silent=True
                )
                versions.append(vid)
                lc.dataset(to_dataset_name(TEST_USERNAME, dataset_name)).import_file(
                    fn,
                    verify_version=vid
                )

            ds.dataset[dataset_name] = DatasetVersions(versions=versions)

            if len(versions) > 5:
                lc.dataset(to_dataset_name(TEST_USERNAME, dataset_name)).set_tag(
                    't1',
                    versions[-3]
                )
    return ds


def to_dataset_name(namespace, dataset_name):
    return f"{namespace}/{dataset_name}"
