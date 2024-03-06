# -*- coding: utf-8 -*-

# Copyright 2020-2024 Jean-Baptiste Delisle
# Licensed under the EUPL-1.2 or later

import numpy as np
from setuptools import Extension, setup

setup(
  ext_modules=[
    Extension(
      'bindensity.libbindensity',
      sources=['src/bindensity/pywrapbindensity.c', 'src/bindensity/libbindensity.c'],
      language='c',
    )
  ],
  include_dirs=[np.get_include()],
)
