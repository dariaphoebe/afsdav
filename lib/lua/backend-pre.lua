lighty.env['uri.scheme'] = 'https'
if lighty.env['request.method'] == 'DELETE' then
    lighty.header['Content-Length'] = '0'
end
