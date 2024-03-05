import io
from typing import Optional
import urllib.request
from rdkit import Chem
from rdkit import RDLogger
from tqdm.auto import tqdm
import zipfile

from .datasets import GeneratedDataset


class BindingDB(GeneratedDataset):
    """BindingDB

    A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein considered to be drug-targets with small, drug-like molecules.
    """

    SOURCE = "https://www.bindingdb.org/bind/downloads/BindingDB_All_3D_202402_sdf.zip"
    COLLECTION = "bindingdb"

    float_fields = {
        "Ki (nM)",
        "IC50 (nM)",
        "Kd (nM)",
        "EC50 (nM)",
        "kon (M-1-s-1)",
        "koff (s-1)",
    }

    def __init__(self, fd: Optional[io.BytesIO] = None):
        """
        Initializes a BindingDB instance.

        Args:
            fd (Optional[io.BytesIO]): The file-like object containing the dataset content.
                If `fd` is not provided, the dataset content will be fetched from the default source.
        """
        if fd is not None:
            self.fd = fd

    @staticmethod
    def _convert_to_numeric(prop_name: str, value: str):
        """
        Converts a property value to numeric type.

        Args:
            prop_name (str): The name of the property.
            value (str): The value of the property.

        Returns:
            The converted numeric value, or None if conversion fails.
        """
        if prop_name in BindingDB.float_fields:
            try:
                return float(value)
            except ValueError:
                return None
        else:
            try:
                float_value = float(value)
                if float_value.is_integer():
                    return int(float_value)
                else:
                    return float_value
            except ValueError:
                return value

    @staticmethod
    def from_url(url: str) -> "BindingDB":
        """
        Creates a BindingDB instance from a URL containing a compressed SDF file (typically upstream).

        Args:
            url (str): The URL of the dataset.

        Returns:
            A BindingDB instance.
        """
        with urllib.request.urlopen(url) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                sdf_name = z.namelist()[0]
                with z.open(sdf_name) as sdf_file:
                    sdf_content = io.BytesIO(sdf_file.read())
        return BindingDB(sdf_content)

    @staticmethod
    def from_compressed_file(file_path: str) -> "BindingDB":
        """
        Creates a BindingDB instance from a compressed SDF file.

        Args:
            file_path (str): The path to the compressed file.

        Returns:
            A BindingDB instance.
        """
        with zipfile.ZipFile(file_path) as z:
            sdf_name = z.namelist()[0]
            with z.open(sdf_name) as sdf_file:
                sdf_content = io.BytesIO(sdf_file.read())
        return BindingDB(sdf_content)

    @staticmethod
    def from_uncompressed_file(file_path: str) -> "BindingDB":
        """
        Creates a BindingDB instance from an uncompressed SDF file.

        Args:
            file_path (str): The path to the uncompressed file.

        Returns:
            A BindingDB instance.
        """
        with open(file_path, "rb") as f:
            file_content = io.BytesIO(f.read())
        return BindingDB(file_content)

    def to_generator(self, progress_bar: bool = True):
        """
        Converts the dataset to a generator.

        Args:
            progress_bar (bool): Whether to display a progress bar.

        Yields:
            dict: A dictionary representing a record in the dataset.
        """
        RDLogger.DisableLog("rdApp.*")  # Suppress RDKit warnings and errors

        cached_sdf = self.get_cache_path().parent / "BindingDB.sdf.zip"

        if cached_sdf.exists():
            self.fd = self.from_compressed_file(cached_sdf)

        if self.fd is None:
            self.fd = self.from_url(self.SOURCE)

        sd = Chem.ForwardSDMolSupplier(self.fd, sanitize=False, removeHs=False)

        if progress_bar:
            pb = tqdm
        else:

            def pb(x, **kwargs):
                return x

        for mol in pb(sd, desc="Parsing BindingDB", unit=" molecule"):
            if mol is not None:
                record = {
                    prop: self._convert_to_numeric(prop, mol.GetProp(prop))
                    for prop in mol.GetPropNames()
                    if mol.HasProp(prop)
                }

                # Normalize PubChem SID and CID fields that are sometimes present in the SDF
                if "PubChem SID" in record:
                    record["PubChem SID of Ligand"] = record.pop("PubChem SID")
                if "PubChem CID" in record:
                    record["PubChem CID of Ligand"] = record.pop("PubChem CID")

                record["SMILES"] = Chem.MolToSmiles(mol)
                yield record

        # Re-enable logging
        RDLogger.EnableLog("rdApp.error")
        RDLogger.EnableLog("rdApp.warning")
