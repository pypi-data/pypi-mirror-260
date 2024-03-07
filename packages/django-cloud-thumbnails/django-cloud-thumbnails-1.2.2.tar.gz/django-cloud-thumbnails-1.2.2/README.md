# Django Cloud Thumbnails


Django Cloud Thumbnails is a fork of
[django-image-cropping](https://github.com/jonasundderwolf/django-image-cropping) that uses
[django-cloud-storage](https://github.com/sysproxy/django-cloud-storage), a custom Django storage backend. 

## Installation

* Install this package using pip
```bash
pip install django-cloud-thumbnails
```

*  Add **django_cloud_thumbnails** to your **INSTALLED_APPS** setting like this
```python
INSTALLED_APPS = [
    ...,
    "django_cloud_thumbnails",
]
```