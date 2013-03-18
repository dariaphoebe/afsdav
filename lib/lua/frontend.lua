local auth = lighty.request['Authorization'] or ''
local k5cc = lighty.req_env['KRB5CCNAME'] or ''
local user = lighty.env['request.user'] or ''
local cache = lighty.req_env['DAV_BASE']..'/run/cache/'

if #user > 0 then
    if #k5cc > 0 then
        os.execute('cp -a '..k5cc..' '..lighty.req_env['DAV_BASE']..'/run/'..user..'.k5')
        if #auth > 0 and auth:sub(1,6) == 'Basic ' then
            local key = cache .. auth:sub(7)
            f = io.open(key,'w')
            if f then
                f:write(user)
                f:close()
            end
        end
    end
end
lighty.request['Authorization'] = ''
