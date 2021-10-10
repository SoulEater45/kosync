# kosync

This project is based on the [koreader-sync](https://github.com/myelsukov/koreader-sync) project and will be extended, so it can be used with the [calibre-web](https://github.com/janeczku/calibre-web) project. It will also have a accompanied Dockerfile, so it can be ran alongside other projects.

# API

Again, thanks to [myelsukov](https://github.com/myelsukov) for the code.
The follwing API list is extracted from his [code](https://github.com/myelsukov/koreader-sync/blob/master/koreader-flask.py):

## Register User

|               |                   |
|---------------|-------------------|
| **URL**       | `/users/create`   |
| **METHOD**    | `POST`            |

## Auth User

|               |                   |
|---------------|-------------------|
| **URL**       | `/users/auth`     |
| **METHOD**    | `POST`            |

## Sync Progress for Document

|               |                               |
|---------------|-------------------------------|
| **URL**       | `/syncs/progress/<document>`  |
| **METHOD**    | `POST`                        |

## Sync Progress

|               |                   |
|---------------|-------------------|
| **URL**       | `/syncs/progress` |
| **METHOD**    | `PUT`             |

