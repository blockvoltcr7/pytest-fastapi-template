import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestContentCrewAPI:
    """Test suite for Content Crew API endpoints using FastAPI TestClient"""

    @pytest.mark.smoke
    def test_content_creation_endpoint(self):
        """Test the main content creation endpoint"""
        payload = {
            "content_ideas": [
                {
                    "topic": "AI Tools for Small Business",
                    "content_type": "blog post",
                    "industry": "technology",
                    "target_audience": "small business owners",
                    "keywords": ["AI", "small business", "automation"]
                }
            ],
            "google_sheet_row": {
                "row_id": 1,
                "source": "test_api"
            }
        }

        response = client.post("/api/v1/content/create", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "processed_ideas" in data
        assert "processing_time" in data
        assert "errors" in data

        assert len(data["processed_ideas"]) == 1
        assert data["processed_ideas"][0]["original_idea"]["topic"] == "AI Tools for Small Business"

    def test_content_creation_multiple_ideas(self):
        """Test content creation with multiple ideas"""
        payload = {
            "content_ideas": [
                {
                    "topic": "Digital Marketing Trends",
                    "content_type": "article",
                    "industry": "marketing"
                },
                {
                    "topic": "Remote Work Best Practices",
                    "content_type": "blog post",
                    "industry": "business"
                }
            ]
        }

        response = client.post("/api/v1/content/create", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert len(data["processed_ideas"]) == 2
        assert data["status"] in ["success", "partial_success"]

    @pytest.mark.smoke
    def test_health_check_endpoint(self):
        """Test content service health check"""
        response = client.get("/api/v1/content/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "service" in data
        assert "tools_available" in data
        assert "agents_count" in data
        assert "timestamp" in data

        assert data["service"] == "content_creation_crew"
        assert data["agents_count"] == 4
        assert data["status"] in ["healthy", "unhealthy"]

class TestContentCrewAPIValidation:
    """Test API validation and error handling"""

    def test_invalid_content_creation_request(self):
        """Test content creation with invalid request"""
        # Missing required fields
        payload = {
            "content_ideas": []  # Empty ideas array
        }

        response = client.post("/api/v1/content/create", json=payload)

        # Should handle gracefully - might return 200 with empty results or 422 for validation
        assert response.status_code in [200, 422]

    def test_malformed_content_idea(self):
        """Test with malformed content idea"""
        payload = {
            "content_ideas": [
                {
                    # Missing topic field
                    "content_type": "blog post"
                }
            ]
        }

        response = client.post("/api/v1/content/create", json=payload)

        # Should return validation error
        assert response.status_code == 422


    def test_content_creation_with_invalid_json(self):
        """Test content creation with completely invalid JSON"""
        response = client.post(
            "/api/v1/content/create",
            data="invalid json content",
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422

class TestContentCrewAPIEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_large_number_of_content_ideas(self):
        """Test with a large number of content ideas"""
        content_ideas = [
            {
                "topic": f"Topic {i}",
                "content_type": "blog post",
                "industry": "technology"
            }
            for i in range(10)  # 10 ideas
        ]

        payload = {"content_ideas": content_ideas}

        response = client.post("/api/v1/content/create", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert len(data["processed_ideas"]) == 10
        assert data["status"] in ["success", "partial_success"]

    def test_content_idea_with_all_optional_fields(self):
        """Test content creation with all optional fields populated"""
        payload = {
            "content_ideas": [
                {
                    "topic": "Comprehensive Content Test",
                    "content_type": "whitepaper",
                    "industry": "fintech",
                    "target_audience": "financial advisors and wealth managers",
                    "competitors": [
                        "competitor1.com",
                        "competitor2.com",
                        "competitor3.com"
                    ],
                    "publish_date": "2024-06-15",
                    "campaign_duration": "3 months",
                    "word_count": "3000-5000",
                    "keywords": [
                        "fintech",
                        "wealth management",
                        "digital transformation",
                        "financial planning",
                        "robo advisors"
                    ]
                }
            ],
            "google_sheet_row": {
                "row_id": 42,
                "source": "google_sheets",
                "campaign_name": "Q2 Content Campaign",
                "assignee": "content_team@company.com"
            }
        }

        response = client.post("/api/v1/content/create", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        processed_idea = data["processed_ideas"][0]

        assert processed_idea["original_idea"]["topic"] == "Comprehensive Content Test"
        assert processed_idea["original_idea"]["content_type"] == "whitepaper"
        assert len(processed_idea["original_idea"]["keywords"]) == 5
        assert len(processed_idea["original_idea"]["competitors"]) == 3


    def test_concurrent_api_requests(self):
        """Test handling of concurrent API requests"""
        import threading
        import time

        results = []

        def make_request(topic_suffix):
            payload = {
                "content_ideas": [
                    {
                        "topic": f"Concurrent Test {topic_suffix}",
                        "content_type": "blog post",
                        "industry": "technology"
                    }
                ]
            }

            response = client.post("/api/v1/content/create", json=payload)
            results.append(response.status_code)

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5

class TestContentCrewAPIPerformance:
    """Test performance characteristics of the API"""

    def test_response_time_single_idea(self):
        """Test response time for single content idea"""
        import time

        payload = {
            "content_ideas": [
                {
                    "topic": "Performance Test",
                    "content_type": "blog post",
                    "industry": "technology"
                }
            ]
        }

        start_time = time.time()
        response = client.post("/api/v1/content/create", json=payload)
        end_time = time.time()

        assert response.status_code == 200

        response_time = end_time - start_time
        # API should respond within reasonable time (adjust as needed)
        assert response_time < 120  # 2 minutes max for single idea

        # Verify processing time is included in response
        data = response.json()
        assert "processing_time" in data
        assert isinstance(data["processing_time"], (int, float))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
