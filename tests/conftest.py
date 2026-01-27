from pathlib import Path
import zipfile

import pytest


@pytest.fixture
def create_zip(tmp_path):
    """Factory fixture to create test ZIP files with specified contents."""

    def _create_zip(files: dict[str, str], name: str = "test.zip") -> Path:
        """Create a ZIP file with the given files.

        Args:
            files: Dict mapping filename to content
            name: Name of the ZIP file to create

        Returns:
            Path to the created ZIP file
        """
        zip_path = tmp_path / name
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for filename, content in files.items():
                zf.writestr(filename, content)
        return zip_path

    return _create_zip
