local auth = lighty.request['Authorization'] or ''
local cache = lighty.req_env['DAV_BASE']..'/run/cache/'
local user = lighty.env['request.user'] or ''
user = string.gsub(user, '@MIT.EDU', '@ATHENA.MIT.EDU')
if #user > 0 then
    lighty.env["request.user"] = user
end

if #auth > 0 and auth:sub(1,6) == 'Basic ' then
    local key = cache .. auth:sub(7)
    f = io.open(key)
    if f then
        d = f:read()
        if d and #d > 0 then
            lighty.env['request.user'] = d
        end
    end
end
