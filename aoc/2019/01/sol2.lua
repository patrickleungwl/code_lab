function get_input(file)
    input = {}
    for tmp in io.lines(file) do 
        input[#input+1] = tmp
    end
    return input
end


function get_fuel(mass)
    m = math.floor(mass/3.0)-2
    return m
end

function get_total_fuel_requirements(input)
    total = 0
    module = 0
    for k,v in pairs(input) do
        t = get_fuel(tonumber(v))
        total = total + t
        print(module..' '..v..' requires '..t )
        while true do
            t = get_fuel(t)
            if t<=0 then
                break
            end
            total = total + t
            print(' '..t..'->'..total )
        end
        module = module + 1
    end
    return total
end


assert(get_fuel(12)==2)
assert(get_fuel(14)==2)
assert(get_fuel(1969)==654)
assert(get_fuel(100756)==33583)


input = get_input(arg[1])
total = get_total_fuel_requirements(input)
print(total)

