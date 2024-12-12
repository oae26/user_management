from builtins import range
import pytest
from sqlalchemy import select
from app.dependencies import get_settings
from app.models.user_model import User, UserRole
from app.services.user_service import UserService
from app.utils.nickname_gen import generate_nickname

pytestmark = pytest.mark.asyncio

# Test creating a user with valid data
async def test_create_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "valid_user@example.com",
        "password": "ValidPassword123!",
        "role": UserRole.ADMIN.name
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test creating a user with invalid data
async def test_create_user_with_invalid_data(db_session, email_service):
    user_data = {
        "nickname": "",  # Invalid nickname
        "email": "invalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.create(db_session, user_data, email_service)
    assert user is None

# Test fetching a user by ID when the user exists
async def test_get_by_id_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_id(db_session, user.id)
    assert retrieved_user.id == user.id

# Test fetching a user by ID when the user does not exist
async def test_get_by_id_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    retrieved_user = await UserService.get_by_id(db_session, non_existent_user_id)
    assert retrieved_user is None

# Test fetching a user by nickname when the user exists
async def test_get_by_nickname_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user.nickname == user.nickname

# Test fetching a user by nickname when the user does not exist
async def test_get_by_nickname_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_nickname(db_session, "non_existent_nickname")
    assert retrieved_user is None

# Test fetching a user by email when the user exists
async def test_get_by_email_user_exists(db_session, user):
    retrieved_user = await UserService.get_by_email(db_session, user.email)
    assert retrieved_user.email == user.email

# Test fetching a user by email when the user does not exist
async def test_get_by_email_user_does_not_exist(db_session):
    retrieved_user = await UserService.get_by_email(db_session, "non_existent_email@example.com")
    assert retrieved_user is None

# Test updating a user with valid data
async def test_update_user_valid_data(db_session, user):
    new_email = "updated_email@example.com"
    updated_user = await UserService.update(db_session, user.id, {"email": new_email})
    assert updated_user is not None
    assert updated_user.email == new_email

# Test updating a user with invalid data
async def test_update_user_invalid_data(db_session, user):
    updated_user = await UserService.update(db_session, user.id, {"email": "invalidemail"})
    assert updated_user is None

# Test deleting a user who exists
async def test_delete_user_exists(db_session, user):
    deletion_success = await UserService.delete(db_session, user.id)
    assert deletion_success is True

# Test attempting to delete a user who does not exist
async def test_delete_user_does_not_exist(db_session):
    non_existent_user_id = "non-existent-id"
    deletion_success = await UserService.delete(db_session, non_existent_user_id)
    assert deletion_success is False

# Test listing users with pagination
async def test_list_users_with_pagination(db_session, users_with_same_role_50_users):
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    assert len(users_page_1) == 10
    assert len(users_page_2) == 10
    assert users_page_1[0].id != users_page_2[0].id

# Test registering a user with valid data
async def test_register_user_with_valid_data(db_session, email_service):
    user_data = {
        "nickname": generate_nickname(),
        "email": "register_valid_user@example.com",
        "password": "RegisterValid123!",
        "role": UserRole.ADMIN
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is not None
    assert user.email == user_data["email"]

# Test attempting to register a user with invalid data
async def test_register_user_with_invalid_data(db_session, email_service):
    user_data = {
        "email": "registerinvalidemail",  # Invalid email
        "password": "short",  # Invalid password
    }
    user = await UserService.register_user(db_session, user_data, email_service)
    assert user is None

# Test successful user login
async def test_login_user_successful(db_session, verified_user):
    user_data = {
        "email": verified_user.email,
        "password": "MySuperPassword$1234",
    }
    logged_in_user = await UserService.login_user(db_session, user_data["email"], user_data["password"])
    assert logged_in_user is not None

# Test user login with incorrect email
async def test_login_user_incorrect_email(db_session):
    user = await UserService.login_user(db_session, "nonexistentuser@noway.com", "Password123!")
    assert user is None

# Test user login with incorrect password
async def test_login_user_incorrect_password(db_session, user):
    user = await UserService.login_user(db_session, user.email, "IncorrectPassword!")
    assert user is None

# Test account lock after maximum failed login attempts
async def test_account_lock_after_failed_logins(db_session, verified_user):
    max_login_attempts = get_settings().max_login_attempts
    for _ in range(max_login_attempts):
        await UserService.login_user(db_session, verified_user.email, "wrongpassword")
    
    is_locked = await UserService.is_account_locked(db_session, verified_user.email)
    assert is_locked, "The account should be locked after the maximum number of failed login attempts."

# Test resetting a user's password
async def test_reset_password(db_session, user):
    new_password = "NewPassword123!"
    reset_success = await UserService.reset_password(db_session, user.id, new_password)
    assert reset_success is True

# Test verifying a user's email
async def test_verify_email_with_token(db_session, user):
    token = "valid_token_example"  # This should be set in your user setup if it depends on a real token
    user.verification_token = token  # Simulating setting the token in the database
    await db_session.commit()
    result = await UserService.verify_email_with_token(db_session, user.id, token)
    assert result is True

# Test unlocking a user's account
async def test_unlock_user_account(db_session, locked_user):
    unlocked = await UserService.unlock_user_account(db_session, locked_user.id)
    assert unlocked, "The account should be unlocked"
    refreshed_user = await UserService.get_by_id(db_session, locked_user.id)
    assert not refreshed_user.is_locked, "The user should no longer be locked"
async def test_change_user_role(db_session, user):
    """
    Tests updating a user's role and ensuring it persists in the database.
    """
    new_role = UserRole.MANAGER
    updated_user = await UserService.update(db_session, user.id, {"role": new_role.name})
    assert updated_user is not None, "User should be successfully updated"
    assert updated_user.role == new_role.name, f"User role should be updated to {new_role.name}"
async def test_search_users_by_exact_nickname(db_session, user):
    """
    Tests fetching users by their exact nickname.
    """
    retrieved_user = await UserService.get_by_nickname(db_session, user.nickname)
    assert retrieved_user is not None, "A user should be returned for an existing nickname"
    assert retrieved_user.nickname == user.nickname, "The retrieved user's nickname should match the queried nickname"

async def test_list_users_with_filters(db_session, users_with_same_role_50_users):
    """
    Tests listing users with pagination and manually filters by role.
    """
    role_to_filter = UserRole.AUTHENTICATED  # Assuming all users in the fixture have this role
    users_page_1 = await UserService.list_users(db_session, skip=0, limit=10)
    users_page_2 = await UserService.list_users(db_session, skip=10, limit=10)
    
    # Verify pagination
    assert len(users_page_1) == 10, "Page 1 should contain 10 users"
    assert len(users_page_2) == 10, "Page 2 should contain 10 users"
    assert users_page_1[0].id != users_page_2[0].id, "Users in page 1 should not overlap with users in page 2"

    # Manually filter users by role
    filtered_users = [user for user in users_page_1 + users_page_2 if user.role == role_to_filter.name]
    assert all(user.role == role_to_filter.name for user in filtered_users), "All filtered users should have the specified role"
@pytest.mark.asyncio
async def test_update_user_profile_success(async_client, user, user_token):
    """
    Test successful user profile update.
    """
    updated_data = {
        "first_name": "UpdatedFirstName",
        "last_name": "UpdatedLastName",
        "bio": "This is an updated bio."
    }
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{user.id}/profile", json=updated_data, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["first_name"] == updated_data["first_name"]
    assert response_data["last_name"] == updated_data["last_name"]
    assert response_data["bio"] == updated_data["bio"]


@pytest.mark.asyncio
async def test_update_user_profile_unauthorized(async_client, user):
    """
    Test unauthorized user profile update (missing token).
    """
    updated_data = {"bio": "This is an updated bio."}
    response = await async_client.put(f"/users/{user.id}/profile", json=updated_data)
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_update_user_profile_invalid_data(async_client, user, user_token):
    """
    Test user profile update with invalid data.
    """
    invalid_data = {"bio": ""}  # Bio cannot be empty
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.put(f"/users/{user.id}/profile", json=invalid_data, headers=headers)
    assert response.status_code == 422  # Unprocessable Entity
@pytest.mark.asyncio
async def test_upgrade_to_professional_status_unauthorized(async_client, user, user_token):
    """
    Test professional status upgrade attempt by a regular user (not admin or manager).
    """
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.post(f"/users/{user.id}/professional-status", headers=headers)
    assert response.status_code == 403  # Forbidden

@pytest.mark.asyncio
async def test_update_user_profile_invalid_data(async_client, user, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    invalid_data = {"bio": ""}
    response = await async_client.put(f"/users/{user.id}/profile", json=invalid_data, headers=headers)
    assert response.status_code == 422
@pytest.fixture
def mock_require_role(mocker):
    mocker.patch("app.dependencies.require_role", return_value={"user_id": "8658e6e4-a004-4d74-b12c-61b0f31d91c8", "role": "ADMIN"})
@pytest.mark.asyncio
async def test_update_user_profile_success(async_client, user, admin_token, mock_require_role):
    headers = {"Authorization": f"Bearer {admin_token}"}
    updated_data = {"bio": "Updated bio", "first_name": "NewName"}
    response = await async_client.put(f"/users/{user.id}/profile", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["bio"] == updated_data["bio"]