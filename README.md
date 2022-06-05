# Save favourite color

This repository contains final project for `Full Stack Web Development with Flask` course from [pirple.com](https://www.pirple.com/) website.

## Features

Right now the site offers the following features:
- register new users;
- login to user's account;
- logout from user's account;
- 404 page;

## TODOs

Below is a list of what needs to be done:
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
