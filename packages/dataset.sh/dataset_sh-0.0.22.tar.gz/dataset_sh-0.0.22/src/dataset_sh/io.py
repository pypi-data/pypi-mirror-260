import json
import os
import warnings
import zipfile
from typing import Optional, Type, TypeVar, List

from pydantic import BaseModel

from .models import DatasetFileInternalPath
from .typing.codegen import CodeGenerator
from .typing.schema_builder import SchemaBuilder
from .utils.misc import id_function
from .core import CollectionConfig, DatasetFileMeta
from .utils.sample import reservoir_sampling

DataModel = TypeVar('DataModel', bound=BaseModel)


class DatasetFile:

    def __init__(self):
        raise ValueError('Please use DatasetFile.open(filename, mode)')

    @staticmethod
    def open(fp: str, mode: str = 'r'):
        """
        Open a dataset file
        :param fp: path to the file
        :param mode: r for read and w for write.
        :return:
        """
        if mode == 'r':
            return DatasetFileReader(fp)
        elif mode == 'w':
            return DatasetFileWriter(fp)
        else:
            raise ValueError('mode must be one of "r" or "w"')

    @staticmethod
    def binary_file_path(fn: str):
        return os.path.join(DatasetFileInternalPath.BINARY_FOLDER, fn)


class DatasetFileWriter:
    def __init__(self, file_path: str, compression=zipfile.ZIP_LZMA, compresslevel=9):
        """
        Write to a dataset file, this object can also be used as a context manager.

        This object need to be closed.

        :param file_path: location of the dataset file to write.
        :param compression: compress mode for zip file.
        :param compresslevel: note that the default compression algorithm ZIP_LZMA do not use this value.

        """
        self.zip_file = zipfile.ZipFile(file_path, 'w', compression=compression, compresslevel=compresslevel)
        self.meta = DatasetFileMeta()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        close the writer.
        :return:
        """
        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'w') as out:
            out.write(self.meta.model_dump_json().encode('utf-8'))
        self.zip_file.close()

    def add_collection(
            self,
            collection_name: str,
            data: List,
            model: Optional[Type[DataModel]] = None,
            tqdm=id_function,
    ):
        """
        add a data collection to this dataset.
        :param collection_name: name of the collection to add.
        :param data: list of objects that extends pydantic BaseModel.
        :param model: the pydantic model class.
        :param tqdm: Optional tqdm progress bar.
        :return:
        """
        for coll in self.meta.collections:
            if coll.name == collection_name:
                raise ValueError(f'collection {collection_name} already exists')

        if model is None:
            if isinstance(data[0], BaseModel):
                warnings.warn(f'model class is not provided, using {data[0].__class__.__name__} as model')
                model = data[0].__class__
            else:
                raise ValueError('Input data must be pydantic model')

        dataset_schema = SchemaBuilder.build(model)

        new_coll = CollectionConfig(
            name=collection_name,
            data_schema=dataset_schema,
        )

        self.meta.collections.append(new_coll)
        target_fp = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(target_fp, 'w') as out:
            for item in tqdm(data):
                out.write(item.model_dump_json(round_trip=True).encode('utf-8'))
                out.write("\n".encode('utf-8'))

    def add_binary_file(self, fn: str, content: bytes):
        """
        Add a binary file to the dataset
        :param fn: name of the binary file.
        :param content: content in bytes.
        :return:
        """
        binary_file_path = DatasetFile.binary_file_path(fn)
        with self.zip_file.open(binary_file_path, 'w') as out:
            out.write(content)


class DatasetFileReader:
    def __init__(self, file_path):
        """
        Read a dataset, this object can be used as a context manager.

        This object must be closed.

        :param file_path:
        """
        self.zip_file = zipfile.ZipFile(file_path, 'r')

        with self.zip_file.open(DatasetFileInternalPath.META_FILE_NAME, 'r') as fd:
            self.meta = DatasetFileMeta(**json.load(fd))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.zip_file.close()

    def binary_files(self):
        """
        Open a binary file for read.
        :return: a file descriptor for the binary file to read.
        """
        prefix = DatasetFileInternalPath.BINARY_FOLDER + '/'
        for name in self.zip_file.namelist():
            if name.startswith(prefix):
                yield name[len(prefix):]

    def open_binary_file(self, filename):
        """
        Open a binary file for read.
        :param filename: name of the binary file.
        :return: a file descriptor for the binary file to read.
        """
        return self.zip_file.open(
            DatasetFile.binary_file_path(filename),
            'r'
        )

    def collection(self, collection_name, model=None):
        """
        Open a collection.
        :param collection_name: name of a collection
        :param model: an optional pydantic model class to hold the data.
        :return: a CollectionReader object for the given collection name.
        """
        cfg = [c for c in self.meta.collections if c.name == collection_name]
        if len(cfg) == 0:
            raise ValueError(f"Collection {collection_name} do not exist")
        else:
            cfg = cfg[0]
        return CollectionReader(self.zip_file, collection_name, cfg, model=model)

    def coll(self, collection_name, model=None):
        return self.collection(collection_name, model=model)

    def collections(self):
        """
        List all collection names
        :return: list of collection names.
        """
        return [c.name for c in self.meta.collections]

    def __getitem__(self, item):
        return self.collection(item)


class CollectionReader(object):
    def __init__(self, zip_file, collection_name, config: CollectionConfig, model=None):
        """
        Collection Reader
        :param zip_file:
        :param collection_name:
        :param config:
        :param model:
        """
        self.zip_file = zip_file
        self.collection_name = collection_name
        self.config = config
        self.model = model

    def code_usage(self):
        generator = CodeGenerator()
        code = generator.generate_all(self.config.data_schema)
        return code

    def top(self, n=10):
        ret = []
        for i, row in enumerate(self):
            if i >= n:
                break
            ret.append(row)
        return ret

    def random_sample(self, n=10):
        return reservoir_sampling(self, n)

    def __iter__(self):
        """
        Iterate through the collection.
        :return:
        """
        entry = os.path.join(
            DatasetFileInternalPath.COLLECTION_FOLDER,
            self.collection_name,
            DatasetFileInternalPath.DATA_FILE
        )
        with self.zip_file.open(entry, 'r') as fd:
            for line in fd:
                line = line.strip()
                if len(line) > 0:
                    item = json.loads(line)
                    if self.model is None:
                        yield item
                    else:
                        yield self.model(**item)

    def to_list(self):
        """
        Read the collection as list instead of iterator
        :return:
        """
        return list(self)


# Standard IO operations


def open_dataset_file(fp: str) -> 'DatasetFileReader':
    """
    Read a dataset file
    :param fp: path to the file
    :return:
    """
    return DatasetFileReader(fp)


def create(fp: str, compression=zipfile.ZIP_LZMA, compresslevel=9) -> 'DatasetFileWriter':
    """
    Create a dataset file to write
    :param fp: path to the file
    :param compression: compress mode for zip file.
    :param compresslevel: note that the default compression algorithm ZIP_LZMA do not use this value.
    :return:
    """
    return DatasetFileWriter(fp, compression=compression, compresslevel=compresslevel)
