# -*- coding: UTF-8 -*-

from .eval_py import PyEvaluated
from .eval_cheetah import CheetahEvaluated

PJCEvaluated = PyEvaluated | CheetahEvaluated
