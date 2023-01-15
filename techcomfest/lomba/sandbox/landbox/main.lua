-- Sandbox 1.0
-- Author: aimardcr

os.execute = function() 
    print('No! bad function!')
end

io.popen = function()
    print('No! bad function!')
end

print('Welcome to LUA Sandbox!')
print('Feel free to type your lua code below, type \'-- END\' once you are done ;)')
print('-- BEGIN')

local code = ''
while true
do
    local input = io.read()
    if input == '-- END' then
        break
    end

    code = code .. input .. '\n'
end

print()

print('-- OUTPUT BEGIN')
pcall(load(code))
print('-- OUTPUT END')