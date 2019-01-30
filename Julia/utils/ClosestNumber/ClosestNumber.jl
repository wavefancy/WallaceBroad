
doc = """Find the closest number from a list of numbers.

Usage:
    ClosestNumber.jl -f file -c int [-t type] [-g int]
    ClosestNumber.jl -h | --help | --version

Notes:
    1. Read data from stdin, add one more column for the closest number found in the -f file list.
    2. -f one column for the numbers to search.

Options:
    -c int        Column index for data from stdin to compare with, starts from 1.
    -f file       File contains the list of numbers to search.
    -g int        Check the closest number in sub-group. Column index in stdin for group name.
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
TYPE        = args["-t"] == nothing ? "Int" : args["-t"]
G_INDEX     = args["-g"] == nothing ? -1  : parse(Int, args["-g"])

# println(TYPE)
# D_TYPE = nothing
if TYPE == "Int"
    D_TYPE = Int
elseif TYPE == "Float64"
    D_TYPE = Float64
else
    println(stderr, "Please set a proper value for -t, Int|Float64")
    exit(-1)
end
# println(D_TYPE)

dict = Dict{String,Array}()
open(NUM_FILE) do file
    for ln in eachline(file)
        # println(ln)
        ss = split(chomp(ln))
        # println(ss)
        if G_INDEX >0
            x = tryparse(D_TYPE, ss[2])
        else
            x = tryparse(D_TYPE, ss[1])
        end
        # println("OK")
        if x != nothing
            g  = G_INDEX > 0 ? ss[1] : "G"
            if haskey(dict, g) == false
                dict[g] = Vector{D_TYPE}([])
            end
            push!(dict[g],x)
        end
    end
end
[sort!(dict[k]) for k in keys(dict)]
# println(dict)

#read data from stdin
# read and streaming https://docs.julialang.org/en/v1/manual/networking-and-streams/index.html
for line in eachline(stdin)
    ss = split(chomp(line))
    # print(ss[COL_INDEX])
    x = tryparse(D_TYPE, ss[COL_INDEX])
    g  = G_INDEX > 0 ? ss[G_INDEX] : "G"

    # print(x)
    if x == nothing || haskey(dict, g)==false
        println(join(vcat(ss, "FAIL"), "\t"))
    else
        vals = dict[g]
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
