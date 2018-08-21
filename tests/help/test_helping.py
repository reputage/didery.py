# import pytest
# import falcon
# import asyncio
# import aiohttp
# from asyncio import ensure_future
# import arrow
#
# try:
#     import simplejson as json
# except ImportError:
#     import json
#
# from ioflo.aio.http import httping
# from ioflo.aio.http.httping import HTTPError
# from ioflo.aio.http import Valet
#
# # from didery import routing
#
# from pydidery.help import helping as h
# from pydidery.lib import generating as gen
#
#
# async def helper():
#     async with aiohttp.ClientSession() as session:
#         async with session.get("http://localhost:8080/history") as response:
#             data = await response.text()
#             # print(data)
#             return data
#
#
# async def httpPost(url, data, headers):
#     async with aiohttp.ClientSession(json_serialize=json.dumps) as session:
#         async with session.post(url, data=data, headers=headers) as response:
#             status = response.status
#             data = await response.text()
#
#             return status, data
#
#
# def patronHelper(method="GET", host="localhost", port=8080, path="history", headers=None, data=None, body=b''):
#     result = yield from h.httpRequest(method, host=host, port=port, path=path, headers=headers, data=data, body=body)
#
#     return result['body'].decode(), result['status']
#
#
# def testHttpRequest():
#     history, vk, sk, pvk, psk = gen.historyGen()
#     history['changed'] = str(arrow.utcnow())
#     body = json.dumps(history, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
#     url = "http://localhost:8080/history/"
#     headers = {
#         "Signature": 'signer="{0}"'.format(gen.signResource(body, gen.key64uToKey(sk)))
#     }
#
#     loop = asyncio.get_event_loop()
#     test = loop.run_until_complete(httpPost(url, body, headers))
#
#     print(test)
#
#     loop = asyncio.get_event_loop()
#     test = loop.run_until_complete(helper())
#
#     print(test)
#
#     assert True
#
#
# def handleAsync(f):
#     response = f()
#
#     while True:
#         try:
#             next(response)
#         except StopIteration as si:
#             return si.value
#
#
# def testPatron():
#     # app = falcon.API(middleware=[routing.CORSMiddleware()])
#     # routing.loadEndPoints(app, store=self.store)
#     #
#     # valet = Valet(
#     #     port=port,
#     #     bufsize=131072,
#     #     wlog=None,
#     #     store=self.store,
#     #     app=app,
#     #     timeout=0.5,
#     # )
#
#     # get all histories
#     response = patronHelper()
#
#     while True:
#         try:
#             next(response)
#         except StopIteration as si:
#             # print("Final: " + si.value)
#             break
#
#     # create a history
#     history, vk, sk, pvk, psk = gen.historyGen()
#     history['changed'] = str(arrow.utcnow())
#     body = json.dumps(history, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
#     did = history['id']
#     path = "history/"
#     headers = {
#         "Signature": 'signer="{0}"'.format(gen.signResource(body, gen.key64uToKey(sk)))
#     }
#
#     response = patronHelper("POST", path=path, data=history, headers=headers)
#
#     while True:
#         try:
#             next(response)
#         except StopIteration as si:
#             # print("Final: " + str(si))
#             break
#         except HTTPError as er:
#             # print(er.detail)
#             pass
#
#     # get a single history
#     path = "history/" + did
#
#     response = patronHelper(path=path)
#
#     while True:
#         try:
#             next(response)
#         except StopIteration as si:
#             print("Final: " + str(si.value))
#             break
#
#     ppvk, ppsk = gen.keyGen()
#     history['changed'] = str(arrow.utcnow())
#     history['signer'] = 1
#     history['signers'].append(ppvk)
#     body = json.dumps(history, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
#
#     headers = {
#         "Signature": 'signer="{0}"; rotation="{1}"'.format(
#             gen.signResource(body, gen.key64uToKey(sk)),
#             gen.signResource(body, gen.key64uToKey(psk))
#         )
#     }
#
#     response = patronHelper("PUT", path=path, data=history, headers=headers)
#
#     while True:
#         try:
#             next(response)
#         except StopIteration as si:
#             print("Final: " + str(si.value))
#             break
#
#     assert True
#
#
# b'{"id":"did:dad:QyAd0Clia3M8G-KccE-X1t4-OklUkAz7ieXhF5zFbhQ=","signer":1,"signers":["QyAd0Clia3M8G-KccE-X1t4-OklUkAz7ieXhF5zFbhQ=","Mb1bxpjJJy6Dw9mNFvX7FnjMF6vgEDGJkMbLgQUufP8=","mJZOsbpKBm_dKGLIfygdLTOaarYycrmFui-kZ4jbyAc="],"changed":"2018-06-22T23:23:00.630020+00:00"}'
# b'{"id":"did:dad:QyAd0Clia3M8G-KccE-X1t4-OklUkAz7ieXhF5zFbhQ=","signer":1,"signers":["QyAd0Clia3M8G-KccE-X1t4-OklUkAz7ieXhF5zFbhQ=","Mb1bxpjJJy6Dw9mNFvX7FnjMF6vgEDGJkMbLgQUufP8=","mJZOsbpKBm_dKGLIfygdLTOaarYycrmFui-kZ4jbyAc="],"changed":"2018-06-22T23:23:00.630020+00:00"}'
