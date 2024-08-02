**XSS PIMP**

- Dynamic Payload Creation: Generates multiple variations of each payload to increase detection rates.

- Advanced HTML Parsing: Uses BeautifulSoup to parse the HTML response and detect XSS vulnerabilities more reliably.

- Session Management: Supports authenticated testing by maintaining a session and logging in before testing.

- User-Agent Rotation and Proxy Support: Randomly selects a User-Agent and optional proxies for each request.

- Detailed Configuration: Allows users to input custom payloads, additional parameters, and login details interactively.

- Multithreading: Utilizes ThreadPoolExecutor for efficient parallel testing.

- Comprehensive Logging: Logs detailed results and errors to a file for easy review.

- Error Handling: Improved error handling to manage and log exceptions effectively.
