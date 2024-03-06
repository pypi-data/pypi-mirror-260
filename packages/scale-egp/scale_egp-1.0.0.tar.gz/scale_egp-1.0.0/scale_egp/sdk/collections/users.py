from scale_egp.sdk.types.user_info import UserInfoResponse

from scale_egp.utils.api_utils import APIEngine


class UsersCollection(APIEngine):
    """
    Collections class for Scale EGP users.
    """

    _sub_path = "users"

    def who_am_i(self) -> UserInfoResponse:
        """
        Get the currently authenticated user.

        Returns:
            The currently authenticated user.
        """
        response = self._get(sub_path="user-info")
        return UserInfoResponse.from_dict(response.json())

    def get(self, id: str) -> UserInfoResponse:
        """
        Get a user by ID.

        Args:
            id: The ID of the user.

        Returns:
            The user.
        """
        response = self._get(sub_path=f"{self._sub_path}/{id}")
        return UserInfoResponse.from_dict(response.json())
