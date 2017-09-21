import logging
from collections import namedtuple
from xml.etree import cElementTree
from zipfile import ZipFile

from lxml import html
from lxml.html.clean import clean_html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Bulletin = namedtuple("Bulletin",
                      ["fichier",
                       "numero",
                       "date",
                       "rubrique",
                       "titre",
                       "texte",
                       "images",
                       "contact"])
Image = namedtuple("Image", ["urlImage", "legendeImage"])


def parse_bulletins(archive_path):
    with ZipFile(archive_path) as zip_file:
        filelist = [file.filename for file in zip_file.filelist
                    if 'BULLETINS' in file.filename and file.filename.endswith(".htm")]

        logger.info("%s files in archive %s", len(filelist), archive_path)

        for file_path in filelist:
            with zip_file.open(file_path) as file:
                logger.info("Parsing %s.", file_path)
                content = file.read()
                tree = clean_html(html.fromstring(content))
                title = tree.xpath('//*[@class="style17"]/text()')[0].strip()
                date, rubrique = tree.xpath('//*[@class="style42"]/text()')
                date = date.strip()
                rubrique = rubrique.strip()
                text_content = "\n".join([el.text_content().strip()
                                          for el in tree.xpath('//*[@width="452"]//*[@class="style95"]')[:-1]])
                assert all([alt == '' or alt == 'spacer' for alt in tree.xpath('//img/@alt')])
                # img_legends = tree.xpath('//img/@alt')
                img_legends = [img_legend.text_content().strip() for img_legend in
                                tree.xpath('//*[@class="style21"]')[1:]]
                i = 0
                images = []
                for url_img in tree.xpath('//img/@src'):
                    if '/Resources' not in url_img:
                        try:
                            img_legend = img_legends[i]
                        except IndexError:
                            img_legend = ""

                        images.append(Image(urlImage=url_img.strip(), legendeImage=img_legend))
                        i += 1
                nb_unused_images = len(tree.xpath('//img')) - len(images)
                assert nb_unused_images == 102

                info_contact = tree.xpath('//*[@class="style85"]')[3].text_content().strip()

                numero = tree.xpath('//*[@class="style32"]/text()')[0].strip()
                yield Bulletin(
                    fichier=file_path,
                    numero=numero,
                    date=date,
                    rubrique=rubrique,
                    titre=title,
                    texte=text_content,
                    images=images,
                    contact=info_contact,
                )


if __name__ == "__main__":

    logger.info("Starting to parse file.")

    root = cElementTree.Element("corpus")

    nb_bulletins = 0
    for bulletin in parse_bulletins('./BULLETINS_LO17.zip'):
        logger.info("Writing in xml content of %s.", bulletin.fichier)

        bulletin_xml_element = cElementTree.SubElement(root, "bulletin")
        cElementTree.SubElement(bulletin_xml_element, "fichier").text = bulletin.fichier
        cElementTree.SubElement(bulletin_xml_element, "numero").text = bulletin.numero
        cElementTree.SubElement(bulletin_xml_element, "date").text = bulletin.date
        cElementTree.SubElement(bulletin_xml_element, "rubrique").text = bulletin.rubrique
        cElementTree.SubElement(bulletin_xml_element, "titre").text = bulletin.titre
        cElementTree.SubElement(bulletin_xml_element, "texte").text = bulletin.texte
        images_xml_element = cElementTree.SubElement(bulletin_xml_element, "images")
        for image in bulletin.images:
            image_xml_element = cElementTree.SubElement(images_xml_element, "image")
            cElementTree.SubElement(image_xml_element, "urlImage").text = image.urlImage
            cElementTree.SubElement(image_xml_element, "legendeImage").text = image.legendeImage
        cElementTree.SubElement(bulletin_xml_element, "contact").text = bulletin.contact

        nb_bulletins += 1

    logger.info("Read and wrote %d bulletins.", nb_bulletins)

    tree = cElementTree.ElementTree(root)
    tree.write("filename.xml", encoding="UTF-8")
