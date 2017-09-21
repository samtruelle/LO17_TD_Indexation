from zipfile import ZipFile

from lxml import html
from lxml.html.clean import clean_html


def parse_bulletins(archive_path):
    with ZipFile(archive_path) as zip_file:
        filelist = [file.filename for file in zip_file.filelist
                    if 'BULLETINS' in file.filename
                    and file.filename.endswith(".htm")]

        for file_path in filelist:
            with zip_file.open(file_path) as file:
                content = file.read()
                tree = clean_html(html.fromstring(content))
                yield from tree.xpath('//img/@src')


if __name__ == "__main__":
    print(len(sorted(list(set(parse_bulletins('./BULLETINS_LO17.zip'))))))
    print(len(sorted((parse_bulletins('./BULLETINS_LO17.zip')))))
