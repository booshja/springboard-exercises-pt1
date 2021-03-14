In order to run this, you will need to have a .env file containing the following variables:
- CURR_USER_KEY : this can be set to "curr_user" to initialize
- DATABASE_URI : this is set to your "warbler" database. It was built with PostgreSQL.
 > Note: for testing, comment this variable out, as the code will default to the testing database ("warbler-test") if DATABASE_URI is not found.
- SECRET_KEY
