# Bulletin Books

## What is Bulletin Books?

Bulletin Books is a work-in progress web app that allows students to trade textbooks in a centralized location. 

Built by a student, for students.

## Phases & Implied Tasks for MVP

1. Get webpage up
  - [X] endpoints for landing page, view listed textbooks, add new textbook, about, delete
2. Develop new book entries
  - [X] Add ISBN lookup
  - [X] Take in user email for contact info
  - [X] Generate random 5 character string for book deletion
  - [X] Send random to user email
  - [X] Add sqlite3 db for table
  - [X] Add function to access table
3. Develop listing book entries
  - [X] Add function to access table
  - [ ] Access firebase table for book entires
  - [ ] Sort by newly listed, alphabetic order
4. Add a new page for viewing each textbook individually for user email. 

## Phases & Implied Tasks for full product

1. Get webpage up
  - [ ] endpoints for landing page, registration, login, view listed textbooks, add new textbook, user profile
2. Develop user registration and login  
  - [ ] Get firebase registration and login working
    - [ ] sanitize user inputs
  - [ ] Get email server working for user authentication
  - [ ] Allow users to reset password through profile page
3. Develop new book entries
  - [ ] Create new firebase table for book entires
    - [ ] Take in name of book, author, edition, year, condition (drop down of excellent, fair, poor), class, user who posted the book
4. Develop listing book entries
  - [ ] Access firebase table for book entires
  - [ ] Sort by newly listed, alphabetic order
5. Develop user profile page
  - [ ] Reset password
  - [ ] Allow notification emails to be sent to user when

## Wanted Features

- [ ] Dark/light mode toggle
- [ ] Firebase integration
- [ ] User login and authentication through email
- [X] Jinja2 templating
- [X] Mobile-friendly design
