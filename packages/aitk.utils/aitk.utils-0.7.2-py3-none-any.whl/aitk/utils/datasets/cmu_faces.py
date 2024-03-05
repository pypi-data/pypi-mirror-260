# -*- coding: utf-8 -*-
# ***********************************************************
# aitk.utils: Python AI utils
#
# Copyright (c) 2020 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.utils
#
# ***********************************************************

import os
import numpy as np
import glob
from PIL import Image

from .utils import get_file, Dataset

_filename = get_file(
    "dogs-vs-cats.tar.gz",
    "https://raw.githubusercontent.com/ArtificialIntelligenceToolkit/datasets/master/cmu_faces/cmu_faces_full_size.npz",
    extract=True,
)

DATA_FILE = _filename

def get():
    """
    """
    np_data = np.load(DATA_FILE, allow_pickle=True)

    labels = np_data["labels"]

    return Dataset(
        train_inputs=np_data["data"].tolist(),
        train_features=[labels.split("_") for labels in labels.tolist()]
    ) # 624, 120, 128

