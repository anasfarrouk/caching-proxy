#!/usr/bin/env python3
import  argparse
import  asyncio
import  time
from    urllib.parse    import  urlparse

CACHE_TTL   =   300 #seconds
cache       =   {}  #{url: (timestamp,response_bytes)}

async   def build_parser():
    parser      =   argparse.ArgumentParser(prog='caching-proxy')
    subparser   =   parser.add_subparsers(dest='command',required=True)

    start       =   subparser.add_parser('start',help='start the proxy server')
    start.add_argument('--host',type=str,required=True)
    start.add_argument('--port',type=int,required=True)
    start.set_defaults(func=start_server)

    clear       =   subparser.add_parser('--clear-cache',help='clear the cache')
    clear.set_defaults(func=clear_cache)

    return  parser

async   def open_conn(host:str):
    u   =   urlparse(host)
    port    =   443 if  u.scheme    ==  'https' else    80
    return  await   asyncio.open_connection(u.hostname,port,ssl=(u.scheme=='https'))

async   def pipe(reader,writer):
    try:
        while   data    :=  await   reader.read(4096):
            write.write(data)
            await   write.drain()
    finally:
        writer.close()
        await   writer.wait_closed()

def add_cache_header(resp:bytes,hit:bool):
    header,_,body   =   resp.partition(b'\r\n\r\n')
    cache_line      =   b'X-Cache: HIT' if  hit else b'X-Cache: MISS'
    new_heaser      =   header + b'\r\n' + cache_line
    return  new_header + b'\r\n\r\n' + body

async   def handle_client(client_reader,client_writer,host):
    request =   await   client_reader.readuntil(b'\r\n\r\n')
    url     =   urlparse(host)

    now     =   time.time()
    cached  =   cache.get(url.geturl())

    if  cached  and now - cached[0] < CACHE_TTL:
        ts,data =   cached
        data    =   add_cached_header(data,hit=True)
        client_writer.write(data)
        await   cleint_writer.drain()
        client_writer.close()
        await   client_writer.wait_closed()
        return

    target_reader,target_writer =   await   open_conn(origin)

    target_writer.write(request)
    await   target_writer.drain()

    response_chunks =   []

    async   def collect(src_reader,dst_writer):
        try:
            while   chunk   :=  await   src_reader.read(4096):
                response_chunks.append(chunk)
                dst_writer.write(chunk)
                await   dst_writer.drain()
        finally:
            dst_writer.close()
            await   dst_writer.wait_closeed()

    await   asyncio.gather(
            collect(client_reader,target_writer),
            collect(target_reader,client_writer),
            )

    raw_response    =   b''.join(response_chunks)
    cache[url.geturl()] =   (now,raw_response)

async   def start_server(args):
    async   def client_cb(r,w):
        await   handle_client(r,w,args.host)

    server  =   await   asyncio.start_server(client_cb,'127.0.0.1',args.port)
    print(f'Caching proxy listening on 127.0.0.1:{args.port}')
    async   with    server:
        await   server.serve_forever()

async   def clear_cache(args):
    pass

async   def main(argv=None):
    parser  =   await   build_parser()
    args    =   parser.parse_args(argv)
    args.func(args)

if  __name__    ==  "__main__":
    asyncio.run(main())

