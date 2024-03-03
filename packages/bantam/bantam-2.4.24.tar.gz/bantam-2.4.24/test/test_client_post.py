import asyncio
from asyncio import CancelledError
from contextlib import suppress
from pathlib import Path
import sys
if True:
    sys.path.insert(0, str(Path(__file__).parent / 'example'))
from pathlib import Path

import pytest
from bantam.http import WebApplication
from class_rest_post import RestAPIExampleAsyncPostInterface, RestAPIExampleAsyncPost

PORT = 8240


@pytest.mark.asyncio
async def test_client_class_method(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()
        client = client[f'http://localhost:{PORT}/']
        response = await client.api_post_basic(1, 2, 4, 5, 6, param1=42, param2=True, param3=992.123)
        assert response == f"Response to test_api_basic 1.0 2"
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task


@pytest.mark.asyncio
async def test_client_constructor(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()[f'http://localhost:{PORT}/']
        response = await client.explicit_constructor(42)
        assert response.self_id is not None
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task


@pytest.mark.asyncio
async def test_client_instance_method(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        Client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()[f'http://localhost:{PORT}/']
        instance = await Client.explicit_constructor(4242)
        response = await instance.my_value()
        assert response == 4242
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task


@pytest.mark.asyncio
async def test_client_class_method_streamed(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()[f'http://localhost:{PORT}/']
        count = 0
        async for item in client.api_post_stream(42, True, 992.123, "They're here..."):
            assert item == count
            count += 1
        assert count == 10
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task


@pytest.mark.asyncio
async def test_client_instance_method_streamed(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        Client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()[f'http://localhost:{PORT}/']
        instance = await Client.explicit_constructor(29)
        count = 0
        async for item in instance.my_value_repeated(200):
            assert item == 29
            count += 1
        assert count == 200
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task


@pytest.mark.asyncio
async def test_client_instance_method_streamed_str(tmpdir):
    app = WebApplication(static_path=Path(tmpdir), js_bundle_name='generated', using_async=False)
    task = asyncio.create_task(app.start(host='localhost', port=PORT, modules=['class_rest_post']))
    try:
        await asyncio.sleep(1)
        Client = RestAPIExampleAsyncPostInterface.ClientEndpointMapping()[f'http://localhost:{PORT}/']
        instance = await Client.explicit_constructor(29)
        count = 0
        async for item in instance.my_value_repeated_string(200):
            assert item == str(29)*65537
            count += 1
            if count == 121:
                break  # disconnects client
        await asyncio.sleep(1)  # give server time to process disconnect
        assert RestAPIExampleAsyncPost.disconnected
    finally:
        task.cancel()
        with suppress(CancelledError):
            await task
