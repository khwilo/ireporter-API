# iReporter API

[![Build Status](https://travis-ci.org/khwilo/ireporter-API.svg?branch=ft-regular-user-modify-162499170)](https://travis-ci.org/khwilo/ireporter-API) [![Coverage Status](https://coveralls.io/repos/github/khwilo/ireporter-API/badge.svg?branch=ft-regular-user-modify-162499170)](https://coveralls.io/github/khwilo/ireporter-API?branch=ft-regular-user-modify-162499170)  

This repository consists of implementation of the API endpoints for the [iReporter web application](https://khwilo.github.io/iReporter/UI/).  

## API ENDPOINTS DESCRIPTION

- `POST '/api/v1/red-flags'` - Create a red-flag record.
- `GET '/api/v1/red-flags'` - Fetch all red-flag records.
- `GET '/api/v1/red-flags/<red-flag-id>` - Fetch a specific red-flag record.
- `DELETE '/api/v1/red-flags/<red-flag-id>` - Delete a specific red flag record.
- `PUT '/api/v1/red-flags/<red-flag-id>/location'` - Edit the location of a specific red-flag record.
- `PUT '/api/v1/red-flags/<red-flag-id>/comment'` - Edit the comment of a specific red-flag record.
- `POST '/auth/register'` - Create a user record.
- `POST '/auth/login'` - Log in a user.  
