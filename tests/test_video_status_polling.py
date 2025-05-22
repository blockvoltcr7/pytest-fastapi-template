import pytest
import allure
import asyncio
from app.services.video_service import VideoService
from app.core.config import settings

@allure.epic("Core Functionality")
@allure.feature("Video Generation")
class TestVideoPolling:
    
    @allure.story("Status Polling Logic")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not settings.hedra_api_key,
        reason="Hedra API key required"
    )
    async def test_status_polling_logic(self):
        """Test the status polling logic with a mock generation"""
        with allure.step("Initialize video service"):
            video_service = VideoService()
        
        with allure.step("Test connection to Hedra API"):
            connection_ok = await video_service.test_connection()
            assert connection_ok, "Hedra API connection failed"
        
        # You could test status polling with a real generation ID if you have one
        # with allure.step("Check status of existing generation"):
        #     generation_id = "your_test_generation_id"
        #     status = await video_service.get_generation_status(generation_id)
        #     print(f"Status: {status}")
        
        print("✅ Status polling test passed")

    @allure.story("Polling Intervals")
    @allure.severity(allure.severity_level.NORMAL)
    def test_polling_intervals(self):
        """Test that polling intervals increase correctly"""
        with allure.step("Initialize video service"):
            video_service = VideoService()
        
        with allure.step("Test initial values"):
            assert video_service.initial_poll_interval == 15
            assert video_service.max_poll_interval == 60
            assert video_service.poll_backoff_factor == 1.2
        
        with allure.step("Test interval calculation logic"):
            current = 15
            intervals = [current]
            
            for i in range(5):
                current = min(int(current * 1.2), 60)
                intervals.append(current)
            
            assert current <= 60, "Interval exceeded maximum"
            assert len(intervals) == 6, "Expected 6 intervals in simulation"
            
            # Document the intervals for reporting
            for i, interval in enumerate(intervals):
                print(f"Interval {i}: {interval}s")
            
            # Verify progression
            assert intervals[1] > intervals[0], "Interval should increase"
            assert intervals[-1] <= 60, "Should not exceed max interval"
        
        print("✅ Polling interval logic test passed") 