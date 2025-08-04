"""Tests for data models."""

from statutory_duty_extractor.models import StatutoryDuty, StatutoryInstrument


def test_statutory_duty_creation() -> None:
    """Test creating a StatutoryDuty instance."""
    duty = StatutoryDuty(
        duty_description="Must conduct safety assessments",
        duty_holder="accountable person",
        legislative_reference="regulation 3(1)",
    )

    assert duty.duty_description == "Must conduct safety assessments"
    assert duty.duty_holder == "accountable person"
    assert duty.legislative_reference == "regulation 3(1)"


def test_statutory_instrument_creation() -> None:
    """Test creating a StatutoryInstrument instance."""
    instrument = StatutoryInstrument(
        document_title="Test Regulations 2024", document_reference="SI 2024/123"
    )

    assert instrument.document_title == "Test Regulations 2024"
    assert instrument.document_reference == "SI 2024/123"
    assert len(instrument.duties) == 0


def test_statutory_instrument_with_duties() -> None:
    """Test StatutoryInstrument with duties."""
    duty = StatutoryDuty(
        duty_description="Must conduct safety assessments",
        duty_holder="accountable person",
        legislative_reference="regulation 3(1)",
    )

    instrument = StatutoryInstrument(
        document_title="Test Regulations 2024",
        document_reference="SI 2024/123",
        duties=[duty],
    )

    assert len(instrument.duties) == 1
    assert instrument.duties[0].duty_description == "Must conduct safety assessments"
