# Save favourite color

This repository contains final project for `Full Stack Web Development with Flask` course from [pirple.com](https://www.pirple.com/) website.

### Link to the working site is [here](https://save-favourite-color-viu5s.ondigitalocean.app/).

## Run project locally

1. Setup and activate your local python environment. [Here](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) are some guides on how to do it.
2. Install requirements:
   ```shell 
   pip install requirements.txt
   ```
3. Create SQLite database with tables:
   ```shell 
   python app/schema.py
   ```
   `flask_tut.db` file will be created inside project root folder.
4. Fill database with data:
   ```bash 
   python app/seed.py
   ```
5. Export flask env variables:
   ```shell 
   export FLASK_APP=app
   export FLASK_ENV=development
   ```

7. Run application:
   ```shell 
   flask run
   ```
8. Go to [127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Features

Right now the site offers following features:
- [x] Register new users.
- [x] Login into user's account.
- [x] Logout from user's account.
- [x] For unknown urls show 404 page.
- [ ] Admin accounts:
  - [ ] Admins can see a list of all users with their info on admin's homepage instead of info about color like regular users see.
  - [ ] Admins can add new colors to database from admin's homepage.
  - [ ] Admins can deactivate users from admin's homepage.
- [ ] Share link to user's favourite color.

## TODOs

Below is a list of what needs to be done:
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Let users edit their favourite color.
- [ ] Cover following with tests:
  - [ ] `model.py` file.
  - [ ] `run.py` file.
  - [ ] `schema.py` file.
  - [ ] `seed.py` files.
- [ ] Run tests on github.
- [ ] Add admin accounts:
  - [ ] Add `is_admin` field to `users` table or create completely different table for admins.
  - [ ] Admin homepage should look different:
    - it should not show info about color, instead it should list all users with their info;
  - [ ] Allow admin to add colors to `colors` table (add link to appropriate page to the upper right corner).
  - [ ] Allow admin to deactivate users from their homepage.
- [ ] Let users share link to their favourite color. The page should include content from the one for logged-in user, but:
  - text should be the following - "{username}'s favourite color is {color}.";
  - block with color should remain;
  - header should look like the one for not logged-in user.
