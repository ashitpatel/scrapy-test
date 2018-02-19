# Based on https://stackoverflow.com/questions/33290876/how-to-create-custom-scrapy-item-exporter

from scrapy.exporters import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.utils.python import to_bytes

class FasttextItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self.file = file
#        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.first_item = True

    def start_exporting(self):
        self.file.write(b'')

    def finish_exporting(self):
        self.file.write(b'\n')

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        # write to file only if one or more labels and content both exist
        if itemdict['labels'] and itemdict['content']:
            self.file.write(to_bytes(itemdict['labels'] + ' ' + itemdict['content'] + '\n'))
