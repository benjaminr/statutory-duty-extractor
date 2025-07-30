"""Data models for statutory duty extraction."""

from pydantic import BaseModel, Field


class StatutoryDuty(BaseModel):
    """Model representing a statutory duty extracted from legal documents."""

    duty_description: str = Field(
        ..., description="The specific duty or obligation described"
    )
    duty_holder: str = Field(
        ..., description="The person or organisation who must fulfil the duty"
    )
    legislative_reference: str = Field(
        ..., description="The specific section or regulation reference"
    )


class StatutoryInstrument(BaseModel):
    """Model representing a statutory instrument and its duties."""

    document_title: str = Field(..., description="Title of the statutory instrument")
    document_reference: str = Field(
        ..., description="Official reference number of the document"
    )
    duties: list[StatutoryDuty] = Field(
        default_factory=list, description="List of statutory duties"
    )
