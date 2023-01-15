-- Sandbox 2.0
-- Author: aimardcr

local env = {
    print=print,
    io = {
        read=io.read, 
        write=io.write, 
    },
    _G = _G
}

function run(untrusted_code)
    local untrusted_function, message = load(untrusted_code, nil, 't', env)
    if not untrusted_function then 
        return nil, message 
    end
    return pcall(untrusted_function)
end

print('Welcome to LUA Sandbox 2.0!')
print('Feel free to type your lua code below, type \'-- END\' once you are done ;)')
print('-- BEGIN')

local code = ''
while true
do
    local input = io.read()
    if input == '-- END' then
        break
    end

    allowed = true
    blacklist = {'os.execute', 'execute', 'io.popen', 'popen', 'package.loadlib', 'loadlib'}
    for i = 1, #blacklist do
        if string.find(input, blacklist[i]) then
            print('No! bad code!')
            allowed = false
            break
        end
    end

    if allowed then
        code = code .. input .. '\n'
    end
end

print()

print('-- OUTPUT BEGIN')
run(code)
print('-- OUTPUT END')