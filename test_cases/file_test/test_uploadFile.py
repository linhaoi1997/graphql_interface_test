from support.base_test.base_api.SpecialApi import UploadApi
from support import BaseTestCase, run


class TestUpload(BaseTestCase):
    upload = UploadApi()

    def test_upload_jpg(self):
        result = self.upload.upload(["test1.jpeg", "test2.jpeg", "test3.jpeg"])
        self.assertCorrect(result)


if __name__ == '__main__':
    run(__file__)
