# kosync

This project is based on the [koreader-sync](https://github.com/myelsukov/koreader-sync) project and will be extended, so it can be used with the [calibre-web](https://github.com/janeczku/calibre-web) project. It will also have a accompanied Dockerfile, so it can be ran alongside other projects.

# API

Again, thanks to [myelsukov](https://github.com/myelsukov) for the code.
The follwing API list is extracted from his [code](https://github.com/myelsukov/koreader-sync/blob/master/koreader-flask.py):

## Register User

Called when going to Tools &rarr; Progress sync &rarr; Register/Login <br>
and `Register` is pressed with filled out `username` and `password`.

|               |                   |
|---------------|-------------------|
| **URL**       | `/users/create`   |
| **METHOD**    | `POST`            |

Received data:
```json
{
    "username": "himynamewhat",
    "password": "5c2f3cbbb37cdabc265ea5ed178493bf"
}
```
The password is an MD5 hash.

## Auth User

Called when going to tools &rarr; Progress sync &rarr; Register/Login <br>
and `Login` is pressed with filled out `username` and `password`.

|               |               |
|---------------|---------------|
| **URL**       | `/users/auth` |
| **METHOD**    | `GET`         |

The headers `x-auth-user` and `x-auth-key`

## Sync Progress for Document

Called when going to tools &rarr; Progress sync &rarr; Pull progress from other devices. <br>
If a saved progress is found, it will be fetched.

|               |                               |
|---------------|-------------------------------|
| **URL**       | `/syncs/progress/<document>`  |
| **METHOD**    | `GET`                         |

## Sync Progress

Called when going to Tools &rarr; Progress sync &rarr; Push progress from this device. <br>
Sends data about the current progress on the device.

|               |                   |
|---------------|-------------------|
| **URL**       | `/syncs/progress` |
| **METHOD**    | `PUT`             |

Received data:
```json
{
    "progress": "/body/DocFragment[6]/body/div[1]/div[1]/span/text().0",
    "document": "3b2e2de1b930903ce39956017920fc91",
    "percentage": 0.69,
    "device_id": "fc6d593bb3b59d5509c9cfe3d7a2629e",
    "device": "myiphone"
}
```
The document field is an MD5 hash of either the filename or the binary, which can be adjusted at Tools &rarr; Progress sync &rarr; Document matching method.

## Additional Information

The API is served under `http://<url>:<port>/kosync/<api-endpoint>`. This is done, so it can be easily integrated into other projects, like [calibre-web](https://github.com/janeczku/calibre-web) and is inspired by their [kobo integration](https://github.com/janeczku/calibre-web/blob/master/cps/kobo.py).

# TODO

Things to do before integrating into [calibre-web](https://github.com/janeczku/calibre-web):

* The verification process can be made optional and a token may be used in the URL, similarly to the [kobo-auth](https://github.com/janeczku/calibre-web/blob/master/cps/kobo_auth.py) integration. But just for security reasons, so it wont get spammed, the provided username could be mathed against the username on calibre-web.
* KOReader saves the files from OPDS in the form of `(<author> - )<book name>.<extension>` (see [here](https://github.com/koreader/koreader/blob/0d231cbbef487c2a83b4ebb939490ecbbb929163/plugins/opds.koplugin/opdsbrowser.lua#L600)). This can be used to make a table of MD5 hash - book (ID) values, so it is known what the progress is for each book! The MD5 hash is used, since you can also use the server of KOReader and they don't want to save sensible informations (or so I guess?).
* The `metadata.db` database of calibre has a `last_read_positions` table which is still unused, or at least mine has no data. The stored data from KOReader and the Kobo integration could be used to display the progress in each book in the user interface. At least both options provide a percentage value and something like the maximum value can be used to be displayed, with other values shown if needed (dropdown, hover, etc).