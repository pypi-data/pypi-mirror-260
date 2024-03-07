#  Copyright (c) 2020 Robert Lieck
from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import URLError, HTTPError
import tarfile
import zipfile
import gzip, bz2, lzma
import shutil

import git

from . import config
from .corpora import FileCorpus, SingleFileCorpus, JSONFileCorpus, JSONLinesFileCorpus, CSVFileCorpus
from .util import __DOWNLOAD__, __ACCESS__, __LOADER__, __URL__, __FILE__, \
    CorpusNotFoundError, DownloadFailedError, LoadingFailedError


# dictionary with loader functions
loaders = {
    "FileCorpus": FileCorpus.init,
    "SingleFileCorpus": SingleFileCorpus,
    "JSONFileCorpus": JSONFileCorpus,
    "JSONLinesFileCorpus": JSONLinesFileCorpus,
    "CSVFileCorpus": CSVFileCorpus,
}

def populate_kwargs(corpus, kwargs_dict):
    if corpus is not None:
        return {**dict(config.corpus_params(corpus)), **kwargs_dict}
    else:
        return kwargs_dict.copy()


def remove(corpus, silent=False, not_exists_ok=False, not_dir_ok=False, **kwargs):
    # populate keyword arguments
    kwargs = populate_kwargs(corpus, kwargs)
    # get path to remove
    path = Path(kwargs[config.__PATH__])
    # check path
    if path.exists():
        if not path.is_dir() and not not_dir_ok:
            raise NotADirectoryError(f"Path {path} for corpus '{corpus}' is not a directory.")
    else:
        if not not_exists_ok:
            raise FileNotFoundError(f"Path {path} for corpus '{corpus}' does not exist.")
        else:
            return
    # get confirmation
    if not silent:
        while True:
            rm = input(f"Remove corpus '{corpus}' ({path}) [y/N]: ").strip().lower()
            if rm in ['y', 'yes']:
                rm = True
                break
            elif rm in ['', 'n', 'no']:
                rm = False
                break
    else:
        rm = True
    # remove
    if rm:
        shutil.rmtree(path)
    else:
        print(f"Canceled. Corpus '{corpus}' ({path}) not removed.")


def load(corpus=None, **kwargs):
    """
    Load a corpus.
    :param corpus: Name of the corpus to load or None to only use given keyword arguments.
    :param kwargs: Keyword arguments that are populated from config; specifying parameters as keyword arguments take
    precedence over the values from config.
    :return: output of loader
    """
    # populate keyword arguments from config
    populated_kwargs = populate_kwargs(corpus, kwargs)
    # check if corpus exists
    path = Path(populated_kwargs[config.__PATH__])
    if path.exists():
        if __LOADER__ in populated_kwargs:
            # extract loader from kwargs
            loader = populated_kwargs[__LOADER__]
            # if string was provided, lookup loader function
            if isinstance(loader, str):
                try:
                    loader = loaders[loader]
                except KeyError:
                    raise LoadingFailedError(f"Unknown {__LOADER__} '{loader}'.")
            # make sure loader is callable
            if not callable(loader):
                raise LoadingFailedError(f"{__LOADER__} '{loader}' is not callable.")
            # call loader
            return loader(**populated_kwargs)
        else:
            raise LoadingFailedError("No loader specified.")
    else:
        # if it does not exist, try downloading (if requested) and then retry
        if config.getbool(populated_kwargs.get(__DOWNLOAD__, False)):
            # download using original (unpopulated) kwargs
            download(corpus, **kwargs)
            # prevent second download attempt in reload
            kwargs[__DOWNLOAD__] = False
                        # reload
            return load(corpus, **kwargs)
        else:
            raise CorpusNotFoundError(f"Corpus '{corpus}' at path '{path}' does not exist "
                                      f"(specify {__DOWNLOAD__}=True to try downloading).")


def create_download_path(corpus, kwargs):
    path = Path(kwargs[config.__PATH__])
    if path.exists():
        # directory is not empty
        if path.is_file() or list(path.iterdir()):
            raise DownloadFailedError(f"Cannot download corpus '{corpus}': "
                                      f"target path {path} exists and is non-empty.")
    else:
        path.mkdir(parents=True)
    return path

__KNOWN_ACCESS_METHODS__ = [
    'git',
    'zip',
    'tar.gz',
    'file',
    'gz',
    'xz',
    'bz2',
]

def download(corpus, **kwargs):
    if corpus is not None and config.get(corpus, config.__PARENT__) is not None:
        # for sub-corpora delegate downloading to parent
        download(config.get(corpus, config.__PARENT__), **kwargs)
    else:
        # populate keyword arguments from config
        kwargs = populate_kwargs(corpus, kwargs)
        # get access method
        access = kwargs[__ACCESS__]
        # check if method is known
        if access in __KNOWN_ACCESS_METHODS__ or callable(access):
            path = create_download_path(corpus, kwargs)
        else:
            raise DownloadFailedError(f"Unknown access method '{access}'")

        # use known access method or provided callable
        try:
            if access == 'git':
                # clone directly into the target directory
                git.Repo.clone_from(url=kwargs[__URL__], to_path=path)
            elif access in ['zip', 'tar.gz', 'file', 'gz', 'xz', 'bz2']:
                # download to temporary file
                url = kwargs[__URL__]
                try:
                    # urlopen(url)
                    tmp_file_name, _ = urlretrieve(url=url) # TODO: urlretrieve may be deprecated
                except (HTTPError, URLError) as e:
                    raise DownloadFailedError(f"Opening url '{url}' failed: {e}")
                # open with custom method
                if access == 'tar.gz':
                    with tarfile.open(tmp_file_name, "r:gz") as tmp_file:
                        tmp_file.extractall(path)
                elif access == 'zip':
                    with zipfile.ZipFile(tmp_file_name) as tmp_file:
                        tmp_file.extractall(path)
                elif access == 'file':
                    target = path / kwargs[__FILE__]
                    shutil.copy(tmp_file_name, target)
                elif access == 'gz':
                    target = path / kwargs[__FILE__]
                    with gzip.open(tmp_file_name, 'rb') as f_in:
                        with open(target, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                elif access == 'xz':
                    target = path / kwargs[__FILE__]
                    with lzma.open(tmp_file_name, 'rb') as f_in:
                        with open(target, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                elif access == 'bz2':
                    target = path / kwargs[__FILE__]
                    with bz2.open(tmp_file_name, 'rb') as f_in:
                        with open(target, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
            elif callable(access):
                # access is a callable
                create_download_path(corpus, kwargs)
                return access(corpus, **kwargs)
        except:
            # clean up the target directory
            shutil.rmtree(path)
            raise
