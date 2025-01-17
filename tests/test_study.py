import io
from zipfile import ZipFile

import pytest

from pyorthanc import Orthanc, Study, util
from .data import a_study
from .setup_server import clear_data, setup_data, ORTHANC_1


@pytest.fixture
def study():
    setup_data(ORTHANC_1)

    client = Orthanc(ORTHANC_1.url, ORTHANC_1.username, ORTHANC_1.password)
    yield Study(client=client, study_id=a_study.IDENTIFIER)

    clear_data(ORTHANC_1)


def test_attributes(study):
    study.build_series()

    assert study.get_main_information().keys() == a_study.INFORMATION.keys()

    assert study.identifier == a_study.IDENTIFIER
    assert study.study_id == a_study.ID
    assert study.uid == a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    assert study.referring_physician_name == a_study.REFERRING_PHYSICIAN_NAME
    assert study.date == a_study.DATE
    assert study.patient_identifier == a_study.PARENT_PATIENT_IDENTIFIER
    assert study.patient_information.keys() == a_study.PATIENT_MAIN_INFORMATION.keys()
    assert study.series != []


def test_remote_empty_series(study):
    study.build_series()

    for series in study.series:
        series._instances = []

    study.remove_empty_series()
    assert study.series == []


def test_zip(study):
    result = study.get_zip()

    assert type(result) == bytes
    zip = ZipFile(io.BytesIO(result))
    assert zip.testzip() is None  # Verify that zip files are valid (if it is, returns None)


def test_anonymize(study):
    study.build_series()

    anonymized_study = study.anonymize(remove=['StudyDate'])
    anonymized_study.build_series()
    assert anonymized_study.uid != a_study.INFORMATION['MainDicomTags']['StudyInstanceUID']
    with pytest.raises(KeyError):
        anonymized_study.date

    anonymized_study = study.anonymize(replace={'StudyDate': '20220101'})
    anonymized_study.build_series()
    assert study.date == a_study.DATE
    assert anonymized_study.date == util.make_datetime_from_dicom_date('20220101')

    anonymized_study = study.anonymize(keep=['StudyDate'])
    anonymized_study.build_series()
    assert study.date == a_study.DATE
    assert anonymized_study.date == a_study.DATE
