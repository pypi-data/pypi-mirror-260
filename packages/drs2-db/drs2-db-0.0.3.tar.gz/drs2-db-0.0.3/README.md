# drs2-db

Module for drs2 db calls  
This a wrapper for drs2 sql calls that:
- retrieves object ids. `get_object_ids(file_ids)`
- updates the DRS_OBJECT_UPDATE_STATUS table. `update_object_ids()`
- retrieves descriptor paths `get_descriptor_path(object_id)`
- checks to see if an object is in the update queue. `check_object_in_update_queue(object_id)`

## Using the module
```
import drs2db
from dotenv import load_dotenv
from drs2.drsdb import DrsDB
from drs2 import configure_logger

load_dotenv()
configure_logger()
logger = logging.getLogger('drs2_judaica_update')

drs_db = DrsDB()
object_id = "12345678"
if drs_db.check_object_in_update_queue(object_id):
    logger.error(f"Object id {object_id} is in update queue")
else:
    logger.info(f"Object id {object_id} is NOT in update queue")

ocfl_path, storage_class = drs_db.get_descriptor_path(object_id)
logger.info(f"{ocfl_path}, {storage_class}")
```

## Dependencies
- Required modules are listed in `requirements.txt`.
  