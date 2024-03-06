# Django Cloud Storage


Django Cloud Storage is a Python package that provides a custom storage backend designed for seamless integration with 
proprietary cloud storage service.

## Installation

```bash
pip install django-cloud-storage
```

## Configuration

In your Django settings file, set the following values:

```python
CLOUD_STORAGE_URL = 'https://your-cloud-service.com'
CLOUD_STORAGE_API_TOKEN = 'your-api-token'
CLOUD_STORAGE_PROJECT_ALIAS = 'myproject'
```

## Usage
To integrate the Cloud Storage with a Django model, follow these steps:

* Import the required models and CloudStorage:
    ```python
    from django_cloud_storage.storage import CloudStorage
    ```
* Define your Django model, using `CloudStorage` as the storage backend for a `FileField`:

    ```python
    class MyModel(models.Model):
        file_field = models.FileField(storage=CloudStorage)

        def __str__(self):
            return self.file_field.name
    ```