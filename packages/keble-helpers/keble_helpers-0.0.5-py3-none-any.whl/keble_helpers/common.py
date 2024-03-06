import uuid
import string
import random
from pydantic import BaseModel
from typing import List, Any
from pathlib import Path
from datetime import date, datetime
import ctypes
import os
import zipfile
import hashlib
import shutil
from types import GeneratorType


def id_generator() -> str:
    return str(uuid.uuid4())


def generate_random_string(length: int = 32, *, lower: bool = True, upper: bool = True, digit: bool = True) -> str:
    candidates = []
    if lower: candidates += string.ascii_lowercase
    if upper: candidates += string.ascii_uppercase
    if digit: candidates += string.digits
    assert len(candidates) > 0, 'Invalid random string generator, missing candidates.'
    return ''.join(random.choice(candidates) for i in range(length))


def is_pydantic_field_empty(obj: BaseModel, field: str) -> bool:
    return not hasattr(obj, field) or getattr(obj, field) is None


def date_to_datetime(d: date) -> datetime:
    if isinstance(d, date):
        return datetime.combine(d, datetime.min.time())
    return d


def datetime_to_date(d: datetime) -> date:
    if isinstance(d, datetime):
        return d.date()
    return d


# _hashu = lambda word: ctypes.c_uint64(hash(word)).value


def hash_string(arg: str) -> str:
    hash_object = hashlib.md5(arg.encode())
    return hash_object.hexdigest()

    # return str(hash(args))
    # return _hashu("".join(args)).to_bytes(8, "big").hex()


def slice_to_list(items: List[Any], slice_size: int) -> List[List[Any]]:
    slices: List[List[date]] = []
    current_slice: List[date] = []
    for _d in items:
        current_slice.append(_d)
        if len(current_slice) >= slice_size:
            slices.append(current_slice)
            current_slice = []
    if len(current_slice) > 0:
        slices.append(current_slice)
    return slices


def bad_utf8_str_encoding(str_: str) -> str:
    return repr(str_)[1:-1]


def get_first_match(items: list, key_fn, value):
    """Return first match item in a list"""
    filtered = list(filter(lambda x: key_fn(x) == value, items))
    if len(filtered) >= 1:
        return filtered[0]
    # return None for not found
    return None


def ensure_has_folder(path: str) -> str:
    exist = os.path.exists(path)
    if not exist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    return path


def zip_dir(folder: Path | str, zip_filepath: Path | str):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    # Convert to Path object
    dir = Path(folder)

    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(dir))

def remove_dir(dir: Path | str):
    shutil.rmtree(dir, ignore_errors=True)


def wait_generator_stop(generator: GeneratorType, *, max_generate: int = 1000):
    generated = []
    attempts = 0
    while True:
        try:
            next_item = next(generator)
            generated.append(next_item)
        except StopIteration:
            break
        attempts += 1
        if attempts > max_generate:
            raise ValueError(f"Generator exceeded max generate allowance {max_generate}")