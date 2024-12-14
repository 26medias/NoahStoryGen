# pdf_builder.py

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, PageBreak, Table, TableStyle
from bs4 import BeautifulSoup
from typing import List, Tuple
import logging

class PdfBuilder:
    """
    A class to convert multiple HTML files into a single PDF file,
    with each HTML file represented as a separate page.
    """

    def __init__(self):
        """
        Initializes the PdfBuilder.
        Sets up logging configuration.
        """
        self.setup_logging()

    def setup_logging(self):
        """
        Configures the logging settings.
        Logs will be printed to the console with timestamps and log levels.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.StreamHandler()
            ]
        )

    def parse_html(self, html_path: str) -> Tuple[str, str]:
        """
        Parses the HTML file and extracts image source and text content.

        Parameters:
        - html_path (str): Path to the input HTML file.

        Returns:
        - Tuple[str, str]: A tuple containing image path and text content.
        """
        try:
            with open(html_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            # Extract image src
            img_tag = soup.find('img')
            img_src = img_tag['src'] if img_tag and img_tag.has_attr('src') else None

            # Extract text inside <p> tag
            p_tag = soup.find('p')
            text_content = p_tag.get_text().strip() if p_tag else ''

            return (img_src, text_content)
        except Exception as e:
            logging.error(f"Error parsing HTML file {html_path}: {e}")
            return (None, '')

    def add_image_with_border(self, img_path: str, styles: ParagraphStyle) -> Image:
        """
        Creates an Image flowable with a border.

        Parameters:
        - img_path (str): Path to the image file.
        - styles (ParagraphStyle): Styles for the image (unused but kept for consistency).

        Returns:
        - Image: ReportLab Image flowable with border.
        """
        try:
            if not os.path.isfile(img_path):
                logging.warning(f"Image file {img_path} not found.")
                return None

            # Create Image flowable
            img = Image(img_path)

            # Set image size (adjust as needed)
            img.drawWidth = 100 * mm
            img.drawHeight = 100 * mm

            # Create a table to add border around the image
            table = Table([[img]], colWidths=[img.drawWidth + 4], rowHeights=[img.drawHeight + 4])
            table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 2, colors.black),  # Border around the image
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))

            return table
        except Exception as e:
            logging.error(f"Error adding image with border: {e}")
            return None

    def add_text(self, text: str, styles: ParagraphStyle) -> Paragraph:
        """
        Creates a Paragraph flowable with specified styles.

        Parameters:
        - text (str): The text content.
        - styles (ParagraphStyle): Styles to apply to the text.

        Returns:
        - Paragraph: ReportLab Paragraph flowable.
        """
        try:
            paragraph = Paragraph(text, styles)
            return paragraph
        except Exception as e:
            logging.error(f"Error adding text to PDF: {e}")
            return None

    def generate_pdf(self, html_files: List[str], output_pdf: str, cwd: str):
        """
        Generates the PDF by parsing HTML files and adding content to the PDF.

        Parameters:
        - html_files (List[str]): List of HTML filenames to convert.
        - output_pdf (str): The name/path of the output PDF file.
        - cwd (str): Current working directory where HTML files and resources are located.
        """
        try:
            # Set up the PDF document
            doc = SimpleDocTemplate(
                output_pdf,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )

            # Define styles
            styles = getSampleStyleSheet()
            bold_style = ParagraphStyle(
                name='Bold',
                parent=styles['Normal'],
                fontName='Helvetica-Bold',
                fontSize=30,
                leading=36,  # Ensures proper line spacing
                alignment=1,  # Center alignment
                spaceAfter=20  # Adds spacing after the paragraph
            )

            elements = []

            for html_file in html_files:
                html_path = os.path.join(cwd, html_file)
                img_src, text_content = self.parse_html(html_path)

                # Add image with border
                if img_src:
                    img_path = os.path.join(cwd, img_src)
                    img_flowable = self.add_image_with_border(img_path, bold_style)
                    if img_flowable:
                        elements.append(img_flowable)
                else:
                    logging.warning(f"No image found in {html_file}.")

                # Add text
                if text_content:
                    paragraph = self.add_text(text_content, bold_style)
                    if paragraph:
                        elements.append(paragraph)
                else:
                    logging.warning(f"No text found in {html_file}.")

                # Add a page break after each HTML file except the last one
                if html_file != html_files[-1]:
                    elements.append(PageBreak())

            # Build the PDF
            doc.build(elements)
            logging.info(f"PDF generated successfully as {output_pdf}")

        except Exception as e:
            logging.error(f"Error generating PDF: {e}")

    def generate(self, html_files: List[str], filename: str, cwd: str, max_workers: int = 4):
        """
        Public method to generate the PDF from HTML files.

        Parameters:
        - html_files (List[str]): List of HTML filenames to convert.
        - filename (str): The name/path of the output PDF file.
        - cwd (str): Current working directory where HTML files and resources are located.
        - max_workers (int): Number of threads for parallel processing (not utilized here).
        """
        try:
            # Validate input
            if not html_files:
                raise ValueError("No HTML files provided for conversion.")

            # Resolve absolute path
            cwd = os.path.abspath(cwd)
            if not os.path.isdir(cwd):
                raise NotADirectoryError(f"The specified cwd is not a directory: {cwd}")

            # Verify that all HTML files exist
            for html in html_files:
                html_path = os.path.join(cwd, html)
                if not os.path.isfile(html_path):
                    raise FileNotFoundError(f"HTML file not found: {html_path}")

            # Generate PDF
            self.generate_pdf(html_files, filename, cwd)

        except Exception as e:
            logging.error(f"Exception in generate method: {e}")
