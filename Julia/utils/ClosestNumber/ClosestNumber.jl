
doc = """Find the closest number from a list of numbers.

Usage:
    ClosestNumber.jl -f file -c int [-t type]
    ClosestNumber.jl -h | --help | --version

Notes:
    1. Read data from stdin, add one more column for the closest number found in the -f file list.
    2. -f one column for the numbers to search.

Options:
    -c int        Column index for data from stdin to compare with, starts from 1.
    -f file       File contains the list of numbers to search.
    -t type       Input data type, default Int, Int|Float64
    -h --help     Show this screen.
    --version     Show version.
"""

using DelimitedFiles
using DocOpt

args = docopt(doc, version=v"1.0")
# println(args)
# println(args["-b"])
NUM_FILE    = args["-f"] # file name for reading numbers.
COL_INDEX   = parse(Int, args["-c"]) # genotyping matrx, sample by genotype.
D_TYPE      = args["-t"] == nothing ? Int : args["-t"]

vals = readdlm(NUM_FILE,'\t',D_TYPE,'\n')
vals = sort(vec(vals)) # convert to array and sort.
# println(vals)

#read data from stdin
# read and streaming https://docs.julialang.org/en/v1/manual/networking-and-streams/index.html
for line in eachline(stdin)
    ss = split(chomp(line))
    # print(ss[COL_INDEX])
    x = tryparse(D_TYPE, ss[COL_INDEX])
    # print(x)
    if x == nothing
        println(join(vcat(ss, "FAIL"), "\t"))
    else
        pos = searchsorted(vals, x)
        # print(repr(pos)*"---")
        # in reverse order if can not find the elements.
        n_stop = pos.stop <= 0 ? 1 : pos.stop
        n_start = pos.start > length(vals) ? length(vals) : pos.start

        if n_start == n_stop
            println(join(vcat(ss, repr(vals[n_stop])), "\t"))
        else
            # println(pos)
            if abs(vals[n_start] - x) < abs(vals[n_stop] -x)
                out = vals[n_start]
            else
                out = vals[n_stop]
            end
            println(join(vcat(ss, repr(out)), "\t"))
        end
    end
end
