### Example pipeline to create locus zoom plot.

- Convert txt file to JSON file
- Convert json file to html
- Start a http server to view the plot


#### INPUT txt file format.
Five columns: `CHR POS REF ALT P`

The reference genome version is hg19. The LD information will be fetched by `lcuszoom.appp.js` from its server.
```
4       148899082       A       G       0.474504
4       148900111       T       C       0.527509
4       148900991       G       A       0.380765
4       148901044       C       T       0.696744
```

#### Follow below scripts to generate an example
Please install missing packages if error happened for some missing package from python. 
Any other files were self-contained in this example folder.
~~~
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
~~~

#### Start a http server from this example folder
```
python3 -m http.server
```

The end, the plot will render in the browser.
