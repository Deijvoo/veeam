import unittest
import os
import shutil
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from veeam_task import create_file, copy_file, delete_file, create_directory, delete_directory, sync_folders



class TestSyncFolders(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir'
        cls.source_dir = os.path.join(cls.test_dir, 'source')
        cls.replica_dir = os.path.join(cls.test_dir, 'replica')
        os.makedirs(cls.source_dir, exist_ok=True)
        os.makedirs(cls.replica_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def setUp(self):
        if not os.path.exists(self.source_dir):
            os.makedirs(self.source_dir)
        if not os.path.exists(self.replica_dir):
            os.makedirs(self.replica_dir)
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dire in dirs:
                shutil.rmtree(os.path.join(root, dire))
        for root, dirs, files in os.walk(self.replica_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dire in dirs:
                shutil.rmtree(os.path.join(root, dire))

        empty_dir_source = os.path.join(self.source_dir, 'empty_dir')
        if os.path.exists(empty_dir_source):
            shutil.rmtree(empty_dir_source)

    def test_create_file(self):
        source_file = os.path.join(self.source_dir, 'test_create_file.txt')
        replica_file = os.path.join(self.replica_dir, 'test_create_file.txt')
        with open(source_file, 'w') as f:
            f.write('Test content')
        create_file(source_file, replica_file)
        self.assertTrue(os.path.exists(replica_file))
        with open(replica_file, 'r') as f:
            self.assertEqual(f.read(), 'Test content')

    def test_copy_file(self):
        source_file = os.path.join(self.source_dir, 'test_copy_file.txt')
        replica_file = os.path.join(self.replica_dir, 'test_copy_file.txt')
        with open(source_file, 'w') as f:
            f.write('Test content')
        create_file(source_file, replica_file)
        with open(source_file, 'w') as f:
            f.write('Updated content')
        copy_file(source_file, replica_file)
        with open(replica_file, 'r') as f:
            self.assertEqual(f.read(), 'Updated content')

    def test_delete_file(self):
        replica_file = os.path.join(self.replica_dir, 'test_delete_file.txt')
        os.makedirs(os.path.dirname(replica_file), exist_ok=True)
        with open(replica_file, 'w') as f:
            f.write('Test content')
        delete_file(replica_file)
        self.assertFalse(os.path.exists(replica_file))

    def test_create_directory(self):
        new_dir = os.path.join(self.replica_dir, 'new_directory')
        create_directory(new_dir)
        self.assertTrue(os.path.exists(new_dir))

    def test_delete_directory(self):
        new_dir = os.path.join(self.replica_dir, 'new_directory')
        os.makedirs(new_dir, exist_ok=True)
        delete_directory(new_dir)
        self.assertFalse(os.path.exists(new_dir))

    def test_sync_folders_create(self):
        source_file = os.path.join(self.source_dir, 'test_sync_folders_file.txt')
        replica_file = os.path.join(self.replica_dir, 'test_sync_folders_file.txt')
        with open(source_file, 'w') as f:
            f.write('Test content')
        sync_folders(self.source_dir, self.replica_dir)
        self.assertTrue(os.path.exists(replica_file))
        with open(replica_file, 'r') as f:
            text = f.readline()
        self.assertEqual(text, 'Test content')

    def test_sync_folders_delete_with_files(self):
        replica_file = os.path.join(self.replica_dir, 'test_delete_file.txt')
        os.makedirs(os.path.dirname(replica_file), exist_ok=True)
        with open(replica_file, 'w') as f:
            f.write('Test content')
        sync_folders(self.source_dir, self.replica_dir)
        self.assertFalse(os.path.exists(replica_file))

    def test_sync_folders_delete_empty(self):
        empty_dir = os.path.join(self.replica_dir, 'empty_dir')
        os.makedirs(empty_dir, exist_ok=True)
        self.assertTrue(os.path.exists(empty_dir))
        self.assertFalse(os.path.exists(os.path.join(self.source_dir, 'empty_dir')))
        sync_folders(self.source_dir, self.replica_dir)
        self.assertFalse(os.path.exists(empty_dir))

    def test_sync_folders_copy(self):
        source_file = os.path.join(self.source_dir, 'test_copy_file.txt')
        replica_file = os.path.join(self.replica_dir, 'test_copy_file.txt')
        with open(source_file, 'w') as f:
            f.write('Test content')
        sync_folders(self.source_dir, self.replica_dir)
        self.assertTrue(os.path.exists(replica_file))
        with open(replica_file, 'r') as f:
            self.assertEqual(f.read(), 'Test content')

    def test_sync_folders_copy_empty(self):
        empty_dir = os.path.join(self.source_dir, 'empty_dir')
        os.makedirs(empty_dir, exist_ok=True)
        sync_folders(self.source_dir, self.replica_dir)
        self.assertTrue(os.path.exists(os.path.join(self.replica_dir, 'empty_dir')))

    def test_sync_folders_update(self):
        source_file = os.path.join(self.source_dir, 'test_update_file.txt')
        replica_file = os.path.join(self.replica_dir, 'test_update_file.txt')
        with open(source_file, 'w') as f:
            f.write('Test content')
        sync_folders(self.source_dir, self.replica_dir)
        self.assertTrue(os.path.exists(replica_file))
        with open(source_file, 'w') as f:
            f.write('Updated content')
        sync_folders(self.source_dir, self.replica_dir)
        with open(replica_file, 'r') as f:
            self.assertEqual(f.read(), 'Updated content')

    def test_sync_folders_missing_directories(self):

        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        if os.path.exists(self.replica_dir):
            shutil.rmtree(self.replica_dir)

        self.assertFalse(os.path.exists(self.source_dir))
        self.assertFalse(os.path.exists(self.replica_dir))

        with self.assertLogs(level=logging.ERROR) as log:
            sync_folders(self.source_dir, self.replica_dir)
        self.assertIn("Source directory does not exist", log.output[0])
        self.assertIn("Replica directory does not exist", log.output[1])


if __name__ == '__main__':
    unittest.main()
