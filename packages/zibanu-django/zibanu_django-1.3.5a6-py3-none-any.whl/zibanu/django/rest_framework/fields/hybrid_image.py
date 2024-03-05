# -*- coding: utf-8 -*-
import base64
import io
import logging
import mimetypes
from typing import Any

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         12/08/23 17:11
# Project:      Zibanu - Django
# Module Name:  hybrid_image
# Description:
# ****************************************************************
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from drf_extra_fields.fields import HybridImageField as SourceHybridImageField
from drf_extra_fields.fields import Base64FieldMixin, ImageField


class HybridImageField(SourceHybridImageField):
    """
    Inherited class from drf_extra_fields.field.HybridImageField to allow size validation and implement the use image
    format and size validation
    """
    INVALID_FILE_SIZE = _("The width or height of the file is invalid.")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        HybridImageField class constructor

        Parameters
        ----------
        *args: Tuple with parameters values
        **kwargs: Parameter dictionary with key/values
        """
        self.max_image_width = kwargs.pop("image_width", 0)
        self.max_image_height = kwargs.pop("image_height", 0)
        super().__init__(*args, **kwargs)

    def to_representation(self, file):
        if self.represent_in_base64:
            if not file:
                return ""

            try:
                with file.open() as f:
                    prepend_info = "data:%s;base64" % mimetypes.guess_type(file.path)[0]
                    base64_data = base64.b64encode(f.read()).decode()
                    return "%s,%s" % (prepend_info, base64_data)
            except Exception as exc:
                logging.critical(str(exc))
                raise OSError(_("Error encoding image file"))
        else:
            return super().to_representation(file)

    def to_internal_value(self, data):
        """
        Override method to process internal data from serializer

        Parameters
        ----------
        data: Data received from serializer (raw post data)

        Returns
        -------
        Python data compatible
        """

        if self.represent_in_base64:
            if self.max_image_width > 0 and self.max_image_height > 0:
                width, height = self.__get_file_size(data)
                if width > self.max_image_width or height > self.max_image_height:
                    raise ValidationError(self.INVALID_FILE_SIZE)
            image_field = Base64FieldMixin.to_internal_value(self, data)
        else:
            image_field = ImageField.to_internal_value(self, data)
        return image_field

    def __get_file_size(self, data: str) -> tuple:
        """
        Get the file size from base64 encoded bytes

        Parameters
        ----------
        data: Base64 encoded bytes

        Returns
        -------
        width, height: Tuple with width and height values
        """
        try:
            from PIL import Image
            base64_data = base64.b64decode(data)
            image = Image.open(io.BytesIO(base64_data))
        except (ImportError, OSError):
            raise ValidationError(self.INVALID_FILE_MESSAGE)
        else:
            width, height = image.size
        return width, height
