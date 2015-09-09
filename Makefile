test:
	py.test -v tests/* polygonmeshtools/*

pep8:
	py.test -v -s polygonmeshtools/test_pep8.py