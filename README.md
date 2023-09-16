[![pytest](https://github.com/Zirochkaa/save-favourite-color/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/Zirochkaa/save-favourite-color/actions/workflows/run_tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Zirochkaa/save-favourite-color/badge.svg?branch=master)](https://coveralls.io/github/Zirochkaa/save-favourite-color?branch=master)

# Save favourite color

This repository contains pet project - fastapi application designed for saving person's favourite color :)

### Link to the working site here - [color.zirochka.me](https://color.zirochka.me/) (currently turned off).

## Run project locally

1. Setup and activate your local python environment. [Here](https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3) are few guides on how to do it.
2. Install requirements:
   ```shell 
   pip install -r requirements-local.txt
   ```
3. Create `.env` file:
   ```shell 
   cp app/.env.template app/.env
   ```
4. Setup PostgreSQL. You have few options:

    4.1. you can use any already existing PostgreSQL (in docker, in any cloud provider, etc.):
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
   gunicorn -c gunicorn_config.py "app:create_app()"
   ```
7. Go to [127.0.0.1:8080](http://127.0.0.1:8080) in your web browser.

## Tests

To run tests use following command:
   ```shell 
   python -m pytest
   ```

*Note*: tests will be run using `DATABASE_URL_TEST`, so you need to create new database and update `DATABASE_URL_TEST`.

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
  - [x] Admins can see a list of all colors with their info on appropriate separate page.
  - [ ] Admins can add new colors to database from appropriate separate page.
  - [x] Admins can see a list of all users with their info on appropriate separate page.
  - [ ] Admins can deactivate users from appropriate separate page.
- [ ] Share link to user's favourite color.

## TODOs

Below is a list of what needs to be done:
- [x] Migrate from SQLite to PostgreSQL.
- [x] Let users edit their favourite color.
- [x] Cover project with tests.
- [x] Run tests on GitHub.
- [x] Use `werkzeug.security` for passwords instead of plain text.
- [ ] Use [flask-debugtoolbar](https://flask-debugtoolbar.readthedocs.io/en/latest/).
- [ ] Migrate from PostgreSQL to MongoDB.
- [ ] Add admin accounts:
  - [x] Add `is_admin` field to `users` table ~~or create completely different table for admins~~.
  - [x] All pages for admin user should look the same as the ones for regular user.
  - [x] Allow admin to see a list of all colors with their info (link to appropriate page should be in admin panel).
  - [ ] Allow admin to add colors to `colors` table (link to appropriate page should be in admin panel).
  - [x] Allow admin to see a list of all users with their info (link to appropriate page should be in admin panel).
  - [ ] Allow admin to deactivate users (link to appropriate page should be in admin panel).
- [ ] Let users share link to their favourite color. This page should:
  - have the following text at the center oh the screen - "{color} is the favourite color of {username}.";
  - have a block with color filling;
  - show headers like `404 page` meaning that some headers should be shown for logged-in user (like `Setting`, `Log out`, etc.) and some other headers should be shown for not logged-in user (like `Log in`, `Sign up`, etc.).
