class useRequest:
    _id = 0
    def __init__(
            self,
            url="",
            method="GET",
            headers=None,
            body=None,
            mode=None,
            credentials=None,
            cache=None,
            redirect=None,
            referrer=None,
            referrerPolicy=None,
            signal=None
        ):

        self.url = url
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.mode = mode
        self.credentials = credentials
        self.cache = cache
        self.redirect = redirect
        self.referrer = referrer
        self.referrerPolicy = referrerPolicy
        self.signal = signal
        self._id = useRequest._id
        useRequest._id += 1

    def to_js(self):
        options = []

        options.append(f'method: "{self.method}"')

        if self.headers:
            options.append(f"headers: {self.headers}")

        if self.body and self.method not in ("GET", "HEAD"):
            options.append(f"body: JSON.stringify({self.body})")

        if self.mode:
            options.append(f'mode: "{self.mode}"')

        if self.credentials:
            options.append(f'credentials: "{self.credentials}"')

        if self.cache:
            options.append(f'cache: "{self.cache}"')

        if self.redirect:
            options.append(f'redirect: "{self.redirect}"')

        if self.referrer:
            options.append(f'referrer: "{self.referrer}"')

        if self.referrerPolicy:
            options.append(f'referrerPolicy: "{self.referrerPolicy}"')

        options_js = ",\n    ".join(options)

        return f"""
const fetch{self._id} = useRequest();
fetch{self._id}.request("{self.url}", {{
    {options_js}
}});
"""

    def __str__(self):
        options = []

        options.append(f'method: "{self.method}"')

        if self.headers:
            options.append(f"headers: {self.headers}")

        if self.body and self.method not in ("GET", "HEAD"):
            options.append(f"body: JSON.stringify({self.body})")

        if self.mode:
            options.append(f'mode: "{self.mode}"')

        if self.credentials:
            options.append(f'credentials: "{self.credentials}"')

        if self.cache:
            options.append(f'cache: "{self.cache}"')

        if self.redirect:
            options.append(f'redirect: "{self.redirect}"')

        if self.referrer:
            options.append(f'referrer: "{self.referrer}"')

        if self.referrerPolicy:
            options.append(f'referrerPolicy: "{self.referrerPolicy}"')

        options_js = ",\n    ".join(options)

        return f"""
const fetch{self._id} = useRequest();
fetch{self._id}.request("{self.url}", {{
    {options_js}
}});
"""

    def get(self, key):
        return f"${{fetch{self._id}.data.get()?.{key}}}"

newRequest = useRequest(
    url="https://jsonplaceholder.typicode.com",
    method="GET",
)
