# Admin Site

OwnRecipes uses the powerful Django Admin Site to make administrative tasks easy.

## How to reach the admin site

Once OwnRecipes is running, you can visit the admin site via the [configured url](Setting_up_env_file.md#admin_url).
By default, that will be `<API_URL>/admin/`, ex. `https://my-ownrecipes-server.com/admin/` for production or
`http://localhost:5210/admin/` for local development.

## Login

Use your [superuser](Running_the_App.md#first-time-setup) to log in.

## Manage users

To create a new user, or edit or delete existing users, navigate to the users admin site via the main menu.
The url will look like `<API_URL>/admin/auth/user/`.

Users have at least the following properties:

| Property     | Explanation |
| ------------ | ----------- |
| Username     | This one is really important. That name is being used for the login, and will be displayed at various places. |
| Active       | If this checkbox is disabled, then this user can no longer be used to log in. |
| Staff status | If this checkbox is enabled, then this user may log in to the Admin Site. |

All other properties, like `First name` and `Last name`, are purely informative and not used by OwnRecipes.
Feel free to fill them as needed.

### Create user

To create a user, select `Add user`, fill in the form and hit `[Save]`.

### Edit user

To edit an existing user, select the user, change the form and hit `[Save]`.

### Change password

Select the user which password should be changed. Then select `[Change password]`.

### Delete user

To delete an existing user, select the user, and hit `[Delete]`.

## Manage news

The news page is part of OwnRecipes homepage. It is global for all users.
To manage the news, navigate to the news admin site via the main menu.
The url will look like `<API_URL>/admin/news/news/`.

If you [imported the test data](Running_the_App.md#first-time-setup) when setting up OwnRecipes,
then you will have already a single news item called `OwnRecipes`. Feel free to edit or delete it.
You can add an arbitrary amount of news items. If there is no active news item to display, then the space will be freed.

News items have the following properties:

| Property  | Explanation |
| --------- | ----------- |
| Title     | The title is displayed as a heading. |
| Content   | The content will be displayed below the heading. Please be aware of some special placeholders, see below. |
| Image     | The image will be used as background for the news item. You can choose any image, but be aware that large images may have performance impact. |
| Frontpage | If this checkbox is disabled, then this news item won't be displayed. |

### Placeholders

OwnRecipes will render some special content, if the news item' content is set to a placeholder.
The content has to exactly match the placeholder, nothing more or less, in order to work.

| Placeholder      | Explanation |
| ---------------- | ----------- |
| `%introduction%` | Display some short description about OwnRecipes, as seen on the [demo site](https://ownrecipes.github.io/ownrecipes-web/). |
| `%features%`     | Display some nice overview of OwnRecipes features, as seen on the [demo site](https://ownrecipes.github.io/ownrecipes-web/). |

## Manage recipe groups

OwnRecipes supports recipe groups, namely `Courses`, `Cuisines`, `Seasons` and `Tags`. When creating or editing recipes, those lists will be extended by new items.

You can manage those lists via the the Admin Site. It can prove useful to add some pre-defined items, that are suggested when using the recipe form.
Or perhaps you want to remove or rename some existing items.

## Manage everything else

Via the Admin Site you can manage most data for OwnRecipes.
Please be aware that there may be complex relations between those data items.
Please make sure you fully understand what you are doing.

You probably do not need to touch any of these.
