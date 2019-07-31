from random import sample
import os, json, shutil
import random

import click
import jinja2
from z3c.rml import rml2pdf

STATIC_ROOT = "static/"

def render_rml(data,card_no,request=None):

    # t = get_template('bingocard.xml')
    # c = RequestContext(request,{'data':data})
    # rml = t.render(c)
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "static/tpl/bingocard.xml"
    template = templateEnv.get_template(TEMPLATE_FILE)
    rml = template.render(data=data,static=STATIC_ROOT)
    try:
        pdf = rml2pdf.parseString(rml)
    except Exception as e:
        print("Error %s" % e)
        return False


    # Save PDF to file and store
    filename = "bingocard_%s.pdf" % card_no
    pdf_filename = os.path.join(STATIC_ROOT,'cards',filename)
    # ... and save it.
    with open(pdf_filename, 'wb') as pdfFile:
       pdfFile.write(pdf.read())
    return True

def create_pdf(card_no=None,request=None):
    objs = random.sample(range(1,110), 12)
    data = []
    for num in objs:
        filename = "M{}.json".format(num)
        fullpath = os.path.join(STATIC_ROOT,'db',filename)
        jdata = open(fullpath)
        jsondata = json.load(jdata)
        image = {}
        image['file'] = os.path.join(STATIC_ROOT,"objects", jsondata['observation']['image']['about'].split("/")[-1])
        name = jsondata['observation']['label'].split(" ")
        image['name'] = name[0]
        data.append(image)
    resp = render_rml(data,card_no,request)
    return resp

@click.command()
@click.option("--cards", default=1, help="Number of cards.")
def main(cards):
    # remove all existing cards
    folder = os.path.join(STATIC_ROOT,'cards')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
          os.unlink(file_path)
        except Exception as e:
            print(e)
    print('Removed all existing cards\n')
    for n in range(0,cards):
        cardname = create_pdf(n)
        if cardname:
            print('Created card %s of %s\n' % (n+1,cards))
        else:
            print('Card creation failed')

if __name__ == '__main__':
    main()
