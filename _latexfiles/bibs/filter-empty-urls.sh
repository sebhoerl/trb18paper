for f in *.bib; do
	egrep -i -v "^ *url *= *\{\}(?:|,)$" $f > $f.tmp
	mv $f.tmp $f
done

