lighty.env['uri.scheme'] = 'https'
if lighty.env['request.method'] == 'DELETE'
or lighty.env['request.method'] == 'UNLOCK' then
    lighty.header['Content-Length'] = '0'
end
