DRF ASSESMENT

This repo consists of a DRF based RESTFUL blog application consisting of email based verification, jwt based user request verifications, CRUDs for both user and blogs as well as paginated public views for blogs.

The URLS consist of: 

**ACCOUNTS URLS:**
- 'register/'
    - No brainer. Used to register.json params include: 
        - username
        - email
        - password
        - password_confirm
- 'verify/'
    - Used to verify registered user.json params include: 
        - email
        - email_verification_token
- 'login/'  
    - json params include: 
        - username
        - password
    - returns access token that can be used for posting and patching user based data

**BLOG URLS:**
- 'me/blogs/setting/'   [GET, POST, PATCH]
    - blog params include:
        - title
        - blog_text
        - image
    - for PATCH-ing remember to mention uid of blog as 'uid' for pk.
- '<str:username>/blogs/'  basic public GET
  
**PROFILE URLS:**
- 'me/profile/setting/'  [POST, PATCH]
    - profiles params include:
        - credit
        - address
        - profileimg
    - for PATCH-ing remember to mention user id of profile as 'user' for pk.
- '<str:username>/profile/'   basic public GET

