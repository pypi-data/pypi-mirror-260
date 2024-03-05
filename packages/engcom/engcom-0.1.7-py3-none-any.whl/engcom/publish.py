import argparse
from engcom.publication import Publication

parser = argparse.ArgumentParser(description='Publish a Python script .py or Jupyter .ipynb file.')
parser.add_argument('source_filename', type=str,
                    help='A Python script .py or Jupyter .ipynb file')
parser.add_argument('to', type=str,
                    help='Destination type (md, pdf, or docx)')
parser.add_argument('--source_kind', type=str, required=False, default='script',
                    help='script or ipynb')
parser.add_argument('--title', type=str, required=False, default=None,
                    help='Title of the document')
parser.add_argument('--author', type=str, required=False, default=None,
                    help='Author of the document')
def main():
    args = parser.parse_args()
    pub = Publication(
        title=args.title, 
        author=args.author, 
        source_filename=args.source_filename, 
        source_kind=args.source_kind
    )
    pub.write(to=args.to)
    return 0