using LinearAlgebra, Printf, PyCall, Random, ProgressMeter, Dates, BenchmarkTools, Logging, ArgParse
using CalculusWithJulia;
using HCubature;
using CSV, DataFrames;
import PyPlot;
import JSON;

const eps = 1e-8

raw"""Returns the value of the matrix element

```math
\braket{\alpha}{0}{\beta}
```

where
"""
function coherent_superposition(α::Complex{Float64}, β::Complex{Float64})
    return exp(-0.5*(abs(α)^2 + abs(β)^2 - 2 * conj(α) * β))
end


raw"""Computes the average state

```math
S = \frac{1}{N} \sum_{i = 1}^N \ketbra{\alpha_i}{\alpha_i}
```

"""
function get_S(αs::Array{Complex{Float64}})
    N = length(αs)
    S = zeros(Complex{Float64}, N, N)

    for i in 1:N
        for j in 1:N
            S[i, j] = coherent_superposition(αs[i], αs[j]) / N
        end
    end
    return S
end

function get_S12(αs::Array{Complex{Float64}})
    return get_S(αs)^(-1/2)
end


function get_ρ(αs::Array{Complex{Float64}}, idx::Int)
    N = length(αs)
    ret = zeros(Complex{Float64}, N, N)
    for i in 1:N
        ret[idx, i] = coherent_superposition(αs[idx], αs[i]) / N
    end
    return ret
end


function PGM_performance(αs::Array{Complex{Float64}})
    N = length(αs)
    for i in 1:N
        for j in i + 1:N
            α = αs[i]
            β = αs[j]
            if norm(α - β) < eps
                return 1. / 3
            end
        end
    end

    S12 = get_S12(αs)
    perf = 0.0
    for idx in 1:N
        ρ = get_ρ(αs, idx)
        outmat = S12 * ρ * S12 * ρ
        perf += tr(outmat)
    end
    ret = perf
    if norm(ret - real(ret)) > eps
        @error "Performance is not real" αs ret
    end
    if real(ret) < 0
        @error "Performance is kekked" αs ret
    end
    ret = norm(ret)
    if ret > 1
        @error "Performance is kekked" αs ret
    end
    return ret
end


function average_PGM_performance()
    f(rα, iα, rβ, iβ, rγ, iγ) = PGM_performance([rα + 1im*iα, rβ + 1im*iβ, rγ + 1im*iγ])
    f(v) = f(v...)

    integral = hcubature(f, (-1.0, -1.0, -1.0, -1.0, -1.0, -1.0), (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), rtol=1e-4)
    @info "Computed integral" integral

    @info "Result" integral ./ 2^6
end



function parse_cli()
    s = ArgParseSettings()
    @add_arg_table s begin
        "--test"
        help = "Run test suites"
        action = :store_true
    end

    return parse_args(s)
end


function test_overlap()

    tests = [
        Dict(
            "alpha" => 0.0 + 0im,
            "beta" => 0.0 + 0im,
            "expe" => 1.0,
        ),
        Dict(
            "alpha" => 10.0 + 0im,
            "beta" => 10.0 + 0im,
            "expe" => 1.0,
        ),
        Dict(
            "alpha" => 0.0 + 0im,
            "beta" => 1.0 + 0im,
            "expe" => 0.6065306597126334
        ),
        Dict(
            "alpha" => (3.0 + 4im)/5,
            "beta" => (-3.0 + 4im)/5,
            "expe" => exp(-18/25) * (cos(24/25) + 1im * sin(24/25)),
        ),
    ]
    for test in tests
        val = coherent_superposition(test["alpha"], test["beta"])
        if norm(val - test["expe"]) > eps
            @error "test overlap" test val
        end
    end
end

function test_S12()
    S = get_S12([0.0 + 0im])
    if length(S) != 1
        @error "Wrong dimension for S"
    end
    if norm(S[1, 1] - 1.0) > eps
        @error "Test S12" S
    end


    S = get_S12([0.0 + 0im, 100])
    if size(S) != (2, 2)
        @error "Wrong dimension for S" S length(S) size(S)
    end
    if norm(S - sqrt(2) .* [1.0 + 0im 0; 0 1]) > eps
        @error "Test S12" S
    end

    c = coherent_superposition(0.0 + 0im, 1.0 + 0im)
    S = get_S([0.0 + 0im, 1])
    expe = [.5 + 0im  c/2; conj(c)/2 .5]
    if norm(S - expe) > eps
        @error "Test S" S expe
    end

    S12 = get_S12([0.0 + 0im, 1])
    phase = sqrt(c/conj(c))
    appo1 = (sqrt(1 - abs(c)) + sqrt(1 + abs(c)))/sqrt(1 - abs(c)^2)
    appo2 = (sqrt(1 - abs(c)) - sqrt(1 + abs(c)))/sqrt(1 - abs(c)^2)

    expe = sqrt(0.5) .* [appo1 phase*appo2; conj(phase)*appo2 appo1]
    if norm(S12 - expe) > eps
        @error "Test S12" S12 expe
    end

    α = 0.5 + 0im
    ret = PGM_performance([α, α*exp(1im*2π/3), α*exp(-1im*2π/3)])
    if norm(ret -  0.731182) > 1e-5
        @error "PGM performance" α ret
    end

end

function test()
    test_overlap()
    test_S12()
end

function num_photons(αs::Array{Complex{Float64}}, num_ref)
	N = length(αs)
	res = 0
    for i in 1:N
       res += (num_ref+1/3)*norm(αs[i])^2
    end
	return res
end


function main(args)
    if args["test"]
        test()
        return
    end
    
    batchsize = 10000000
    alpha_bound = 0.75
    
    alpha = (2*alpha_bound).*rand(Complex{Float64}, batchsize, 3).-complex(alpha_bound, alpha_bound)
    
    resources_list = []
    error_prob_list = []
    column_names = ["Resources", "ProbError",]
    
    for i in 1:batchsize
    	push!(resources_list, num_photons(alpha[i, 1:3], 4))
    	push!(error_prob_list, 1.0-PGM_performance(alpha[i, 1:3]))
    end
    
    res_matrix = DataFrame(hcat(resources_list, error_prob_list), :auto)
    rename!(res_matrix, column_names)
    
    file_path = "/scratch/fbelliardo/pgm_results.csv"
    
    CSV.write(file_path, res_matrix)
end


if abspath(PROGRAM_FILE) == @__FILE__
    args = parse_cli()
    main(args)
end
