from re import findall
from os import path, environ
from unittest import TestCase
from subprocess import check_output, TimeoutExpired

def find_code_blocks_in_markdown(filename):
    markdown = open(filename).read()
    return findall(r"\`{4}\n([a-z]*[\s\S]*?)\n\`{4}", markdown)

class TestReadme(TestCase):

    def test_readme_instructions_start_the_server(self):
        readme = path.join(environ['PWD'], 'readme.md')
        code_blocks = find_code_blocks_in_markdown(readme)
        run_command = code_blocks[1].replace('stenograpi.py', 'dist/stenograpi.py')
        with self.assertRaisesRegex(TimeoutExpired, 'timed out'):
            check_output(run_command, shell=True, timeout=0.250)
