"""Tests for Flask application."""

import pytest
import os
from app import app
from docx import Document
from docx.shared import Pt


@pytest.fixture
def client():
    """Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_docx(tmp_path):
    """Create a test Word document."""
    doc = Document()
    doc.add_paragraph("测试内容")

    path = str(tmp_path / "test.docx")
    doc.save(path)
    return path


def test_index_loads(client):
    """Test that index page loads."""
    response = client.get('/')
    assert response.status_code == 200


def test_format_endpoint_without_file(client):
    """Test /format endpoint with no file returns error."""
    response = client.post('/format')
    assert response.status_code == 400


def test_format_endpoint_with_invalid_file(client):
    """Test /format endpoint with non-docx file returns error."""
    data = {'file': (b'not a docx', 'test.txt')}
    response = client.post('/format', data=data, content_type='multipart/form-data')
    assert response.status_code == 400


def test_format_endpoint_success(client, sample_docx):
    """Test /format endpoint with valid docx returns formatted file."""
    with open(sample_docx, 'rb') as f:
        data = {'file': f}
        response = client.post('/format', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    # Response should be docx file
    assert response.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
