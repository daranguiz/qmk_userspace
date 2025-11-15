"""
File system writer utility

Handles writing generated files to disk
"""

from pathlib import Path
from typing import Dict
import shutil


class FileSystemWriter:
    """Utility for writing generated files to disk"""

    @staticmethod
    def write_file(file_path: Path, content: str) -> None:
        """
        Write content to a file

        Args:
            file_path: Path to the file
            content: Content to write
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    @staticmethod
    def ensure_directory(dir_path: Path) -> None:
        """
        Ensure a directory exists

        Args:
            dir_path: Path to the directory
        """
        dir_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clean_directory(dir_path: Path) -> None:
        """
        Remove a directory and all its contents

        Args:
            dir_path: Path to the directory to clean
        """
        if dir_path.exists():
            shutil.rmtree(dir_path)

    @staticmethod
    def write_all(output_dir: Path, files: Dict[str, str]) -> None:
        """
        Write multiple files to a directory

        Cleans the output directory first to ensure no stale files remain.

        Args:
            output_dir: Output directory path
            files: Dictionary of {filename: content}
        """
        # Clean output directory first to remove any stale generated files
        FileSystemWriter.clean_directory(output_dir)
        FileSystemWriter.ensure_directory(output_dir)

        for filename, content in files.items():
            file_path = output_dir / filename
            FileSystemWriter.write_file(file_path, content)
