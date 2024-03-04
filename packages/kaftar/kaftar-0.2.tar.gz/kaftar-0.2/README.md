# Kaftar SDK

## Usage

Package installation

``` bash
pip install kaftar
```

Usage:

``` python
import uuid
import time
from kaftar import Notification

message_uuid = uuid.uuid4()
group_uuid = uuid.uuid4()
broker_url = "BROKER_URL_HERE"

app = Notification('app_name', broker_url)
app.send_notification(
    {
        'subject': 'Notification title goes here',
        'content': 'Notification body goes here'
    },
    [
        {
            'receiver': "076f08cc-4122-400a-bffa-2a0157ba57eb",  # can be email or phone number
            'message_uuid': str(message_uuid),  # Optional (task will generate an id if not provided here)
            'uuid': "076f08cc-4122-400a-bffa-2a0157ba57eb"
        }
    ],
    int(time.time()),
    group_uuid=group_uuid # Optional
)
# Delete single notification
app.delete_notification(message_uuid)

# Delete group of notifications
app.delete_group_notification(group_uuid)
```
