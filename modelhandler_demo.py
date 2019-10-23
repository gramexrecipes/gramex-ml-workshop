from gramex.config import variables
import os.path as op

DIR = variables['GRAMEXDATA'] + '/apps/mlhandler'


def init_form(handler):
    """Process input from the landing page and write the current session config."""
    data_file = handler.request.files.get('data-file', [{}])[0]
    # TODO: Unix filenames may not be valid Windows filenames.
    outpath = op.join(DIR, "data.csv")
    with open(outpath, 'wb') as fout:
        fout.write(data_file['body'])
    return 'OK'
