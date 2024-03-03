from .si_data import Package, DIRNAMES, Context
from zipfile import ZipFile
import argparse
import os
import xml.etree.ElementTree as etree
import yaml
import shutil


def make_content_types():
    types = {
        'xml': 'si/xml',
        'png': 'si/image',
        'jpg': 'si/image',
        'jpeg': 'si/image',
        'mp3': 'si/audio',
    }
    root = etree.Element('Types', {
        'xmlns': 'http://schemas.openxmlformats.org/package/2006/content-types'
    })
    for k, v in types.items():
        etree.SubElement(root, 'Default', {
            'Extension': k,
            'ContentType': v,
        })
    return etree.ElementTree(root)


def main():
    parser = argparse.ArgumentParser(description='Converts YAML to SIQ and back')
    parser.add_argument('input', help='Input file (yml or siq)')
    parser.add_argument('output', nargs='?', help='Output file')
    options = parser.parse_args()

    context = Context()
    if options.input.endswith('.siq'):
        # Load XML
        input_xml = True
        context.base_path = os.path.dirname(options.output or options.input)
        with ZipFile(options.input, 'r') as siq:
            with siq.open('content.xml', 'r') as content:
                root = etree.parse(content).getroot()
            # Extract all media files into /media
            media_path = os.path.join(context.base_path, 'media')
            for name in siq.namelist():
                parts = name.split('/')
                if parts[0] in DIRNAMES.values():
                    if not os.path.exists(media_path):
                        os.mkdir(media_path)
                    if len(parts) != 2:
                        print(f'Skip "{name}", subdirs not supported')
                    # Empty dir
                    if not parts[-1]:
                        continue
                    target = os.path.join(media_path, parts[-1])
                    with siq.open(name) as source:
                        with open(target, 'wb') as target:
                            shutil.copyfileobj(source, target)
        package = Package.from_xml(root, context)
    else:
        # Load YAML
        input_xml = False
        context.base_path = os.path.dirname(options.input)
        with open(options.input, 'r') as f:
            data = yaml.safe_load(f)
        package = Package.from_yaml(data)

    if options.output:
        need_xml = options.output.endswith('.siq')
        output = options.output
    else:
        need_xml = not input_xml
        ext = '.siq' if need_xml else '.yml'
        output = os.path.splitext(options.input)[0] + ext

    if need_xml:
        with ZipFile(output, 'w') as siq:
            with siq.open('content.xml', 'w') as content:
                tree = etree.ElementTree(package.to_xml())
                tree.write(content, encoding='utf-8', xml_declaration=True)
            with siq.open('Texts/authors.xml', 'w') as authors:
                authors.write('<?xml version="1.0" encoding="utf-8"?><Authors />'.encode())
            with siq.open('Texts/sources.xml', 'w') as sources:
                sources.write('<?xml version="1.0" encoding="utf-8"?><Sources />'.encode())
            with siq.open('[Content_Types].xml', 'w') as ct:
                tree = make_content_types()
                tree.write(ct, encoding='utf-8', xml_declaration=True)
            # And now packing files
            for r in package.rounds:
                for t in r.themes:
                    for q in t.questions:
                        for a in q.scenario:
                            if a.path:
                                siq.write(a.path, f'{a.dirname}/{a.value}')
            if package.logo_path:
                siq.write(package.logo_path, f'Images/{package.logo_name}')
    else:
        with open(output, 'w') as f:
            yaml.dump(package.to_yaml(), f, allow_unicode=True)


if __name__ == '__main__':
    main()
