from support import UploadApi

if __name__ == '__main__':
    upload = UploadApi()

    test_right_data = [
        ['052420205956.jpg', 'image/jpg'],
        ['052420205957.jpg', 'image/jpg'],
        ['052420205958.jpg', 'image/jpg'],
        ['052420205959.jpg', 'image/jpg'],
        ['052420205960.jpg', 'image/jpg'],
        ['052420205961.jpg', 'image/jpg'],
        ['052420205962.jpg', 'image/jpg'],
        ['052420205963.jpg', 'image/jpg'],
        ['052420205964.jpg', 'image/jpg'],
        ['052420205965.jpg', 'image/jpg'],
        ['052420205966.jpg', 'image/jpg'],
        ['052420205966.jpg', 'image/jpg'],
        ['test.jpeg', 'image/jpg'],
        ['test0.jpeg', 'image/jpg'],
        ['test0.jpg', 'image/jpg'],
        ['test_change.jpg', 'image/jpg'],
    ]

    upload.upload([i[0] for i in test_right_data])
