
wecho "
	# Convert input to Json format
	cat ./data/test.input.txt
	| python3 ./LocusZoomJson.py
	> data/test.json

	# Render json file to HTML format.
    !! python3 ./LocusZoomJSON2HTML.py
        -r 4:147901190-148901190
        -j data/test.json
        -t TEST
    > test.html

    # Render a stack of images together.
    !! python3 ./LocusZoomJSON2HTML.py
        -r 16:74942344-75942030
        -j 'data/json.CAD-16-75442143.json,./data/json.MIG-16-75442143.json,./data/json.SCZ-16-75442143.json'
        -t CAD,MIG,SCZ
    > stack.html
"
