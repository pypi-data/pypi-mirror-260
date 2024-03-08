from unittest.mock import MagicMock, patch

import pytest
from takeoff_client import TakeoffClient, TakeoffError
import responses


class TestTakeoffClient:
    def test_initialization_default(self):
        client = TakeoffClient()
        assert client.base_url == "http://localhost"
        assert client.port == 3000
        assert client.mgmt_port == 3001
        assert client.url == "http://localhost:3000"
        assert client.mgmt_url == "http://localhost:3001"

    def test_initialization_custom(self):
        # test that mgmt_port is set to port + 1
        client = TakeoffClient("http://test", 9000)
        assert client.base_url == "http://test"
        assert client.port == 9000
        assert client.mgmt_port == 9001
        assert client.url == "http://test:9000"
        assert client.mgmt_url == "http://test:9001"

    def test_initalization_custom_mgmt_port(self):
        client = TakeoffClient("http://test", 9000, 9005)
        assert client.base_url == "http://test"
        assert client.port == 9000
        assert client.mgmt_port == 9005
        assert client.url == "http://test:9000"
        assert client.mgmt_url == "http://test:9005"

    def test_get_readers(self):
        mock_response = {
            "primary": [
                {
                    "reader_id": "test",
                    "backend": "test",
                    "model_name": "test",
                    "model_type": "test",
                    "pids": [0],
                    "ready": True,
                }
            ]
        }

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_response

            client = TakeoffClient()
            response = client.get_readers()

            mock_get.assert_called_once_with("http://localhost:3001/reader_groups")
            assert response == mock_response

    def test_embed(self):
        mock_response = {"text": ["embedded text"]}

        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.status_code = 200

            client = TakeoffClient()
            response = client.embed("text to embed")

            mock_post.assert_called_once()
            assert response == mock_response

            # Test that an Exception is raised when the status code is not 200
            mock_post.return_value.status_code = 400
            mock_post.return_value.text = "Error message"

            with pytest.raises(Exception) as e:
                client.embed("text to embed")

            assert str(e.value) == "Embedding failed\nStatus code: 400\nResponse: Error message"

    def test_generate(self):
        mock_response = {"text": "generated text"}

        with patch("requests.post") as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.status_code = 200

            client = TakeoffClient()
            response = client.generate("text to generate")

            mock_post.assert_called_once()
            assert response == mock_response

            # Test that an Exception is raised when the status code is not 200
            mock_post.return_value.status_code = 400
            mock_post.return_value.text = "Error message"

            with pytest.raises(Exception) as e:
                client.generate("text to generate")

            assert str(e.value) == "Generation failed\nStatus code: 400\nResponse: Error message"

    @pytest.fixture
    def mock_response(self):
        # Mocking a requests.Response object
        mock_response = MagicMock()
        mock_response.status_code = 200

        def printer(x):
            print(x)
            return x

        alist = [b"data: Generated text 1\n\n", b"data: Generated text 2\n\n"]

        mock_response.__iter__.return_value = (printer(x) for x in alist)
        return mock_response

    def test_generate_stream_success(self, mock_response):
        # Setup
        text = "test text"
        url = "http://example.com/generate_stream"

        # Patching requests.post to return the mock_response
        with patch("requests.post", return_value=mock_response) as mock_post:
            instance = TakeoffClient()
            instance.url = "http://example.com"

            # Action
            result_generator = instance.generate_stream(text)
            result = list(result_generator)

            # Assert
            mock_post.assert_called_once_with(
                url=url,
                json={
                    "text": text,
                    "sampling_temperature": None,
                    "sampling_topp": None,
                    "sampling_topk": None,
                    "repetition_penalty": None,
                    "no_repeat_ngram_size": None,
                    "max_new_tokens": None,
                    "min_new_tokens": None,
                    "regex_string": None,
                    "json_schema": None,
                    "prompt_max_tokens": None,
                    "consumer_group": "primary",
                },
                stream=True,
            )

            print(result)
            assert len(result) == 2
            assert result[0].data == "Generated text 1"
            assert result[1].data == "Generated text 2"

    def test_generate_stream_failure(self, mock_response):
        # Setup for failure scenario
        mock_response.status_code = 400
        mock_response.text = "Error message"
        text = "test text"

        with patch("requests.post", return_value=mock_response):
            instance = TakeoffClient()
            instance.url = "http://example.com"

            # Assert exception is raised on failure
            with pytest.raises(Exception) as excinfo:
                _ = list(instance.generate_stream(text))

            assert "Generation failed" in str(excinfo.value)


    @responses.activate
    def test_create_reader(self):
        responses.add(
            responses.POST,
            "http://localhost:3001/reader",
            json={"reader_id": "test"},
            status=201,
        )

        client = TakeoffClient()
        response = client.create_reader({"model_name": "test", "device": "cuda"})

        assert response == {"reader_id": "test"}
    
    @responses.activate
    def test_reader_create_failure(self):
        responses.add(
            responses.POST,
            "http://localhost:3001/reader",
            status=400,
        )

        client = TakeoffClient()
        with pytest.raises(TakeoffError) as e:
            client.create_reader({"model_name": "test", "device": "cuda"})

        assert str(e.value) == "Reader creation failed\nStatus code: 400\nResponse: "
        
    @responses.activate
    def test_reader_create_failure_bad_device(self):
        client = TakeoffClient()
        # No device specified
        with pytest.raises(TakeoffError) as e:
            client.create_reader({"model_name": "test", "device": "mars"})
        assert "device" in str(e.value)
        # Wrong device
        with pytest.raises(TakeoffError) as e:
            client.create_reader({"model_name": "test"})
        assert "device" in str(e.value)

    @responses.activate
    def test_reader_create_failure_bad_model_name(self):
        client = TakeoffClient()
        # No model specified
        with pytest.raises(TakeoffError) as e:
            client.create_reader({"device": "mars"})
        assert "model_name" in str(e.value)
        # Empty model string
        with pytest.raises(TakeoffError) as e:
            client.create_reader({"model_name": ""})
        assert "model_name" in str(e.value)
        
    @responses.activate
    def test_reader_delete(self):
        responses.add(
            responses.DELETE,
            "http://localhost:3001/reader/test",
            status=204,
        )

        client = TakeoffClient()
        response = client.delete_reader("test")

        assert response == None
    
    @responses.activate
    def test_reader_delete_failure(self):
        responses.add(
            responses.DELETE,
            "http://localhost:3001/reader/test",
            status=404,
        )

        client = TakeoffClient()
        with pytest.raises(TakeoffError) as e:
            client.delete_reader("test")

        assert str(e.value) == "Reader deletion failed\nStatus code: 404\nResponse: "
        
    @responses.activate
    def test_list_reader_groups(self):
        responses.add(
            responses.GET,
            "http://localhost:3001/reader_groups",
            json={"primary": {"reader_id": "test"}},
            status=200,
        )

        client = TakeoffClient()
        response = client.list_all_readers()

        assert response == {"primary": {"reader_id": "test"}}
    
    @responses.activate
    def test_list_reader_groups_failure(self):
        responses.add(
            responses.GET,
            "http://localhost:3001/reader_groups",
            status=404,
        )

        client = TakeoffClient()
        with pytest.raises(TakeoffError) as e:
            client.list_all_readers()

        assert str(e.value) == "Reader listing failed\nStatus code: 404\nResponse: "
    
    @responses.activate
    def test_get_reader_config(self):
        responses.add(
            responses.GET,
            "http://localhost:3001/config/test",
            json={"reader_id": "test"},
            status=200,
        )

        client = TakeoffClient()
        response = client.get_reader_config("test")

        assert response == {"reader_id": "test"}
        
    @responses.activate
    def test_get_reader_config_failure(self):
        responses.add(
            responses.GET,
            "http://localhost:3001/config/test",
            status=404,
        )

        client = TakeoffClient()
        with pytest.raises(TakeoffError) as e:
            client.get_reader_config("test")

        assert str(e.value) == "Reader config retrieval failed\nStatus code: 404\nResponse: "