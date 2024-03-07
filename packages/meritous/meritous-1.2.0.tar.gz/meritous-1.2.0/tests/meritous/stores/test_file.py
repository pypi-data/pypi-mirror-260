import data

from meritous.core.stores import FileStore  
from meritous.core.serializers import JSONSerializer
from meritous.core import Model, Property
import meritous.core.exceptions

class ModelTest(Model):
    _schema = {
        data.TEST_STR : Property(str, data.TEST_STR_ALT)
    }

def test_filestore_save(tmp_path):
    fn = tmp_path / "test_output.json"
    fs = FileStore(ModelTest, JSONSerializer)
    m = ModelTest()
    fs.save(fn, m)
    assert fn.read_text() == '{"TEST": "TEST ALT"}'

def test_filestore_load(tmp_path):
    fn = tmp_path / "test_input.json"
    fn.write_text('{"TEST": "TEST ALT"}')
    fs = FileStore(ModelTest, JSONSerializer)
    m = fs.load(fn)
    assert m.TEST == data.TEST_STR_ALT

