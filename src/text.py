from .items import Items


class Text(Items):
    def __init__(self, bbox):
        super().__init__(bbox)
        self.type = 'Text'
        self._text = ''

    def setText(self, text):
        self._text = text

    def getText(self):
        return self._text

    def getBox(self):
        return [self.bbox.xmin, self.bbox.ymin, self.bbox.xmax, self.bbox.ymax]
