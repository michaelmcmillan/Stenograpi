from re import findall
from os import path, environ
from unittest import TestCase
from subprocess import check_output, TimeoutExpired

def get_markdown(filename):
    return open(filename).read()

def find_code_blocks_in_markdown(markdown):
    return findall(r"\`{4}\n([a-z]*[\s\S]*?)\n\`{4}", markdown)

class TestReadme(TestCase):

    @classmethod
    def setUpClass(cls):
        readme_location = path.join(environ['PWD'], 'readme.md')
        cls.readme_markdown = get_markdown(readme_location)

    def test_readme_provides_the_correct_download_url(self):
        code_blocks = find_code_blocks_in_markdown(self.readme_markdown)
        download_command = code_blocks[0]
        domain = 'https://raw.githubusercontent.com/michaelmcmillan'
        self.assertIn(domain + '/Stenograpi/master/dist/stenograpi.py', download_command)

    def test_readme_instructions_start_the_server(self):
        code_blocks = find_code_blocks_in_markdown(self.readme_markdown)
        run_command = code_blocks[1].replace('stenograpi.py', 'dist/stenograpi.py')
        with self.assertRaisesRegex(TimeoutExpired, 'timed out'):
            check_output(run_command, shell=True, timeout=0.250)
