# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2024. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2024. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         28/02/24 15:27
# Project:      Zibanu - Django
# Module Name:  object_to_list
# Description:
# ****************************************************************
# Default imports
from typing import Any


def object_to_list(obj: Any) -> list:
    l_return = []
    if isinstance(obj, str):
        l_return.append(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):
                l_return = l_return + object_to_list(value)
            elif isinstance(value, list):
                for value_detail in value:
                    l_return.append(key + ": " + str(value_detail))
            elif isinstance(value, str):
                l_return.append(key + ": " + value)
    elif isinstance(obj, list):
        l_return = obj.copy()
    else:
        l_return.append(str(obj))

    return l_return
