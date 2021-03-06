
go: performance-graph.pdf
	evince performance-graph.pdf

performance-graph.pdf: performance-numbers.db gen-performance-graph
	./gen-performance-graph

performance-numbers.db: test-bloom-filter
	./this-pylint \
		--ignore-message ".*Unable to import 'dbm'" \
		--ignore-message ".*Unable to import 'anydbm'" \
		--to-pylint bloom_filter_mod.py test-bloom-filter
	rm -f seek.txt array.txt hybrid.txt mmap.txt
	#/usr/local/pypy-2.3.1/bin/pypy ./test-bloom-filter --performance-test
	/usr/local/pypy-2.3.1/bin/pypy ./test-bloom-filter
	/usr/local/cpython-3.4/bin/python ./test-bloom-filter
	/usr/local/cpython-2.5/bin/python ./test-bloom-filter
	#/usr/local/cpython-2.7/bin/python ./test-bloom-filter
	#/usr/local/cpython-3.0/bin/python ./test-bloom-filter
	/usr/local/jython-2.7b3/bin/jython ./test-bloom-filter

clean:
	rm -f *.pyc *.class
	rm -rf __pycache__
	rm -f bloom-filter-rm-me
	rm -f *.ps *.pdf
	rm -f seek.txt array.txt
	rm -rf dist build bloom_filter.egg-info
	rm -f performance-numbers

veryclean: clean
	rm -f performance-numbers.db
	rm -f performance-numbers

build:
	python setup.py sdist bdist_wheel

