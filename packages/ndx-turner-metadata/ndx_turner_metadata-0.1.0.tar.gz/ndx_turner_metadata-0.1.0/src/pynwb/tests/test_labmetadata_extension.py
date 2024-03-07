from pynwb import NWBHDF5IO, NWBFile
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing import TestCase, remove_test_file, NWBH5IOFlexMixin

from ndx_turner_metadata import TurnerLabMetaData


class TestLabMetaDataExtensionConstructor(TestCase):
    """Simple unit test for creating a LabMetaDataExtension."""

    def setUp(self):
        """Set up an NWB file."""
        self.nwbfile = mock_NWBFile()
        self.lab_meta_data_name = "MPTPMetaData"

    def test_constructor(self):
        """Test that the constructor for LabMetaDataExtension sets values as expected."""

        # Create a LabMetaDataExtension object
        lab_meta_data = TurnerLabMetaData(
            name=self.lab_meta_data_name,
            MPTP_status="pre-MPTP",
        )

        # Test that the object has the expected values
        self.assertEqual(lab_meta_data.name, self.lab_meta_data_name)
        self.assertEqual(lab_meta_data.MPTP_status, "pre-MPTP")

class TestLabMetaDataExtensionSimpleRoundtrip(TestCase):
    """Simple roundtrip test for LabMetaDataExtension."""

    def setUp(self):
        self.nwbfile = mock_NWBFile()
        self.path = "test.nwb"
        self.lab_meta_data_name = "MPTPMetaData"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        """
        Add a LabMetaDataExtension to an NWBFile, write it to file, read the file, and test that
        the LabMetaDataExtension from the file matches the original LabMetaDataExtension.
        """

        # Create a LabMetaDataExtension object
        lab_meta_data = TurnerLabMetaData(
            name=self.lab_meta_data_name,
            MPTP_status="pre-MPTP",
        )

        self.nwbfile.add_lab_meta_data(lab_meta_data)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(lab_meta_data, read_nwbfile.lab_meta_data[self.lab_meta_data_name])


class TestLabMetaDataExtensionRoundtripPyNWB(NWBH5IOFlexMixin, TestCase):
    """Complex, more complete roundtrip test for LabMetaDataExtension using pynwb.testing infrastructure."""

    def getContainerType(self):
        return "TurnerLabMetaData"

    def addContainer(self):
        # Create a LabMetaDataExtension object
        lab_meta_data = TurnerLabMetaData(
            name="MPTPMetaData",
            MPTP_status="pre-MPTP",
        )

        self.nwbfile.add_lab_meta_data(lab_meta_data)

    def getContainer(self, nwbfile: NWBFile):
        return nwbfile.lab_meta_data["MPTPMetaData"]
