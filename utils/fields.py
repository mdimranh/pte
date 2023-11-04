from django.db import models


class jsonField(models.JSONField):
    def __init__(
        self,
        *args,
        schema={},
        **kwargs,
    ):
        super().__init__(*args, **kwargs)