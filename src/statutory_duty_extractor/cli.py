"""Command-line interface for statutory duty extraction."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from .extractor import StatutoryDutyExtractor

console = Console()
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


def setup_extractor() -> StatutoryDutyExtractor:
    """Set up the extractor with Azure OpenAI credentials from environment."""
    load_dotenv(override=True)

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

    if not azure_endpoint or not api_key:
        raise ValueError(
            "Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables"
        )

    return StatutoryDutyExtractor(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment_name,
    )


def extract_from_file(file_path: Path) -> None:
    """Extract duties from a single file and display results."""
    extractor = setup_extractor()

    console.print(f"\n[bold blue]Processing:[/bold blue] {file_path.name}")

    try:
        document_title = file_path.stem.replace("_", " ").title()
        document_reference = file_path.stem.upper()

        # Handle PDF files directly, text files as before
        if file_path.suffix.lower() == ".pdf":
            result = extractor.extract_duties_from_pdf(
                pdf_path=file_path,
                document_title=document_title,
                document_reference=document_reference,
            )
        else:
            document_text = file_path.read_text(encoding="utf-8")
            result = extractor.extract_duties_from_text(
                document_text=document_text,
                document_title=document_title,
                document_reference=document_reference,
            )

        if not result.duties:
            console.print("[bold yellow]Warning:[/bold yellow] No duties extracted")
            return

        table = Table(title=f"Statutory Duties - {result.document_title}")
        table.add_column("Duty Holder", style="cyan", width=20)
        table.add_column("Duty Description", style="white", no_wrap=False)
        table.add_column("Reference", style="green", width=15)

        for duty in result.duties:
            table.add_row(
                duty.duty_holder,
                duty.duty_description,
                duty.legislative_reference,
            )

        console.print(table)
        console.print(
            f"\n[bold green]Extracted {len(result.duties)} duties[/bold green]"
        )

    except Exception as e:
        console.print(f"[bold red]Failed to process file:[/bold red] {e}")


def main() -> None:
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract statutory duties from UK statutory instruments"
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to statutory instrument file to process",
    )

    args = parser.parse_args()

    if not args.file.exists():
        console.print(f"[bold red]Error:[/bold red] File not found: {args.file}")
        return

    extract_from_file(args.file)


if __name__ == "__main__":
    main()
