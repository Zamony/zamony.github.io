import unittest

from publish import *

class DSSSGTest(unittest.TestCase):
	def test_translit(self):
		self.assertEqual( translit(""), "" )
		self.assertEqual( translit(" абба "), "abba" )
		self.assertEqual( translit(" аб    б7а "), "ab-b7a" )
		self.assertEqual( translit(" аб. : '+ _ ба        "), "ab-ba" )
		self.assertEqual( translit("hello-    ----------    world : "), "hello-world" )

	def test_load_post_structure(self):
		try:
			load_post_structure("./_tests/test_empty_date.md")
			self.assertEqual(0, 1)
		except SystemExit:
			pass

		try:
			load_post_structure("./_tests/test_empty_title.md")
			self.assertEqual(0, 1)
		except SystemExit:
			pass

		posts = load_post_structure("./_tests/test_correct_load.md")
		self.assertEqual(posts["date"], datetime.datetime.strptime("09.09.2017", "%d.%m.%Y"))
		self.assertEqual(posts["title"], "test0")
		self.assertEqual(posts["meta_keywords"], "test1")
		self.assertEqual(posts["meta_description"], "test2")

if __name__ == "__main__": 
    unittest.main()