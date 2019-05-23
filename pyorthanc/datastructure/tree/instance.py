# coding: utf-8
# author: gabriel couture
from typing import Dict, Any

from pyorthanc.orthanc import Orthanc


class Instance:
    """Represent an instance that is in an Orthanc server

    This object has many getters that allow the user to retrieve metadata
    or the entire DICOM file of the Instance
    """

    def __init__(self, instance_identifier: str, orthanc: Orthanc) -> None:
        """Constructor

        Parameters
        ----------
        instance_identifier
            Orthanc instance identifier.
        orthanc
            Orthanc object.
        """
        self.orthanc: Orthanc = orthanc

        self.instance_identifier: str = instance_identifier

    def get_instance_dicom_file(self) -> bytes:
        """Retrieves DICOM file

        This method retrieves bytes corresponding to DICOM file.

        Returns
        -------
        bytes
            Bytes corresponding to DICOM file

        Examples
        --------
        >>> instance = Instance('instance identifier',
        ...                     Orthanc('http://localhost:8080'))
        >>> dicom_file_bytes = instance.get_instance_dicom_file('instance_identifier')
        >>> with open('your_path', 'wb') as file_handler:
        ...     file_handler.write(dicom_file_bytes)
        """
        return self.orthanc.get_instance_file(self.instance_identifier).json()

    def get_identifier(self) -> str:
        """Get instance identifier

        Returns
        -------
        str
            Instance identifier
        """
        return self.instance_identifier

    def get_main_information(self) -> Dict:
        """Get instance information

        Returns
        -------
        Dict
            Dictionary with tags as key and information as value
        """
        return self.orthanc.get_instance_information(self.instance_identifier).json()

    def get_content(self) -> Any:
        """Get content

        Returns
        -------
        Any
            Content corresponding.
        """
        return self.orthanc.get_instance_content(self.instance_identifier).json()

    def get_tags(self) -> Dict:
        """Get tags

        Returns
        -------
        Dict
            Tags in the form of a dictionary.
        """
        return self.orthanc.get_instance_tags(self.instance_identifier).json()

    def get_simplified_tags(self) -> Dict:
        """Get simplified tags

        Returns
        -------
        Dict
            Simplified tags in the form of a dictionary.
        """
        return self.orthanc.get_instance_simplified_tags(
            self.instance_identifier).json()

    def get_content_by_tag(self, tag: str) -> Any:
        """Get content by tag

        Parameters
        ----------
        tag
            Tag like '0040-a730'.

        Returns
        -------
        Any
            Content corresponding to specified tag.
        """
        return self.orthanc.get_instance_content_by_group_element(
            instance_identifier=self.instance_identifier,
            group_element=tag).json()

    def get_content_by_group_element(self, group_element: str) -> Any:
        """Get content by group element like '0040-a730/1/0040-a730'

        Parameters
        ----------
        group_element
            Group element like '0040-a730/1/0040-a730'.

        Returns
        -------
        Any
            Content corresponding to specified tag.
        """
        return self.orthanc.get_instance_content_by_group_element(
            instance_identifier=self.instance_identifier,
            group_element=group_element).json()

    def __str__(self):
        return f'Instance (identifier={self.get_identifier()})'
