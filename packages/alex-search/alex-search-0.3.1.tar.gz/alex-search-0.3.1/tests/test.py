import unittest
from unittest.mock import patch
from venv.bin.openAlex import search_papers, export_data


class TestCLI(unittest.TestCase):
    def test_search_papers(self):
        query = "artificial intelligence"
        results = search_papers(query)
        self.assertTrue(results)
        self.assertIsInstance(results, list)
        self.assertIsInstance(results[0], dict)
        self.assertIn("title", results[0])

        author_filter = "John Doe"
        results_with_author = search_papers(query, author=author_filter)
        for result in results_with_author:
            self.assertIn(author_filter, result.get("author", ""))

    # @patch("builtins.open", unittest.mock.mock_open())
    # def test_export_data(self):
    #     # Test export_data function with sample data and output file
    #     data = [{"title": "Paper 1", "authors": ["Author 1", "Author 2"], "year": 2022},
    #             {"title": "Paper 2", "authors": ["Author 3", "Author 4"], "year": 2023}]
    #     output_file = "test_output.json"
    #     export_data(data, output_file)
    #     # Verify that the output file is created and contains the expected content
    #     with open(output_file, "r") as f:
    #         content = f.read()
    #         self.assertIn("Paper 1", content)
    #         self.assertIn("Paper 2", content)
    #         self.assertIn("Author 1", content)
    #         self.assertIn("Author 2", content)
    #         self.assertIn("Author 3", content)
    #         self.assertIn("Author 4", content)


if __name__ == "__main__":
    unittest.main()
