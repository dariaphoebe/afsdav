-- WebDAV/AFS Backend Handler
--

for i,k in pairs({'DAV_BASE','DAV_USERF'}) do
    if (_G[k] == nil) then
        _G[k] = os.getenv(k)
    end
end

function cgi_handler(script_name)
    lighty.env["physical.path"] = _G['DAV_BASE'] .. '/www/cgi/' .. script_name
end

if (lighty.env["request.method"] == "GET" or lighty.env["request.method"] == "POST") then
    uri_path = lighty.env['uri.path']
    if (string.sub(uri_path, -1) == '/') then
        attr = lighty.stat(lighty.env["physical.path"])
        if (attr and attr.is_dir) then
            cgi_handler('index')
        end
    elseif (string.sub(uri_path, 2, 7) == 'tokens') then
        lighty.content = {{ filename = _G['DAV_BASE'] .. '/run/' .. _G['DAV_USERF'] .. '.tok' }}
        return 200
    elseif (string.sub(uri_path, 2, 4) == 'fs_') then
        cgi_handler('fs')
    end
end
