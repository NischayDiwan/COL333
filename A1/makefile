all:
	clear
	python run.py -src data/input.txt -tar data/pred.txt -tm 2
	diff data/pred.txt data/output.txt -w | grep -i "<" | wc -l

best:
	python run.py -src data/output.txt -tar data/perf.txt -tm 2

nis:
	python runN.py -src data/input.txt -tar data/pred.txt -tm 2
	diff data/pred.txt data/output.txt -w | grep -i "<" | wc -l

keke: 
	python runN.py -src testcases/input2.txt -tar testcases/pred2.txt -tm 2
	diff testcases/pred2.txt data/corpus.txt -w | grep -i "<" | wc -l
