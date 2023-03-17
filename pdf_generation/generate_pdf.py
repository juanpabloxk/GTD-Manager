import jinja2
import pdfkit
from datetime import datetime
from logging_tools import log


def generate_gtd_report(commented_items=[], deleted_items=[], all_items=[]):
    today_date = datetime.today().strftime("%d %b, %Y %R")

    context = {
        'today_date': today_date,
        'commented_items': commented_items,
        'deleted_items': deleted_items,
        'all_items': all_items
    }

    template_loader = jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('pdf_generation/template.html')
    output_text = template.render(context)

    filename = f'reports/gtd_report_{datetime.today().strftime("%d_%b_%Y")}.pdf'

    config = pdfkit.configuration()
    pdfkit.from_string(output_text,
                       filename,
                       options={
                           'encoding': 'UTF-8',
                           'enable-local-file-access': True,
                           'page-size': 'Letter'
                       },
                       configuration=config,
                       css=[
                           'pdf_generation/normalize.css',
                           'pdf_generation/bootstrap.css',
                           'pdf_generation/style.css'
                       ]
                       )

    log('PDF exported', filename)
