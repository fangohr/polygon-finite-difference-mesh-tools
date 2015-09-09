test:
	py.test -v polygonmeshtools

pep8:
	py.test -v -s polygonmeshtools/check_pep8.py

coverage:
	py.test --cov=polygonmeshtools  --cov-report=html polygonmeshtools 
	# Open htmlcov/index.html to see coverage report