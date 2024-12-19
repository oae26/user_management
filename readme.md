# Reflection Document: 

This course definitely gave me more learning than I had thought I would acquire. I went into this class at first a bit confused as to why it was named “building web apps”, as we were mainly working with Python. As the semester progressed, however, I realized that it was more informative than it let on. I definitely learned a lot on how to use GitHub, and how to set up environment variables, tasks and issues. I had always struggled with Git/Github, and I never really learned how to use it until now, and I’d say I’ve become quite good at it. In addition to Git, I’d never used Ubuntu or WSL at all, so this was a fun learning experience and a good way to prepare myself for a class like IT490. I’d say the only thing I still don’t understand is Docker, since I’m not entirely sure how it works exactly, but overall, I learned a lot more than I thought I would. I would say Professor Wenbo also did a great job of informing the class and instructing us all. Getting to learn and use FastAPI was also a fun experience, and all the DevOps was informative and intriguing. Getting to explore adding my own test cases let me really learn why we have them, and how we actually write them to be effective. Additionally, adding the new feature was pretty cool as well. To conclude, this course increased my knowledge on coding, and gave me more insights.

# DockerHub deployment link:

1. https://hub.docker.com/repository/docker/oae26/is218final/general

# Feature Added: 

Feature 8, which was updating the users to allow for role updates. 

# Link to GitHub with All Commits
1. https://github.com/oae26/user_management


## User Profile Management

This feature lets users manage their profile information. Users can update fields such as their name, bio, location, and other personal details.
Key Features:

    Users can edit their own profile details.
    Admins and managers can edit the profile of any user.
    Validation is applied to ensure only valid data is updated.
    Changes are immediately persisted in the database.

## Professional Status Upgrade

This feature empowers admins and managers to upgrade users to "Professional" status.

Key Features:

    Admins and managers can promote users to professional status via a dedicated API endpoint.
    Sends notifications to users upon status upgrade, ensuring transparency and acknowledgment. This also shows users their professional status on their pages, for visibility.