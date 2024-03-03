"""
Test suite for Validator
"""
from music_checker_micro.music_checker import MusicChecker as MC
from music_manager_micro.music_manager import MusicManager as MM
from src.music_validator_micro.music_validator import MusicValidator as MV


def test_get_all_mbid():
    """
    Test of getting distinct mbid
    """
    library = "###TESTINGMVMBID###"
    library_dir = "./tests/mbid_samples"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'TXXX:MusicBrainz Artist Id'])
    mv.execute()
    mbids = mv.get_all_artist_mbid()
    assert mbids[0] == '1234-5678-9012'
    assert mbids[1] == '1234-5678-9013'


def test_validator():
    """
    Full test of the music checker stack
    """

    library = "###TESTINGMV###"
    library_dir = "./tests/sample_mp3"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'ABC'])
    output = mv.execute()
    assert len(output.items()) == 3
    assert output['ABC'][0] == './tests/sample_mp3/sample.mp3'
    output = mv.get_list()
    assert len(output.items()) == 3
    assert output['ABC'][0] == './tests/sample_mp3/sample.mp3'


def test_multiple_validator():
    """
    Test of the validator with a directory containing more than
    one media file
    """

    library = "###TESTINGMVM###"
    library_dir = "./tests/multi_sample"
    mm = MM(library, library_dir)
    mm.reset_library()
    mm.execute()
    mc = MC(library)
    mc.execute()
    mv = MV(library, tag_list=['TALB', 'TIT2', 'ABC'])
    output = mv.execute()
    assert len(output.items()) == 3
    assert len(output['ABC']) == 2
    assert './tests/multi_sample/2.mp3' in output['ABC']
    output = mv.get_list()
    assert len(output.items()) == 3
    assert len(output['ABC']) == 2
    assert './tests/multi_sample/2.mp3' in output['ABC']
