#!/usr/bin/env python3
"""
Tests for the pod_repo_push command
"""

import os
import unittest
from unittest import mock
from pathlib import Path
import tempfile
import shutil
import sys

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lee_devkit.commands import pod_repo_push
from lee_devkit.config import Config


class TestPodRepoPush(unittest.TestCase):
    """Test the pod_repo_push command"""
    
    def setUp(self):
        """Set up the test environment"""
        # Create a temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create a mock config
        self.config = mock.MagicMock(spec=Config)
        self.config.get_spec_repos.return_value = {
            'NBSpecs': 'git@git.ninebot.com:iOS/NBSpecs.git',
            'TestSpecs': 'git@example.com:test/specs.git'
        }
        self.config.get_default_spec_repo.return_value = 'NBSpecs'
        self.config.get_spec_repo_url.return_value = 'git@git.ninebot.com:iOS/NBSpecs.git'
    
    def tearDown(self):
        """Clean up the test environment"""
        os.chdir(self.old_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_find_podspec_file_none(self):
        """Test finding podspec files when none exist"""
        # Mock the input function to avoid blocking the test
        with mock.patch('builtins.input', return_value='1'):
            result = pod_repo_push.find_podspec_file()
        
        self.assertIsNone(result)
    
    def test_find_podspec_file_single(self):
        """Test finding podspec files when a single one exists"""
        # Create a test podspec file
        with open('TestLib.podspec', 'w') as f:
            f.write('# Test podspec file')
        
        # Mock the input function to avoid blocking the test
        with mock.patch('builtins.input', return_value='1'):
            result = pod_repo_push.find_podspec_file()
        
        self.assertEqual(result, 'TestLib.podspec')
    
    def test_find_podspec_file_multiple(self):
        """Test finding podspec files when multiple exist"""
        # Create test podspec files
        with open('TestLib1.podspec', 'w') as f:
            f.write('# Test podspec file 1')
        with open('TestLib2.podspec', 'w') as f:
            f.write('# Test podspec file 2')
        
        # Mock the input function to select the second file
        with mock.patch('builtins.input', return_value='2'):
            result = pod_repo_push.find_podspec_file()
        
        self.assertEqual(result, 'TestLib2.podspec')
    
    def test_find_podspec_file_json(self):
        """Test finding podspec files with .podspec.json extension"""
        # Create a test podspec.json file
        with open('TestLib.podspec.json', 'w') as f:
            f.write('{"name": "TestLib"}')
        
        # Mock the input function to avoid blocking the test
        with mock.patch('builtins.input', return_value='1'):
            result = pod_repo_push.find_podspec_file()
        
        self.assertEqual(result, 'TestLib.podspec.json')
    
    def test_push_options_default(self):
        """Test PushOptions with default values"""
        options = pod_repo_push.PushOptions()
        args = options.to_args()
        
        # Check that default options are included
        self.assertIn('--allow-warnings', args)
        self.assertIn('--verbose', args)
        self.assertIn('--skip-import-validation', args)
        self.assertIn('--use-libraries', args)
        self.assertIn('--use-modular-headers', args)
    
    def test_push_options_custom(self):
        """Test PushOptions with custom values"""
        options = pod_repo_push.PushOptions()
        options.allow_warnings = False
        options.verbose = False
        options.swift_version = '5.0'
        options.sources = ['git@example.com:test/specs.git']
        options.extra_args = ['--no-subspecs']
        
        args = options.to_args()
        
        # Check that custom options are handled correctly
        self.assertNotIn('--allow-warnings', args)
        self.assertNotIn('--verbose', args)
        self.assertIn('--skip-import-validation', args)
        self.assertIn('--use-libraries', args)
        self.assertIn('--use-modular-headers', args)
        self.assertIn('--swift-version', args)
        self.assertEqual(args[args.index('--swift-version') + 1], '5.0')
        self.assertIn('--sources', args)
        self.assertEqual(args[args.index('--sources') + 1], 'git@example.com:test/specs.git')
        self.assertIn('--no-subspecs', args)
    
    def test_push_options_from_args(self):
        """Test creating PushOptions from command line arguments"""
        # Create mock arguments
        args = mock.MagicMock()
        args.no_allow_warnings = True
        args.no_verbose = False
        args.no_skip_import_validation = False
        args.no_use_libraries = True
        args.no_use_modular_headers = False
        args.extra_args = '--swift-version=5.0,--no-subspecs'
        
        options = pod_repo_push.PushOptions.from_args(args)
        args_list = options.to_args()
        
        # Check that options are set correctly from arguments
        self.assertNotIn('--allow-warnings', args_list)
        self.assertIn('--verbose', args_list)
        self.assertIn('--skip-import-validation', args_list)
        self.assertNotIn('--use-libraries', args_list)
        self.assertIn('--use-modular-headers', args_list)
        self.assertIn('--swift-version=5.0', args_list)
        self.assertIn('--no-subspecs', args_list)
    
    def test_build_push_command(self):
        """Test building the pod repo push command"""
        options = pod_repo_push.PushOptions()
        command = pod_repo_push.build_push_command(
            'NBSpecs', 
            'TestLib.podspec', 
            options, 
            'git@git.ninebot.com:iOS/NBSpecs.git'
        )
        
        # Check the command structure
        self.assertEqual(command[0], 'pod')
        self.assertEqual(command[1], 'repo')
        self.assertEqual(command[2], 'push')
        self.assertEqual(command[3], 'NBSpecs')
        self.assertEqual(command[4], 'TestLib.podspec')
        self.assertIn('--allow-warnings', command)
        self.assertIn('--verbose', command)
        self.assertIn('--skip-import-validation', command)
        self.assertIn('--use-libraries', command)
        self.assertIn('--use-modular-headers', command)
        self.assertIn('--sources', command)
        self.assertIn('git@git.ninebot.com:iOS/NBSpecs.git', command)
    
    def test_get_repositories(self):
        """Test getting repositories from config"""
        repos = pod_repo_push.get_repositories(self.config)
        
        self.assertEqual(len(repos), 2)
        self.assertIn('NBSpecs', repos)
        self.assertIn('TestSpecs', repos)
        self.assertEqual(repos['NBSpecs'], 'git@git.ninebot.com:iOS/NBSpecs.git')
        self.assertEqual(repos['TestSpecs'], 'git@example.com:test/specs.git')
    
    def test_get_default_repository(self):
        """Test getting the default repository"""
        default_repo = pod_repo_push.get_default_repository(self.config)
        
        self.assertEqual(default_repo, 'NBSpecs')
    
    def test_get_repository_url(self):
        """Test getting a repository URL"""
        url = pod_repo_push.get_repository_url(self.config, 'NBSpecs')
        
        self.assertEqual(url, 'git@git.ninebot.com:iOS/NBSpecs.git')
    
    def test_list_repositories(self):
        """Test listing repositories"""
        with mock.patch('builtins.print') as mock_print:
            result = pod_repo_push.list_repositories(self.config)
        
        self.assertTrue(result)
        mock_print.assert_called()
    
    def test_add_repository(self):
        """Test adding a repository"""
        with mock.patch('builtins.print') as mock_print:
            result = pod_repo_push.add_repository(
                self.config, 'NewRepo', 'git@example.com:new/repo.git'
            )
        
        self.assertTrue(result)
        self.config.add_spec_repo.assert_called_with('NewRepo', 'git@example.com:new/repo.git')
        mock_print.assert_called()
    
    def test_add_repository_invalid_url(self):
        """Test adding a repository with invalid URL"""
        with mock.patch('builtins.print') as mock_print:
            result = pod_repo_push.add_repository(
                self.config, 'NewRepo', 'invalid-url'
            )
        
        self.assertFalse(result)
        self.config.add_spec_repo.assert_not_called()
        mock_print.assert_called()
    
    def test_remove_repository(self):
        """Test removing a repository"""
        with mock.patch('builtins.print') as mock_print:
            result = pod_repo_push.remove_repository(self.config, 'NBSpecs')
        
        self.assertTrue(result)
        self.config.remove_spec_repo.assert_called_with('NBSpecs')
        mock_print.assert_called()
    
    def test_set_default_repository(self):
        """Test setting the default repository"""
        with mock.patch('builtins.print') as mock_print:
            result = pod_repo_push.set_default_repository(self.config, 'TestSpecs')
        
        self.assertTrue(result)
        self.config.set_default_spec_repo.assert_called_with('TestSpecs')
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()