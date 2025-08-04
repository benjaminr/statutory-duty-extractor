"""Core extraction functionality for statutory duties."""

import logging
from pathlib import Path

import pymupdf
from openai import AzureOpenAI
from pydantic import ValidationError

from .models import StatutoryInstrument

logger = logging.getLogger(__name__)


class StatutoryDutyExtractor:
    """Extract statutory duties from UK statutory instruments using Azure OpenAI."""

    def __init__(
        self,
        azure_endpoint: str,
        api_key: str,
        api_version: str = "2025-03-01-preview",
        deployment_name: str = "gpt-4o-mini",
    ):
        """
        Initialise the extractor with Azure OpenAI credentials.

        Args:
            azure_endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            api_version: API version to use
            deployment_name: Name of the deployed model
        """
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self.deployment_name = deployment_name
        self.prompts_dir = Path(__file__).parent.parent.parent / "prompts"

    def load_prompt(self, prompt_name: str) -> str:
        """Load a prompt from the prompts directory."""
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        return prompt_file.read_text(encoding="utf-8")

    def extract_duties_from_text(
        self, document_text: str, document_title: str, document_reference: str
    ) -> StatutoryInstrument:
        """
        Extract statutory duties from a document.

        Args:
            document_text: Full text of the statutory instrument
            document_title: Title of the document
            document_reference: Official reference number

        Returns:
            StatutoryInstrument containing extracted duties
        """
        try:
            system_prompt = self.load_prompt("system_prompt").format(
                document_title=document_title, document_reference=document_reference
            )
            user_prompt = self.load_prompt("user_prompt").format(
                document_text=document_text
            )

            response = self.client.beta.chat.completions.parse(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                response_format=StatutoryInstrument,
            )

            return response.choices[0].message.parsed or StatutoryInstrument(
                document_title=document_title,
                document_reference=document_reference,
                duties=[],
            )

        except ValidationError as e:
            logger.error(f"Validation error parsing response: {e}")
            return StatutoryInstrument(
                document_title=document_title,
                document_reference=document_reference,
                duties=[],
            )
        except Exception as e:
            logger.error(f"Error extracting duties: {e}")
            return StatutoryInstrument(
                document_title=document_title,
                document_reference=document_reference,
                duties=[],
            )

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from a PDF file using PyMuPDF."""
        try:
            doc = pymupdf.open(pdf_path)
            text_content = ""

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()
                text_content += "\n\n"

            doc.close()
            return text_content.strip()

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""

    def extract_duties_from_pdf(
        self, pdf_path: Path, document_title: str, document_reference: str
    ) -> StatutoryInstrument:
        """
        Extract statutory duties from a PDF document.

        Args:
            pdf_path: Path to the PDF file
            document_title: Title of the document
            document_reference: Official reference number

        Returns:
            StatutoryInstrument containing extracted duties
        """
        try:
            logger.info(f"Extracting text from PDF: {pdf_path.name}")
            document_text = self.extract_text_from_pdf(pdf_path)

            if not document_text:
                logger.warning("No text extracted from PDF")
                return StatutoryInstrument(
                    document_title=document_title,
                    document_reference=document_reference,
                    duties=[],
                )

            logger.info(f"Extracted {len(document_text)} characters from PDF")

            return self.extract_duties_from_text(
                document_text=document_text,
                document_title=document_title,
                document_reference=document_reference,
            )

        except Exception as e:
            logger.error(f"Error extracting duties from PDF: {e}")
            return StatutoryInstrument(
                document_title=document_title,
                document_reference=document_reference,
                duties=[],
            )
