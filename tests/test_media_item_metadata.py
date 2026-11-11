"""Tests for MediaItemMetadata."""

from music_assistant_models.media_items.metadata import MediaItemMetadata


def test_last_musicbrainz_lookup_defaults_to_none() -> None:
    """A metadata blob written before the field existed reads back as never looked up."""
    assert MediaItemMetadata.from_dict({}).last_musicbrainz_lookup is None


def test_update_always_overwrites_last_musicbrainz_lookup() -> None:
    """A newer lookup timestamp replaces the stored one, like last_refresh does."""
    metadata = MediaItemMetadata(last_musicbrainz_lookup=100)
    metadata.update(MediaItemMetadata(last_musicbrainz_lookup=200))
    assert metadata.last_musicbrainz_lookup == 200


def test_update_keeps_the_earliest_original_year() -> None:
    """The first release of an album is the earliest year any source gives."""
    metadata = MediaItemMetadata(original_year=1975)

    metadata.update(MediaItemMetadata(original_year=1973))
    assert metadata.original_year == 1973

    metadata.update(MediaItemMetadata(original_year=1980))
    assert metadata.original_year == 1973

    empty = MediaItemMetadata()
    empty.update(MediaItemMetadata(original_year=1990))
    assert empty.original_year == 1990
