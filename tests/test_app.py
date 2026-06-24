import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Arrange-Act-Assert: Verify endpoint returns all activities."""
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Tennis Club", "Art Studio", "Music Ensemble", "Debate Team", "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == len(expected_activities)
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """Arrange-Act-Assert: Verify response structure has required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Missing '{field}' in {activity_name}"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success(self, client, reset_activities):
        """Arrange-Act-Assert: Student successfully signs up for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_returns_404_when_activity_not_found(self, client, reset_activities):
        """Arrange-Act-Assert: Signup fails with 404 for non-existent activity."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_returns_400_when_student_already_signed_up(self, client, reset_activities):
        """Arrange-Act-Assert: Duplicate signup prevented with 400 error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_success(self, client, reset_activities):
        """Arrange-Act-Assert: Student successfully unregisters from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_returns_404_when_activity_not_found(self, client, reset_activities):
        """Arrange-Act-Assert: Unregister fails with 404 for non-existent activity."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_returns_404_when_participant_not_found(self, client, reset_activities):
        """Arrange-Act-Assert: Unregister fails with 404 when student not in activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "unknown@mergington.edu"  # Not a participant
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]
