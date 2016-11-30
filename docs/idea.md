Modules:

    Request from integration test:

      HTTP Server
        Representation of the Request

      HTTP Client
        Forwarded Request

    Response from HTTP API:

      HTTP Client
        Representation of the Response

      HTTP Server
        Forwarded Response

     After forwarded response: 

      Write the Requests and Responses to a .md file.

On persistence:

    Stenograpi will need to somehow store what it observes over
    the wire. A request, as far as I know, always has (0, 1) response.

    This should get stored in mutliple files per request. Differentiate
    requests by looking at the method, path and body. Allow for customization.

    Each file should then be transpiled to a Markdown document. When you
    first run Stenograpi this document will look very shallow, because 
    Stenograpi only has raw data from the HTTP exchange. However, the developer
    can easily edit the file with titles and descriptions. When Stenograpi
    is ran for a second time, these will be included in the document.

    We are in a sense testing use cases. That is the whole point. And a use
    case often has succeeding and failing outcomes. This must be taken into account.

On tests:
    Should not really be coupled to tests after all, it has no 
    obvious benefit since we can not extract the test name, test
    description and assertion.

    Instead, the main use case example could just be cURL requests (?).
