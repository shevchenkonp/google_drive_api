This simple app implements Secure Upload and upload file to Google Drive after.

The Secure Upload for filtering file format is presented in the app. 
Configuring decided formats is available with the app config.

After the Secure Upload check Google Drive Api takes file from uploads folder and redirects it to 
specified Google Drive Folder (determined by FOLDER_ID).

Also the authentication with the Flask-Security is implemented. 
The design of default Flask-Security LoginForm is changed with Bootstrap.

For the user authentication app uses the Soft Block. 
The Soft Block implies block user after a few unsuccessful login attempts for a necessary time.
