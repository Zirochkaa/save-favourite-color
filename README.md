# Save favourite color

This repository contains final project for `Full Stack Web Development with Flask` course from [pirple.com](https://www.pirple.com/) website.

### Link to the working site is [here](https://save-favourite-color-viu5s.ondigitalocean.app/).

## Run project locally

1. Setup and activate your local python environment. [Here](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) are few guides on how to do it.
2. Install requirements:
   ```shell 
   pip install requirements.txt
   ```
3. Create `.env` file:
   ```shell 
   cp app/.env.template app/.env
   ```
4. Setup PostgreSQL. You have few options:

    4.1. you can use any already existing PostgreSQL (in docker, in any cloud provider, etc):
      1. create new database;
      2. update `DATABASE_URL` in `.env` file;

    4.2. you can setup PostgreSQL locally:
      1. for example, you can use [this](https://www.sqlshack.com/setting-up-a-postgresql-database-on-mac/) guide or any other guide;
      2. after setting up PostgreSQL locally create new database:
         ```shell 
         psql postgres -c 'create database save_favourite_color;'
         ```
5. Apply migrations to your database:
   ```shell 
   flask db upgrade
   ```
6. Run application:
   ```shell 
   flask run
   ```
7. Go to [127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Tests

To run tests use following command:
   ```shell 
   python -m pytest
   ```

If you want to check code coverage use following command:
   ```shell 
   python -m pytest --cov=app
   ```

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
- [x] Migrate from SQLite to PostgreSQL
- [x] Let users edit their favourite color.
- [x] Cover project with tests.
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
