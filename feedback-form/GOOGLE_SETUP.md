# One-time Google setup for the feedback forms

You do this once. After it, creating each year's four forms is one command,
and the QR codes in the slide decks never change.

Nothing secret goes in this repository. Both files below live under
`~/.config/introtopython/`, outside every git working tree.

## 1. Make a Google Cloud project

1. Go to <https://console.cloud.google.com/projectcreate>.
2. Name it something recognisable, e.g. `introtopython-feedback`. No
   organisation needed. Create.

## 2. Turn on the Forms API

1. With that project selected, go to
   <https://console.cloud.google.com/apis/library/forms.googleapis.com>.
2. Enable.

## 3. Set up the consent screen

Google renamed this. There is no longer an "OAuth consent screen" menu item:
it is now **APIs & Services → Google Auth Platform**, split across the tabs
**Branding**, **Audience** and **Clients**. If a guide tells you to look for
"OAuth consent screen", this is where it went.

1. Go to <https://console.cloud.google.com/auth/branding> and set the app
   name to `IntroToPython feedback`, with your own address as support and
   developer email.
2. Go to <https://console.cloud.google.com/auth/audience> and choose the user
   type:
   - **Internal**, if this is a University of Konstanz Workspace account.
     Simpler: there is no test user list and you can go straight to step 4.
   - **External** otherwise. Then, still on the Audience page, under
     **Test users** click **Add users** and add your own Google address.
     Without this, the consent screen will refuse you.

If the Audience page shows no **Test users** section at all, it is because
the app is Internal, or because its publishing status is *In production*
rather than *Testing*. In both cases there is nothing to add here.

## 4. Create the OAuth client

1. **APIs & Services → Credentials → Create credentials → OAuth client ID**.
2. Application type: **Desktop app**. Name it anything.
3. **Download JSON**.
4. Put it here, and keep it to yourself:

```bash
mkdir -p ~/.config/introtopython
mv ~/Downloads/client_secret_*.json ~/.config/introtopython/google_client_secret.json
chmod 600 ~/.config/introtopython/google_client_secret.json
```

## 5. Create the forms

```bash
python tools/make_google_forms.py --dry-run   # check the questions read right
python tools/make_google_forms.py             # create and publish them
python tools/make_feedback.py                 # regenerate the redirect pages
```

The first real run opens a browser once so you can approve access. Because
the app is yours and unverified, Google shows **"Google hasn't verified this
app"**. That is expected: click *Advanced* then *Go to IntroToPython feedback
(unsafe)*. It is your own project asking for access to your own forms.

## Next year

Edit `year` in `forms.toml`, then:

```bash
python tools/make_google_forms.py && python tools/make_feedback.py
```

Commit the result. **Do not reprint or re-export any QR code.** The images in
the slide decks point at this repository, not at Google, and the redirect
pages are what change.

## Two things worth knowing

**You will probably be asked to approve access again each year.** While the
OAuth app stays in *Testing* status, Google expires the stored refresh token
after seven days. That is harmless here, because the tool is run about twice a
year: it just means the browser opens and you click *Allow*. Publishing the
app to *Production* would avoid it but invites a verification review for a
one-person tool, which is not worth it.

**Email collection is forced off, deliberately.** The API defaults
`emailCollectionType` to `DO_NOT_COLLECT` for a personal Google account but to
`VERIFIED` for a Workspace account. On a Workspace account the forms would
quietly record who answered, while the form text promises they do not. So
`make_google_forms.py` sets `DO_NOT_COLLECT` explicitly and then reads each
form back to confirm it, and fails loudly if it ever comes back otherwise.
