from re import findall
from unittest import TestCase
from subprocess import check_output, TimeoutExpired
from os import path, getcwd, name as operating_system

def file_exists(path_to_file):
    return path.isfile(path_to_file)

def get_markdown(path_to_file):
    return open(path_to_file).read()

def find_code_blocks_in_markdown(markdown):
    return findall(r"\`{4}\n([a-z]*[\s\S]*?)\n\`{4}", markdown)

def find_links_in_markdown(markdown):
    return dict(findall(r"\[(.*)\]\((.*)\)", markdown))

class TestReadme(TestCase):

    @classmethod
    def setUpClass(cls):
        readme_location = path.join(getcwd(), 'readme.md')
        cls.readme_markdown = get_markdown(readme_location)

    def test_readme_provides_the_correct_download_url(self):
        code_blocks = find_code_blocks_in_markdown(self.readme_markdown)
        download_command = code_blocks[0]
        domain = 'https://raw.githubusercontent.com/michaelmcmillan'
        self.assertIn(domain + '/Stenograpi/master/dist/stenograpi.py', download_command)

    def test_readme_instructions_start_the_server(self):
        code_blocks = find_code_blocks_in_markdown(self.readme_markdown)
        run_command = code_blocks[1].replace('stenograpi.py', 'dist/stenograpi.py')
        if operating_system == 'nt':
            run_command = run_command.replace('python3', '%PYTHON%/python')
        with self.assertRaisesRegex(TimeoutExpired, 'timed out'):
            check_output(run_command, shell=True, timeout=0.250)

    def test_link_to_example_output_is_not_broken(self):
        links = find_links_in_markdown(self.readme_markdown)
        output_example_target = links['see for yourself']
        output_example_location = path.join(getcwd(), output_example_target)
        self.assertTrue(file_exists(output_example_location))
