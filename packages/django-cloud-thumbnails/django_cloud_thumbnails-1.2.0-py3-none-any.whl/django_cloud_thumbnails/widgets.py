import logging

from django import forms
from django.apps import apps
from django.contrib.admin.widgets import AdminFileWidget, ForeignKeyRawIdWidget
from django.db.models import ObjectDoesNotExist

from .config import settings
from .utils import get_backend

logger = logging.getLogger(__name__)


def thumbnail_url(image_path):
    thumbnail_options = {
        'detail': True,
        'upscale': True,
        'size': settings.IMAGE_CROPPING_THUMB_SIZE,
    }
    return get_backend().get_thumbnail_url(image_path, thumbnail_options)


def get_attrs(image, name):
    try:
        try:
            if image.closed:
                image.open()
            image.seek(0)
        except:
            pass

        try:
            width, height = get_backend().get_size(image)
        except AttributeError:
            width = image.width
            height = image.height
        return {
            'class': 'crop-thumb',
            'data-thumbnail-url': thumbnail_url(image),
            'data-field-name': name,
            'data-org-width': width,
            'data-org-height': height,
            'data-max-width': width,
            'data-max-height': height,
        }
    except (ValueError, AttributeError, IOError):
        return {}


class CropWidget:
    def _media(self):
        js = [
            'image_cropping/js/dist/image_cropping.min.js',
        ]

        if settings.IMAGE_CROPPING_JQUERY_URL:
            js.insert(0, settings.IMAGE_CROPPING_JQUERY_URL)
        css = {
            'all': [
                'image_cropping/css/jquery.Jcrop.min.css',
                'image_cropping/css/image_cropping.css',
            ]
        }

        return forms.Media(css=css, js=js)

    media = property(_media)


class ImageCropWidget(AdminFileWidget, CropWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update(get_attrs(value, name))
        render_args = [name, value, attrs]
        if renderer:
            render_args.append(renderer)
        return super().render(*render_args)


class HiddenImageCropWidget(ImageCropWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}
        attrs['data-hide-field'] = True
        render_args = [name, value, attrs]
        if renderer:
            render_args.append(renderer)
        return super().render(*render_args)


class CropForeignKeyWidget(ForeignKeyRawIdWidget, CropWidget):
    def __init__(self, *args, **kwargs):
        self.field_name = kwargs.pop('field_name')
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        if value:
            rel_to = self.rel.model
            app_name = rel_to._meta.app_label
            model_name = rel_to._meta.object_name.lower()
            try:
                image = getattr(
                    apps.get_model(app_name, model_name).objects.get(pk=value),
                    self.field_name,
                )
                if image:
                    attrs.update(get_attrs(image, name))
            except (ObjectDoesNotExist, LookupError):
                logger.error(
                    "Can't find object: %s.%s with primary key %s "
                    "for cropping." % (app_name, model_name, value)
                )
            except AttributeError:
                logger.error(
                    "Object %s.%s doesn't have an attribute named '%s'."
                    % (app_name, model_name, self.field_name)
                )

        render_args = [name, value, attrs]
        if renderer:
            render_args.append(renderer)
        return super().render(*render_args)
