import pytest

from fese import tags
from fese.exceptions import LanguageNotFound


@pytest.mark.parametrize("string", ["00:46:34.125000000", "01:32:0"])
def test_safe_td(string):
    assert tags._safe_td(string) is not None


@pytest.mark.parametrize(
    "tags_dict", [{"language": "eng"}, {"language": "spa", "title": "latin"}]
)
def test_generic_tags(tags_dict):
    assert tags.FFprobeGenericSubtitleTags(tags_dict)


@pytest.mark.parametrize(
    "tags_dict",
    [
        {"language": "eng"},
        {
            "creation_time": "2018-02-16T18:29:09.000000Z",
            "language": "eng",
            "handler_name": "SoundHandler",
        },
    ],
)
def test_mp4_tags(tags_dict):
    assert tags.FFprobeMp4SubtitleTags(tags_dict)


@pytest.mark.parametrize(
    "tags_dict",
    [
        {
            "language": "swe",
            "BPS-eng": "28",
            "DURATION-eng": "01:31:19.587000000",
            "NUMBER_OF_FRAMES-eng": "545",
            "NUMBER_OF_BYTES-eng": "19218",
            "_STATISTICS_WRITING_APP-eng": "mkvmerge v32.0.0 ('Astral Progressions') 64-bit",
            "_STATISTICS_WRITING_DATE_UTC-eng": "2019-03-29 20:13:32",
            "_STATISTICS_TAGS-eng": "BPS DURATION NUMBER_OF_FRAMES NUMBER_OF_BYTES",
        },
        {"language": "eng"},
    ],
)
def test_mkv_tags(tags_dict):
    assert tags.FFprobeMp4SubtitleTags(tags_dict)


def test_wo_language():
    with pytest.raises(LanguageNotFound):
        assert tags.FFprobeGenericSubtitleTags({"language": "Unknown"})


def test_language_converter_exception():
    with pytest.raises(LanguageNotFound):
        assert tags.FFprobeGenericSubtitleTags({"language": "fil"})


def test_wo_language_w_language_fallback():
    tags.LANGUAGE_FALLBACK = "en"

    tags_ = tags.FFprobeGenericSubtitleTags({"language": "Unknown"})
    assert tags_.language.alpha3 == "eng"

    tags.LANGUAGE_FALLBACK = None


def test_wo_language_w_language_fallback_invalid():
    tags.LANGUAGE_FALLBACK = "Unknown"

    with pytest.raises(ValueError):
        assert tags.FFprobeGenericSubtitleTags({"language": "Unknown"})

    tags.LANGUAGE_FALLBACK = None


def test_w_alpha2_language():
    tags_ = tags.FFprobeGenericSubtitleTags({"language": "en"})
    assert tags_.language.alpha3 == "eng"


def test_w_alpha2_language_extra():
    tags_ = tags.FFprobeGenericSubtitleTags({"language": "zh-Hans"})
    assert tags_.language.alpha3 == "zho"


@pytest.mark.parametrize(
    "content,alpha3,expected_country",
    [
        ("brazil", "por", "BR"),
        ("latino", "spa", "MX"),
        ("braSil", "por", "BR"),
        ("mExico", "spa", "MX"),
    ],
)
def test_w_custom_language(content, alpha3, expected_country):
    tags_obj = tags.FFprobeGenericSubtitleTags({"title": content, "language": alpha3})
    assert tags_obj.language.country == expected_country


@pytest.mark.parametrize(
    "data,expexted_cls",
    [
        ({"BPS-eng": 123, "language": "eng"}, tags.FFprobeMkvSubtitleTags),
        ({"creation_time": "123", "language": "eng"}, tags.FFprobeMp4SubtitleTags),
        ({"language": "eng"}, tags.FFprobeGenericSubtitleTags),
    ],
)
def test_detect_cls_from_data(data, expexted_cls):
    assert isinstance(
        tags.FFprobeGenericSubtitleTags.detect_cls_from_data(data), expexted_cls
    )
