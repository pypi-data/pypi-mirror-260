from meritous.core import Store

class FileStore(Store):

    def load(self, fn):
        with open(fn) as fp:
            return super().load(fp.read())
        
    def save(self, fn, model):
        with open(fn, 'w') as fp:
            fp.write(super().save(model))