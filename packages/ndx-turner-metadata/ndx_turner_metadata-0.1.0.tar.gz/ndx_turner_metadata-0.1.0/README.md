# ndx-turner-metadata Extension for NWB

The NWB extension for storing Turner lab specific metadata.

Extends `pynwb.file.LabMetaData` to store the MPTP treatment status of the subject.


## Installation

```bash
pip install ndx_turner_metadata
```

## Usage

```python
from uuid import uuid4
from datetime import datetime
from dateutil.tz import tzlocal

from pynwb import NWBFile, NWBHDF5IO

from ndx_turner_metadata import TurnerLabMetaData

# Create NWBFile
nwbfile = NWBFile(
        session_description="session_description",
        identifier=str(uuid4()),
        session_start_time=datetime(1970, 1, 1, tzinfo=tzlocal()),
    )

# Create LabMetaData
lab_meta_data = TurnerLabMetaData(
    name="MPTPMetaData",
    MPTP_status="pre-MPTP",
)

# Add to NWBFile
nwbfile.add_lab_meta_data(lab_meta_data=lab_meta_data)

# Write LabMetaData to NWB file
nwbfile_path = "metadata.nwb"
with NWBHDF5IO(nwbfile_path, mode="w") as io:
    io.write(nwbfile)
            
# Check LabMetaData was added to the NWB file
with NWBHDF5IO(nwbfile_path, mode="r", load_namespaces=True) as io:
    read_nwbfile = io.read()
    read_nwbfile_lab_metadata = read_nwbfile.lab_meta_data["MPTPMetaData"]

```

---
This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
