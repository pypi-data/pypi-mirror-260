# Dj Easy view CRUD mixins

Makes your CRUD's even more smaller and customizable with dj easy views . 

## Installation


```
pip install djeasyview
```

## Usage

### List and create

This mixin provides generic implementations for listing and creating resources.

#### Example:

```python
from djeasyview import DjeasyListCreateView
from your_app.models import YourModel
from your_app.serializers import YourModelSerializer
from rest_framework.permissions import IsAuthenticated

class YourView(DjeasyListCreateView):
    model = YourModel
    list_serializer_class = YourModelSerializer
    create_serializer_class = YourModelSerializer
    serializer_class = YourModelSerializer
    queryset = YourModel
    permission_classes = [IsAuthenticated]
```




### Retrive , Update , Delete

This mixin provides generic implementations for Retrive , updating and deleting resources.


```python
from djeasyview import DjeasyRetrieveUpdateApiView
from your_app.models import YourModel
from your_app.serializers import YourModelSerializer
from rest_framework.permissions import IsAuthenticated

class YourView(DjeasyRetrieveUpdateApiView):
    model = YourModel
    list_serializer_class = YourModelSerializer
    create_serializer_class = YourModelSerializer
    serializer_class = YourModelSerializer
    queryset = YourModel
    permission_classes = [IsAuthenticated]
```