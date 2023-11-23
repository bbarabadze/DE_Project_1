"""
    This module contains API functions
"""

# Standard packages
from typing import List
# 3rd Party packages
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
# User-defined packages
from api_validation import NameOccurrence, UserActivity, validate_top_number
from drawing import create_graph
from analytics import top_names, top_most_active
from main import REACTIONS_FOLDER, POSTS_FOLDER, USERS_FILE

app = FastAPI()


@app.get("/common_name/top/{top_number}", tags=["Tops"])
async def get_top_common_names(top_number: int) -> list[NameOccurrence]:
    """
    Retrieves the top <top number> most common names on the social network\n
    **param** top_number: Integer number between 1 and 1000, number of the top most common names\n
    **return**  List of the top most common names
    """
    # Number must be between 1 and 1000
    validate_top_number(top_number)

    # Gets dataframe of most common names
    top_common_names_df = top_names(USERS_FILE, top_number)

    # Populates a list of pydantic objects from pandas dataframe
    result = [NameOccurrence(**item) for item in top_common_names_df.to_dict(orient='records')]

    return result


@app.get("/activity/top/{top_number}", tags=["Tops"])
async def get_top_active_users(top_number: int) -> List[UserActivity]:
    """
    Retrieves the top <top number> most active users on the social network\n
    **param** top_number: Integer number between 1 and 1000, number of the top most active users\n
    **return**  List of the top most active users
    """

    # Number must be between 1 and 1000
    validate_top_number(top_number)

    # Gets dataframe of most active users
    tops = top_most_active(REACTIONS_FOLDER, POSTS_FOLDER, USERS_FILE, top_number)

    # Populates a list of pydantic objects from pandas dataframe
    result = [UserActivity(**item) for item in tops.to_dict(orient='records')]
    return result


@app.get("/get_friends/{user_id}", tags=["Friendship"])
async def get_friends_graph(user_id: int):
    """
    Draws graph illustrating all friends of the specified user and their friendships\n
    **param** user_id: ID of the user\n
    **return** A Graph image
    """

    img_byte_array = create_graph(user_id)

    if img_byte_array:
        # Return the image as a streaming response
        return StreamingResponse(img_byte_array, media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404, detail="User ID doesn't exist")


if __name__ == '__main__':
    uvicorn.run('api:app', port=8001, reload=True)
