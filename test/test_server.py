# Tests to verify that the server used by the testing harness works
# correctly.
#
# You can specifically enable these tests by passing the --server-tests
# flag to pytest; this will disable the other tests.


from .utils import servertest


@servertest
async def test_index(client):
    response = await client.get("/enum/")
    assert response.status_code == 200
    assert response.json() == {"detail": "hello, world!"}


@servertest
async def test_redirect(client):
    response = await client.get("/enum/redirect")
    assert response.status_code == 307

    response = await client.get("/enum/redirect", follow_redirects=True)
    assert response.status_code == 200
    assert response.url.path == "/enum/"


@servertest
async def test_login(client, settings):
    # GET request should return Method Not Allowed
    response = await client.get("/auth/login")
    assert response.status_code == 405

    # POST request with correct login data should return a 200 response
    password = settings.auth_router_password()
    data = {"username": "admin", "password": password}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert response.json() == {"detail": "login succeeded"}

    # POST request with incorrect login data should return a 403 response
    data = {"username": "admin", "password": "incorrect password"}
    response = await client.post("/auth/login", json=data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


@servertest
async def test_get_user(client, settings):
    uid = settings.user_uid()

    # id parameter is required
    response = await client.get("/user/search")
    assert response.status_code == 422

    # Make a query for a user that exists
    response = await client.get(f"/user/search?uid={uid}")
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "uid": uid}

    # Make a query for a user that does not exist
    response = await client.get(f"/user/search?uid={10**10}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@servertest
async def test_get_ext_endpoints(settings, client):
    """Try to retrieve the .php and .html endpoint created by the extension testing router."""

    endpoint = settings.ext_router_endpoint()
    response = await client.get(f"/ext/{endpoint}.html")
    assert response.status_code == 200

    response = await client.get(f"/ext/{endpoint}.php")
    assert response.status_code == 200

    # Ensure that other endpoints return a 404 response
    response = await client.get("/ext/test")
    assert response.status_code == 404

    response = await client.get("/ext/invalid_test_endpoint.html")
    assert response.status_code == 404

    response = await client.get("/ext/invalid_test_endpoint.php")
    assert response.status_code == 404


@servertest
async def test_no_openapi(client):
    """By default, the OpenAPI configuration should not appear while running PyTest."""

    response = await client.get("/openapi.json")
    assert response.status_code == 404

    response = await client.get("/docs")
    assert response.status_code == 404
