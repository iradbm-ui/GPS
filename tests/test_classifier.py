from gps_presence.classifier import Presence, PresenceClassifier


def test_classifies_signed_distances() -> None:
    classifier = PresenceClassifier(boundary_margin=0.2)

    assert classifier.classify(2.0, -4.0) is Presence.IN_A
    assert classifier.classify(-3.0, 1.5) is Presence.IN_B
    assert classifier.classify(-1.0, -0.5) is Presence.OUTSIDE


def test_margin_prevents_boundary_flicker() -> None:
    classifier = PresenceClassifier(boundary_margin=0.5)

    assert classifier.classify(0.4, -2.0) is Presence.OUTSIDE
    assert classifier.classify(0.51, -2.0) is Presence.IN_A
    assert classifier.classify(0.1, -2.0) is Presence.OUTSIDE


def test_disjoint_regions_are_required() -> None:
    classifier = PresenceClassifier(boundary_margin=0.0)

    try:
        classifier.classify(1.0, 1.0)
    except ValueError as error:
        assert "disjoint" in str(error)
    else:
        raise AssertionError("Overlapping positive distances should be rejected")
