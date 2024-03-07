from ndx_turner_metadata import TurnerLabMetaData
from pynwb import NWBHDF5IO

file_path = "/Volumes/LaCie/CN_GCP/Turner/nwbfiles_public/stub_Isis_I_160818_3.nwb"

with NWBHDF5IO(file_path, mode="r+", load_namespaces=True) as io:
    nwbfile = io.read()

    # Create a LabMetaDataExtension object
    lab_meta_data = TurnerLabMetaData(
        name="MPTPMetaData",
        MPTP_status="pre-MPTP",
    )

    nwbfile.add_lab_meta_data(lab_meta_data)
    io.write(nwbfile)
