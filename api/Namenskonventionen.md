# Best-Practices bei der Gestaltung von REST-APIs

## Versionierung

### **Versioning Strategies:**

**1. Query Parameter Versioning:**

- Pros: Clear version separation without changing the URI, easy implementation.
- Cons: May result in long and complex URLs, less intuitive than URI versioning.

**2. Header Versioning:** 

- Pros: Adheres to REST principles, keeps the URI focused on the resource.
- Cons: Less intuitive, requires more effort to inspect requests as version information is in headers.

~~**3. URI Versioning:**~~

- Pros: Easy implementation, clear version separation in the URL.
- Cons: Can lead to cluttered and less readable endpoints, **not recommended** by REST architecture.

### Managing Breaking Changes

**1. Communicate Changes Clearly:**
Provide detailed release notes, migration guides, and updated API documentation.

**2. Use Semantic Versioning:**
Increment major version for breaking changes, minor for backward-compatible features, and patch for bug fixes.

>[Quelle](https://codedamn.com/news/backend/rest-api-versioning-best-practices)

## Namenskonventionen

**1. Use nouns to represent resources:**
RESTful URI should refer to a resource that is a thing (noun) instead of referring to an action (verb) because nouns have properties that verbs do not have – similarly, resources have attributes. Some examples of a resource are:

- Users of the system
- User Accounts
- Network Devices etc.

and their resource URIs can be designed as below:

```http
/device-management/managed-devices 

/device-management/managed-devices/{device-id} 

/user-management/users

/user-management/users/{id}
```

**2. Consistency is the key:**
Use consistent resource naming conventions and URI formatting for minimum ambiguity and maximum readability and maintainability. You may implement the below design hints to achieve consistency:

### Do not use: ### 
**1. Do not use trailing forward slash (/) in URIs**

```http
http://api.example.com/device-management/managed-devices/ 

/*This is much better version*/
http://api.example.com/device-management/managed-devices         
```

**2. Do not use underscores ( _ )**

```http
//More readable
http://api.example.com/inventory-management/managed-entities/{id}/install-script-location  

//Less readable
http://api.example.com/inventory-management/managedEntities/{id}/installScriptLocation  
``` 

**3. Do not use file extensions**

```http
/*Do not use it*/
/device-management/managed-devices.xml  

/*This is correct URI*/
/device-management/managed-devices
```

**4. Never use CRUD function names in URIs**
 
 ```http
  //Get all devices
HTTP GET /device-management/managed-devices  

//Create new Device
HTTP POST /device-management/managed-devices

//Get device for given Id
HTTP GET /device-management/managed-devices/{id} 

//Update device for given Id
HTTP PUT /device-management/managed-devices/{id}

//Delete device for given Id
HTTP DELETE /device-management/managed-devices/{id} 
 ```

 **5. Do not Use Verbs in the URI**

```http
//It is RPC, and not REST
/device-management/managed-devices/{id}/scripts/{id}/execute    
```

*you can find more best practice methods under the following link:* [Quelle](https://restfulapi.net/resource-naming/)

## Korrekter Einsatz der HTTP-Methoden

> HTTP (Hypertext Transfer Protocol) methods, also known as HTTP verbs, indicate the desired action to be performed on a resource. Here are some of the commonly used HTTP methods along with their correct use:

**1. GET:**
Used to retrieve resources from the server. GET requests should be safe and not have any impact on the server's state. They are often used to load web pages, images, or other static content.

```http
GET /profile HTTP/1.1
Host: www.example.com
Content-Type: application/json

{"name": "John Doe", "age": 20}
```

**2. POST:**
Used to send data to the server to create a new resource. POST requests can be used to submit form data or upload files.

```http
POST /form HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
```

**3. PUT:**
Used to create or update a resource on the server. Unlike POST, a PUT request should be idempotent, meaning that multiple consecutive requests should have the same effect as a single request.

```http
PUT /profile HTTP/1.1
Host: www.example.com
Content-Type: application/json

{"name": "John Doe", "age": 30}
```

**4. Delete:**
Used to delete a resource on the server.

```http
DELETE /resource HTTP/1.1
Host: www.example.com
```

**5. PATCH:**
PATCH: Used to partially update a resource. It is useful when you only want to modify specific fields of a resource without updating the entire resource.

```http
PATCH /resource HTTP/1.1
Host: www.example.com
Content-Type: application/json

{"status": "inactive"}
```

**6. OPTIONS:**
Allows the client to inquire about the supported methods or communication options for a resource.

```http
OPTIONS /info HTTP/1.1
Host: www.example.com
```


 *These methods form the foundation of communication between the client and server. It's important to use the appropriate methods based on the intended action to ensure consistent and secure communication.*

[Quelle](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)