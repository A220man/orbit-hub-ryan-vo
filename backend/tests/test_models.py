
import pytest
from httpx import AsyncClient, ASGITransport
import uuid

from app.main import app


@pytest.mark.asyncio
async def test_create_model():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/models",
            json={
                "name": "Test Model",
                "description": "A test model",
                "framework": "PyTorch",
                "version": "1.0.0",
                "metadata_json": '{"accuracy": 0.95}',
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Model"
        assert data["framework"] == "PyTorch"
        assert data["version"] == "1.0.0"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_model():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a model first
        create_resp = await client.post(
            "/api/v1/models",
            json={
                "name": "Get Test Model",
                "framework": "TensorFlow",
                "version": "2.0.0",
            },
        )
        model_id = create_resp.json()["id"]

        # Get the model
        response = await client.get(f"/api/v1/models/{model_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == model_id
        assert data["name"] == "Get Test Model"
        assert data["framework"] == "TensorFlow"


@pytest.mark.asyncio
async def test_get_model_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        fake_id = uuid.uuid4()
        response = await client.get(f"/api/v1/models/{fake_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_models():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a few models
        await client.post(
            "/api/v1/models",
            json={"name": "Model A", "framework": "PyTorch", "version": "1.0"},
        )
        await client.post(
            "/api/v1/models",
            json={"name": "Model B", "framework": "TensorFlow", "version": "2.0"},
        )

        response = await client.get("/api/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        assert len(data["items"]) >= 2
        assert data["page"] == 1
        assert data["page_size"] == 20


@pytest.mark.asyncio
async def test_list_models_pagination():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/models?page=1&page_size=1")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 1
        assert len(data["items"]) <= 1


@pytest.mark.asyncio
async def test_list_models_filter_by_name():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/models",
            json={"name": "SpecialModel", "framework": "PyTorch", "version": "1.0"},
        )
        await client.post(
            "/api/v1/models",
            json={"name": "OtherModel", "framework": "PyTorch", "version": "1.0"},
        )

        response = await client.get("/api/v1/models?name=Special")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        for item in data["items"]:
            assert "Special" in item["name"]


@pytest.mark.asyncio
async def test_list_models_filter_by_framework():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/models?framework=PyTorch")
        assert response.status_code == 200
        data = response.json()
        for item in data["items"]:
            assert item["framework"] == "PyTorch"


@pytest.mark.asyncio
async def test_update_model():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a model
        create_resp = await client.post(
            "/api/v1/models",
            json={"name": "Original", "framework": "PyTorch", "version": "1.0"},
        )
        model_id = create_resp.json()["id"]

        # Update the model
        response = await client.patch(
            f"/api/v1/models/{model_id}",
            json={"name": "Updated", "version": "2.0"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == model_id
        assert data["name"] == "Updated"
        assert data["version"] == "2.0"
        assert data["framework"] == "PyTorch"  # unchanged


@pytest.mark.asyncio
async def test_update_model_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        fake_id = uuid.uuid4()
        response = await client.patch(
            f"/api/v1/models/{fake_id}",
            json={"name": "Updated"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_model():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Create a model
        create_resp = await client.post(
            "/api/v1/models",
            json={"name": "ToDelete", "framework": "PyTorch", "version": "1.0"},
        )
        model_id = create_resp.json()["id"]

        # Delete the model
        response = await client.delete(f"/api/v1/models/{model_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_resp = await client.get(f"/api/v1/models/{model_id}")
        assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_model_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        fake_id = uuid.uuid4()
        response = await client.delete(f"/api/v1/models/{fake_id}")
        assert response.status_code == 404
